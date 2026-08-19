"""
Pathfinder — Database Seed Script

Validates the course/skills dataset and populates PostgreSQL with:
- Skills taxonomy
- Course catalog with embeddings
- Course-skill mappings
- Prerequisite graph edges (validated as a DAG)

Run: python -m app.seed
"""

import json
import asyncio
import sys
from pathlib import Path
from uuid import uuid4
from collections import Counter

import networkx as nx
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker, init_db, engine
from app.core.embeddings import EmbeddingService
from app.models import (
    Skill, Course, CourseSkill, CoursePrerequisite
)


# ─── Paths ───────────────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SKILLS_FILE = DATA_DIR / "skills.json"
COURSES_FILE = DATA_DIR / "courses.json"


# ─── Dataset Validation ─────────────────────────────────────────────────────

class ValidationError:
    def __init__(self, check: str, message: str, severity: str = "ERROR"):
        self.check = check
        self.message = message
        self.severity = severity

    def __str__(self):
        return f"[{self.severity}] {self.check}: {self.message}"


def validate_dataset(skills_data: list[dict], courses_data: list[dict]) -> list[ValidationError]:
    """Run all 8 mandatory validation checks on the dataset."""
    errors: list[ValidationError] = []

    # Build lookup sets
    skill_names = {s["name"] for s in skills_data}
    course_titles = [c["title"] for c in courses_data]
    course_title_set = set(course_titles)
    valid_difficulties = {"beginner", "intermediate", "advanced"}

    # ── Check 1: Duplicate courses ──
    title_counts = Counter(course_titles)
    for title, count in title_counts.items():
        if count > 1:
            errors.append(ValidationError(
                "DUPLICATE_COURSE",
                f"Course '{title}' appears {count} times"
            ))

    for i, course in enumerate(courses_data):
        title = course.get("title", f"<course index {i}>")

        # ── Check 2: Missing skills ──
        for skill in course.get("skills_taught", []):
            if skill not in skill_names:
                errors.append(ValidationError(
                    "MISSING_SKILL",
                    f"Course '{title}' references skill '{skill}' which is not in skills.json"
                ))

        # ── Check 3: Invalid prerequisites ──
        for prereq in course.get("prerequisites", []):
            if prereq not in course_title_set:
                errors.append(ValidationError(
                    "INVALID_PREREQUISITE",
                    f"Course '{title}' has prerequisite '{prereq}' which does not exist"
                ))

        # ── Check 4: Self-prerequisite ──
        if title in course.get("prerequisites", []):
            errors.append(ValidationError(
                "SELF_PREREQUISITE",
                f"Course '{title}' lists itself as a prerequisite"
            ))

        # ── Check 5: Invalid difficulty ──
        difficulty = course.get("difficulty_level", "")
        if difficulty not in valid_difficulties:
            errors.append(ValidationError(
                "INVALID_DIFFICULTY",
                f"Course '{title}' has invalid difficulty '{difficulty}' "
                f"(must be one of: {', '.join(sorted(valid_difficulties))})"
            ))

        # ── Check 6: Invalid rating ──
        rating = course.get("rating", 0)
        if not (0.0 <= rating <= 5.0):
            errors.append(ValidationError(
                "INVALID_RATING",
                f"Course '{title}' has rating {rating} (must be 0.0–5.0)"
            ))

        # ── Check 7: Invalid duration ──
        duration = course.get("duration_hours", 0)
        if duration <= 0:
            errors.append(ValidationError(
                "INVALID_DURATION",
                f"Course '{title}' has duration {duration} hours (must be > 0)"
            ))

    # ── Check 8: Prerequisite cycles (DAG validation) ──
    G = nx.DiGraph()
    for course in courses_data:
        title = course["title"]
        G.add_node(title)
        for prereq in course.get("prerequisites", []):
            if prereq in course_title_set:  # only add valid edges
                G.add_edge(prereq, title)  # prereq → course

    if not nx.is_directed_acyclic_graph(G):
        cycles = list(nx.simple_cycles(G))
        for cycle in cycles[:5]:  # show first 5 cycles
            errors.append(ValidationError(
                "PREREQUISITE_CYCLE",
                f"Cycle detected: {' → '.join(cycle)} → {cycle[0]}"
            ))

    return errors


