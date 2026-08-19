export interface Skill {
  id: string;
  name: string;
  track: string;
  description?: string;
}

export interface Course {
  id: string;
  title: string;
  description: string;
  provider: string;
  track: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  duration_hours: number;
  rating: number;
  url?: string;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
  skills: UserSkill[];
  interests: UserInterest[];
}

export interface UserSkill {
  skill_id: string;
  skill_name: string;
  proficiency_level: number;
}

export interface UserInterest {
  track: string;
  weight: number;
}

export interface Goal {
  id: string;
  raw_text: string;
  target_role?: string;
  target_skills?: string[];
  timeframe_weeks?: number;
  hours_per_week?: number;
  status: 'active' | 'completed' | 'abandoned';
}

export interface LearningPath {
  id: string;
  goal_id: string;
  status: string;
  items: PathItem[];
}

export interface PathItem {
  id: string;
  course: Course;
  sequence_order: number;
  milestone_number: number;
  status: 'locked' | 'available' | 'in_progress' | 'completed';
  explanation_text?: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'tool';
  content: string;
  created_at: string;
}

export interface FeedbackEvent {
  path_item_id: string;
  feedback_type: 'too_easy' | 'too_hard' | 'not_relevant' | 'helpful';
}
