import React, { useState } from 'react';
import type { PathItemDetail } from '../../types';
import { DifficultyBadge } from './DifficultyBadge';
import { Clock, Star, ThumbsUp, ChevronDown, ChevronUp, X, Check, Lock, Play } from 'lucide-react';
import { api } from '../../services/api';
import { useUser } from '../../context/UserContext';

interface CourseCardProps {
  item: PathItemDetail;
  onStatusUpdate?: () => void;
}

export const CourseCard: React.FC<CourseCardProps> = ({ item, onStatusUpdate }) => {
  const { userId } = useUser();
  const [isExpanded, setIsExpanded] = useState(false);
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  
  const statusColors = {
    locked: 'border-surface-800 opacity-50',
    available: 'border-primary-500/50 bg-primary-900/10',
    in_progress: 'border-accent-amber/50 bg-accent-amber/10',
    completed: 'border-accent-emerald/50 bg-accent-emerald/10',
  };

  const handleFeedback = async (type: string) => {
    if (!userId || submittingFeedback) return;
    setSubmittingFeedback(true);
    try {
      await api.sendFeedback({ user_id: userId, path_item_id: item.id, feedback_type: type });
      alert('Feedback submitted!');
    } catch (e) {
      console.error(e);
      alert('Failed to submit feedback');
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const handleStatusChange = async (newStatus: string) => {
    try {
      await api.updateItemStatus(item.id, newStatus);
      if (onStatusUpdate) onStatusUpdate();
    } catch (e) {
      console.error(e);
      alert('Failed to update status');
    }
  };

  return (
    <div className={`glass-card p-4 transition-all duration-300 border-l-4 ${statusColors[item.status]}`}>
      <div className="flex justify-between items-start cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-1">
            {item.status === 'completed' && <Check className="w-4 h-4 text-accent-emerald" />}
            {item.status === 'locked' && <Lock className="w-4 h-4 text-surface-500" />}
            {item.status === 'in_progress' && <Play className="w-4 h-4 text-accent-amber" />}
            <h4 className="text-lg font-semibold text-white">{item.course_title}</h4>
          </div>
          <p className="text-sm text-surface-400 mb-2">{item.course_provider}</p>
          <div className="flex flex-wrap gap-2 items-center">
            {item.course_difficulty && <DifficultyBadge level={item.course_difficulty} />}
            {item.course_duration_hours && (
              <span className="flex items-center text-xs text-surface-400">
                <Clock className="w-3 h-3 mr-1" /> {item.course_duration_hours}h
              </span>
            )}
            {item.course_rating && (
              <span className="flex items-center text-xs text-accent-amber">
                <Star className="w-3 h-3 mr-1" /> {item.course_rating}
              </span>
            )}
          </div>
        </div>
      </div>
      
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-white/10 animate-fade-in">
          <p className="text-sm text-surface-300 mb-4">{item.course_description}</p>
          {item.explanation_text && (
            <div className="bg-white/5 p-3 rounded-lg mb-4 text-sm text-primary-200">
              <span className="font-semibold block mb-1">Why this course?</span>
              {item.explanation_text}
            </div>
          )}
          
          <div className="flex flex-wrap items-center justify-between gap-4 mt-4">
            <div className="flex space-x-2">
              {item.status === 'available' && (
                <button onClick={(e) => { e.stopPropagation(); handleStatusChange('in_progress'); }} className="btn-primary text-xs py-1 px-3">
                  Start Course
                </button>
              )}
              {item.status === 'in_progress' && (
                <button onClick={(e) => { e.stopPropagation(); handleStatusChange('completed'); }} className="bg-accent-emerald text-surface-950 px-3 py-1 rounded-lg text-xs font-semibold hover:bg-accent-emerald/90 transition-colors">
                  Mark Completed
                </button>
              )}
            </div>
            
            {(item.status === 'available' || item.status === 'in_progress') && (
              <div className="flex space-x-1">
                <button onClick={(e) => { e.stopPropagation(); handleFeedback('helpful'); }} disabled={submittingFeedback} className="p-2 rounded-lg bg-surface-800 hover:bg-surface-700 text-surface-300 transition-colors tooltip" title="Helpful">
                  <ThumbsUp className="w-4 h-4" />
                </button>
                <button onClick={(e) => { e.stopPropagation(); handleFeedback('too_easy'); }} disabled={submittingFeedback} className="p-2 rounded-lg bg-surface-800 hover:bg-surface-700 text-surface-300 transition-colors tooltip" title="Too Easy">
                  <ChevronDown className="w-4 h-4" />
                </button>
                <button onClick={(e) => { e.stopPropagation(); handleFeedback('too_hard'); }} disabled={submittingFeedback} className="p-2 rounded-lg bg-surface-800 hover:bg-surface-700 text-surface-300 transition-colors tooltip" title="Too Hard">
                  <ChevronUp className="w-4 h-4" />
                </button>
                <button onClick={(e) => { e.stopPropagation(); handleFeedback('not_relevant'); }} disabled={submittingFeedback} className="p-2 rounded-lg bg-surface-800 hover:bg-surface-700 text-surface-300 transition-colors tooltip" title="Not Relevant">
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
