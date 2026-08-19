import React from 'react';
import { Target, Trophy, Flame } from 'lucide-react';
import { ResponsiveContainer, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';

const dummySkillData = [
  { subject: 'React', A: 80, fullMark: 100 },
  { subject: 'TypeScript', A: 65, fullMark: 100 },
  { subject: 'Node.js', A: 45, fullMark: 100 },
  { subject: 'CSS', A: 90, fullMark: 100 },
  { subject: 'Python', A: 30, fullMark: 100 },
];

const DashboardPage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto p-4 animate-fade-in">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Your Dashboard</h1>
          <p className="text-surface-300">Track your progress and skills</p>
        </div>
        <div className="px-4 py-2 bg-primary-500/10 border border-primary-500/20 rounded-lg text-primary-300 text-sm font-medium">
          Coming in Phase 2
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        {/* Stats */}
        <div className="md:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-card p-6 flex items-center gap-4">
            <div className="p-4 bg-accent-emerald/20 rounded-xl text-accent-emerald">
              <Target className="w-8 h-8" />
            </div>
            <div>
              <p className="text-surface-400 text-sm">Active Goals</p>
              <p className="text-2xl font-bold">2</p>
            </div>
          </div>
          <div className="glass-card p-6 flex items-center gap-4">
            <div className="p-4 bg-accent-cyan/20 rounded-xl text-accent-cyan">
              <Trophy className="w-8 h-8" />
            </div>
            <div>
              <p className="text-surface-400 text-sm">Milestones Met</p>
              <p className="text-2xl font-bold">7</p>
            </div>
          </div>
          <div className="glass-card p-6 flex items-center gap-4">
            <div className="p-4 bg-accent-amber/20 rounded-xl text-accent-amber">
              <Flame className="w-8 h-8" />
            </div>
            <div>
              <p className="text-surface-400 text-sm">Current Streak</p>
              <p className="text-2xl font-bold">5 Days</p>
            </div>
          </div>
        </div>

        {/* Radar Chart */}
        <div className="md:col-span-2 glass-card p-6 min-h-[400px] flex flex-col">
          <h2 className="text-xl font-semibold mb-6">Skill Profile</h2>
          <div className="flex-1 w-full relative">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="70%" data={dummySkillData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8' }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar name="Skills" dataKey="A" stroke="#06b6d4" fill="#06b6d4" fillOpacity={0.4} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Next Actions */}
        <div className="glass-card p-6">
          <h2 className="text-xl font-semibold mb-6">Up Next</h2>
          <div className="space-y-4">
            <div className="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-primary-500/50 transition-colors cursor-pointer">
              <p className="text-xs text-primary-400 font-medium mb-1">Module 3</p>
              <p className="text-sm font-semibold mb-2">Advanced State Management</p>
              <div className="w-full bg-surface-800 rounded-full h-1.5">
                <div className="bg-gradient-to-r from-primary-500 to-accent-cyan h-1.5 rounded-full" style={{ width: '45%' }}></div>
              </div>
            </div>
            <div className="p-4 bg-white/5 rounded-xl border border-white/10 hover:border-primary-500/50 transition-colors cursor-pointer opacity-50">
              <p className="text-xs text-surface-400 font-medium mb-1">Module 4</p>
              <p className="text-sm font-semibold">Performance Optimization</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