# ─── Seeding Logic ───────────────────────────────────────────────────────────

async def seed_database():
    """Main seed function: validate, insert, embed."""

    print("=" * 60)
    print("  Pathfinder — Database Seed Script")
    print("=" * 60)

    # ── Load data files ──
    print("\n📂 Loading data files...")
    if not SKILLS_FILE.exists():
        print(f"❌ Skills file not found: {SKILLS_FILE}")
        sys.exit(1)
    if not COURSES_FILE.exists():
        print(f"❌ Courses file not found: {COURSES_FILE}")
        sys.exit(1)

    with open(SKILLS_FILE, "r", encoding="utf-8") as f:
        skills_data = json.load(f)
    with open(COURSES_FILE, "r", encoding="utf-8") as f:
        courses_data = json.load(f)

    print(f"   Loaded {len(skills_data)} skills, {len(courses_data)} courses")

    # ── Validate dataset ──
    print("\n🔍 Validating dataset...")
    errors = validate_dataset(skills_data, courses_data)

    if errors:
        print(f"\n❌ Validation FAILED with {len(errors)} error(s):\n")
        for err in errors:
            print(f"   {err}")
        print("\n   Fix these errors in the data files and re-run the seed script.")
        sys.exit(1)
    else:
        print("   ✅ All 8 validation checks passed!")

    # ── DAG statistics ──
    G = nx.DiGraph()
    for course in courses_data:
        G.add_node(course["title"])
        for prereq in course.get("prerequisites", []):
            G.add_edge(prereq, course["title"])

    entry_points = [n for n in G.nodes() if G.in_degree(n) == 0]
    leaf_courses = [n for n in G.nodes() if G.out_degree(n) == 0]
    longest_path = nx.dag_longest_path(G)

    print(f"   📊 DAG: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"   📊 Entry points (no prereqs): {len(entry_points)}")
    print(f"   📊 Leaf courses (no dependents): {len(leaf_courses)}")
    print(f"   📊 Longest prerequisite chain: {len(longest_path)} courses")

    # ── Initialize database ──
    print("\n🗄️  Initializing database tables...")
    await init_db()
    print("   ✅ Tables created")

    # ── Enable pgvector extension ──
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
    print("   ✅ pgvector extension enabled")

    # ── Load embedding model ──
    print("\n🤖 Loading embedding model...")
    embedding_service = EmbeddingService()
    embedding_service.load()
    print("   ✅ Model loaded")

    # ── Clear existing data ──
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(text("DELETE FROM course_prerequisites"))
            await session.execute(text("DELETE FROM course_skills"))
            await session.execute(text("DELETE FROM courses"))
            await session.execute(text("DELETE FROM skills"))
        print("   🧹 Cleared existing seed data")

    # ── Insert skills ──
    print("\n📝 Inserting skills...")
    skill_id_map: dict[str, str] = {}  # skill_name -> UUID str

    async with async_session_maker() as session:
        async with session.begin():
            for skill_data in skills_data:
                skill_id = uuid4()
                skill = Skill(
                    id=skill_id,
                    name=skill_data["name"],
                    track=skill_data["track"],
                    description=skill_data.get("description"),
                )
                session.add(skill)
                skill_id_map[skill_data["name"]] = skill_id
        print(f"   ✅ Inserted {len(skills_data)} skills")

    # ── Generate embeddings ──
    print("\n🔢 Generating course embeddings...")
    embedding_texts = []
    for course in courses_data:
        text_blob = (
            f"{course['title']} "
            f"{course['description']} "
            f"{', '.join(course.get('skills_taught', []))}"
        )
        embedding_texts.append(text_blob)

    embeddings = embedding_service.encode_batch(embedding_texts)
    print(f"   ✅ Generated {len(embeddings)} embeddings (dim={len(embeddings[0])})")

    # ── Insert courses ──
    print("\n📝 Inserting courses...")
    course_id_map: dict[str, str] = {}  # course_title -> UUID str

    async with async_session_maker() as session:
        async with session.begin():
            for i, course_data in enumerate(courses_data):
                course_id = uuid4()
                course = Course(
                    id=course_id,
                    title=course_data["title"],
                    description=course_data["description"],
                    provider=course_data.get("provider"),
                    track=course_data["track"],
                    difficulty_level=course_data["difficulty_level"],
                    duration_hours=course_data["duration_hours"],
                    rating=course_data.get("rating", 4.0),
                    url=course_data.get("url"),
                    embedding=embeddings[i],
                )
                session.add(course)
                course_id_map[course_data["title"]] = course_id
        print(f"   ✅ Inserted {len(courses_data)} courses")

    # ── Insert course-skill mappings ──
    print("\n📝 Inserting course-skill mappings...")
    mapping_count = 0

    async with async_session_maker() as session:
        async with session.begin():
            for course_data in courses_data:
                course_id = course_id_map[course_data["title"]]
                for skill_name in course_data.get("skills_taught", []):
                    skill_id = skill_id_map[skill_name]
                    cs = CourseSkill(
                        course_id=course_id,
                        skill_id=skill_id,
                        proficiency_gained=1,
                    )
                    session.add(cs)
                    mapping_count += 1
        print(f"   ✅ Inserted {mapping_count} course-skill mappings")

    # ── Insert prerequisite edges ──
    print("\n📝 Inserting prerequisite edges...")
    prereq_count = 0

    async with async_session_maker() as session:
        async with session.begin():
            for course_data in courses_data:
                course_id = course_id_map[course_data["title"]]
                for prereq_title in course_data.get("prerequisites", []):
                    prereq_id = course_id_map[prereq_title]
                    cp = CoursePrerequisite(
                        course_id=course_id,
                        prerequisite_course_id=prereq_id,
                    )
                    session.add(cp)
                    prereq_count += 1
        print(f"   ✅ Inserted {prereq_count} prerequisite edges")

    # ── Create HNSW index ──
    print("\n📊 Creating HNSW vector index...")
    async with engine.begin() as conn:
        # Drop existing index if any
        await conn.execute(text(
            "DROP INDEX IF EXISTS courses_embedding_hnsw_idx"
        ))
        await conn.execute(text(
            "CREATE INDEX courses_embedding_hnsw_idx "
            "ON courses USING hnsw (embedding vector_cosine_ops)"
        ))
    print("   ✅ HNSW index created")

    # ── Test similarity search ──
    print("\n🔎 Testing similarity search...")
    test_query = "I know Python, want to learn data analysis"
    query_embedding = embedding_service.encode(test_query)

    async with async_session_maker() as session:
        result = await session.execute(
            text("""
                SELECT title, description, track, difficulty_level,
                       1 - (embedding <=> :embedding::vector) as similarity
                FROM courses
                ORDER BY embedding <=> :embedding::vector
                LIMIT 5
            """),
            {"embedding": str(query_embedding)}
        )
        rows = result.fetchall()

        print(f"\n   Query: \"{test_query}\"")
        print(f"   Top 5 results:")
        for i, row in enumerate(rows, 1):
            print(f"   {i}. [{row.difficulty_level}] {row.title} "
                  f"(sim={row.similarity:.4f}, track={row.track})")

    # ── Summary ──
    print("\n" + "=" * 60)
    print("  ✅ Seed complete!")
    print(f"  📊 {len(skills_data)} skills")
    print(f"  📚 {len(courses_data)} courses")
    print(f"  🔗 {mapping_count} course-skill mappings")
    print(f"  ➡️  {prereq_count} prerequisite edges")
    print(f"  🔢 {len(embeddings)} embeddings (dim={len(embeddings[0])})")
    print(f"  📈 HNSW index active")
    print(f"  🌳 DAG validated (acyclic ✓)")
    print("=" * 60)


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    asyncio.run(seed_database())
