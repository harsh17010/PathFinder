import React from 'react';

export const LoadingSpinner: React.FC<{ size?: 'sm' | 'md' | 'lg', text?: string }> = ({ size = 'md', text }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className={`${sizeClasses[size]} border-4 border-white/10 border-t-primary-500 rounded-full animate-spin`} />
      {text && <p className="text-surface-400 text-sm animate-pulse-soft">{text}</p>}
    </div>
  );
};
