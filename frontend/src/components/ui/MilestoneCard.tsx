import React from 'react';
import type { PathItemDetail } from '../../types';
import { CheckCircle2, Circle, PlayCircle } from 'lucide-react';

interface MilestoneCardProps {
  milestoneNumber: number;
  items: PathItemDetail[];
}

export const MilestoneCard: React.FC<MilestoneCardProps> = ({ milestoneNumber, items }) => {
  const total = items.length;
  const completed = items.filter(i => i.status === 'completed').length;
  const inProgress = items.some(i => i.status === 'in_progress');
  
  const isCompleted = total > 0 && completed === total;
  const isActive = !isCompleted && (inProgress || items.some(i => i.status === 'available'));
  
  let statusIcon = <Circle className="w-6 h-6 text-surface-600" />;
  let borderClass = 'border-surface-800';
  
  if (isCompleted) {
    statusIcon = <CheckCircle2 className="w-6 h-6 text-accent-emerald" />;
    borderClass = 'border-accent-emerald/50 bg-accent-emerald/5';
  } else if (isActive) {
    statusIcon = <PlayCircle className="w-6 h-6 text-primary-400" />;
    borderClass = 'border-primary-500/50 bg-primary-500/10 shadow-[0_0_15px_rgba(99,102,241,0.1)]';
  }

  const progressPercent = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className={`glass-card p-4 border ${borderClass} flex items-center space-x-4 transition-all duration-300`}>
      <div className="flex-shrink-0">
        {statusIcon}
      </div>
      <div className="flex-1">
        <h3 className="text-lg font-semibold text-white mb-1">Milestone {milestoneNumber}</h3>
        <div className="flex items-center space-x-2 text-sm text-surface-400">
          <span>{completed} of {total} courses completed</span>
        </div>
        <div className="w-full bg-surface-800 rounded-full h-1.5 mt-2 overflow-hidden">
          <div 
            className={`h-1.5 rounded-full transition-all duration-500 ${isCompleted ? 'bg-accent-emerald' : 'bg-primary-500'}`}
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>
    </div>
  );
};
