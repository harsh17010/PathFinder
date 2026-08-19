import React from 'react';

interface DifficultyBadgeProps {
  level: string;
}

export const DifficultyBadge: React.FC<DifficultyBadgeProps> = ({ level }) => {
  const normalized = level.toLowerCase();
  
  let colors = 'bg-surface-800 text-surface-300';
  if (normalized === 'beginner') colors = 'bg-accent-emerald/20 text-accent-emerald border-accent-emerald/30';
  if (normalized === 'intermediate') colors = 'bg-accent-amber/20 text-accent-amber border-accent-amber/30';
  if (normalized === 'advanced') colors = 'bg-accent-rose/20 text-accent-rose border-accent-rose/30';

  return (
    <span className={`text-xs px-2 py-1 rounded-full border uppercase tracking-wider font-semibold ${colors}`}>
      {level}
    </span>
  );
};
