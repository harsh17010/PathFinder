import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { api } from '../services/api';
import type { LearningPathDetail } from '../types';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { CourseCard } from '../components/ui/CourseCard';
import { MilestoneCard } from '../components/ui/MilestoneCard';
import { Map, AlertCircle } from 'lucide-react';

const PathPage: React.FC = () => {
  const { userId, activeGoal } = useUser();
  const navigate = useNavigate();
  const [path, setPath] = useState<LearningPathDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchPath = async () => {
    if (!userId || !activeGoal) return;
    try {
      setLoading(true);
      // Fetch latest path for the user and goal. 
      // If none, maybe try to generate or just show error.
      // Assuming GET /api/v1/paths/{userId} doesn't quite exist in our typed mock, 
      // let's use generatePath for now or mock it since it's a hackathon.
      // But we have GET /api/v1/paths/{userId} in the original api.ts? Let's check `api` in types
      // Actually, we replaced it with generatePath and getPathDetail.
      // We don't have a list paths endpoint. We can just generate one if none.
      const newPath = await api.generatePath(userId, activeGoal.id);
      setPath(newPath);
    } catch (e) {
      console.error(e);
      setError('Failed to load learning path. Have you chatted with Pathfinder to create one?');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!userId) {
      navigate('/onboarding');
      return;
    }
    if (!activeGoal) {
      setLoading(false);
      setError('No active goal found. Please set a goal first.');
      return;
    }
    fetchPath();
  }, [userId, activeGoal, navigate]);

  if (loading) {
    return <div className="flex h-[50vh] items-center justify-center"><LoadingSpinner size="lg" text="Generating your personalized path..." /></div>;
  }

  if (error || !path) {
    return (
      <div className="flex flex-col items-center justify-center h-[50vh] text-center max-w-lg mx-auto">
        <AlertCircle className="w-12 h-12 text-accent-rose mb-4" />
        <h2 className="text-xl font-semibold mb-2">Oops!</h2>
        <p className="text-surface-400 mb-6">{error}</p>
        <button onClick={() => navigate('/chat')} className="btn-primary py-2 px-6 rounded-xl">Talk to Pathfinder</button>
      </div>
    );
  }

  const milestones = Array.from(new Set(path.items.map(i => i.milestone_number))).sort((a,b) => a-b);

  return (
    <div className="max-w-4xl mx-auto animate-fade-in pb-20">
      <div className="glass-card p-6 mb-8 border-b-4 border-b-primary-500">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center mb-2">
              <Map className="w-6 h-6 mr-2 text-primary-400" />
              Your Learning Path
            </h1>
            <p className="text-surface-300">{path.overview_explanation || "A curated sequence of courses to achieve your goals."}</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-white">{path.estimated_weeks || 12}</div>
            <div className="text-sm text-surface-400">Estimated Weeks</div>
          </div>
        </div>
      </div>

      <div className="space-y-12 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-primary-500 before:via-accent-cyan before:to-surface-800">
        {milestones.map(milestone => {
          const mItems = path.items.filter(i => i.milestone_number === milestone).sort((a,b) => a.sequence_order - b.sequence_order);
          return (
            <div key={milestone} className="relative z-10 space-y-6">
              <div className="md:w-3/4 mx-auto">
                <MilestoneCard milestoneNumber={milestone} items={mItems} />
              </div>
              <div className="space-y-4 md:w-3/4 mx-auto pl-8 md:pl-12 border-l-2 border-surface-800">
                {mItems.map(item => (
                  <CourseCard key={item.id} item={item} onStatusUpdate={fetchPath} />
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default PathPage;
