import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';

interface SkillRadarProps {
  currentSkills: { name: string; level: number }[];
  targetSkills: { name: string; level: number }[];
}

export const SkillRadarChart: React.FC<SkillRadarProps> = ({ currentSkills, targetSkills }) => {
  // Merge current and target skills by name
  const allNames = Array.from(new Set([...currentSkills.map(s => s.name), ...targetSkills.map(s => s.name)]));
  
  const data = allNames.map(name => {
    const current = currentSkills.find(s => s.name === name)?.level || 0;
    const target = targetSkills.find(s => s.name === name)?.level || 0;
    return {
      skill: name,
      Current: current,
      Target: target,
      fullMark: 5,
    };
  });

  return (
    <div className="w-full h-80">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="skill" tick={{ fill: '#94a3b8', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 5]} tick={{ fill: '#475569' }} />
          <Radar name="Current Skills" dataKey="Current" stroke="#6366f1" fill="#6366f1" fillOpacity={0.5} />
          <Radar name="Target Profile" dataKey="Target" stroke="#10b981" fill="#10b981" fillOpacity={0.3} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '0.5rem' }}
            itemStyle={{ color: '#e2e8f0' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};
