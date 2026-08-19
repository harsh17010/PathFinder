import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { SkillRadarChart } from '../components/ui/SkillRadarChart';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Target, TrendingUp, BookOpen, Clock } from 'lucide-react';

const DashboardPage: React.FC = () => {
  const { userId, userProfile, activeGoal } = useUser();
  const navigate = useNavigate();
  const loading = false;
  const [targetSkills, setTargetSkills] = useState<{name: string, level: number}[]>([]);

  useEffect(() => {
    if (!userId) {
      navigate('/onboarding');
      return;
    }
    
    // Generate dummy target skills based on user current skills + 2
    if (userProfile && userProfile.skills) {
       const targets = userProfile.skills.map(s => ({
         name: s.skill_name,
         level: Math.min(5, s.proficiency_level + 2)
       }));
       setTargetSkills(targets);
    }
  }, [userId, navigate, userProfile]);

  if (!userProfile || loading) {
    return <div className="flex h-full items-center justify-center"><LoadingSpinner size="lg" /></div>;
  }

  const currentSkills = userProfile.skills.map(s => ({ name: s.skill_name, level: s.proficiency_level }));

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold mb-2">Welcome back, {userProfile.name.split(' ')[0]}!</h1>
          <p className="text-surface-400">Here's your learning progress overview.</p>
        </div>
        <button onClick={() => navigate('/path')} className="btn-primary py-2 px-4 rounded-lg text-sm font-semibold">
          View Learning Path
        </button>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2 glass-card p-6 flex flex-col">
          <h3 className="text-lg font-semibold mb-4 flex items-center"><Target className="w-5 h-5 mr-2 text-primary-400" /> Active Goal</h3>
          {activeGoal ? (
            <div className="flex-1 bg-surface-900/50 p-4 rounded-xl border border-surface-800">
              <p className="text-lg text-white font-medium mb-4">"{activeGoal.raw_text}"</p>
              <div className="flex space-x-4 text-sm text-surface-400">
                <span className="flex items-center"><Clock className="w-4 h-4 mr-1"/> {activeGoal.timeframe_weeks || 12} Weeks</span>
                <span className="flex items-center"><BookOpen className="w-4 h-4 mr-1"/> {activeGoal.hours_per_week || 5} hrs/week</span>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
              <p className="text-surface-400 mb-4">You don't have an active goal yet.</p>
              <button onClick={() => navigate('/chat')} className="btn-primary py-2 px-4 rounded-lg text-sm">Talk to Pathfinder</button>
            </div>
          )}
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center"><TrendingUp className="w-5 h-5 mr-2 text-accent-emerald" /> Skill Profile</h3>
          <div className="mt-2 -ml-4">
            <SkillRadarChart currentSkills={currentSkills} targetSkills={targetSkills} />
          </div>
        </div>
      </div>
      
      <div className="glass-card p-6">
        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
        <div className="text-center py-12 text-surface-400">
          No recent activity to show.
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
