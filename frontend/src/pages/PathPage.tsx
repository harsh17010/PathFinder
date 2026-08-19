import React from 'react';
import { BookOpen, CheckCircle, Lock, ArrowRight } from 'lucide-react';

const PathPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto p-4 animate-fade-in">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold mb-2">Frontend Engineering Path</h1>
          <p className="text-surface-300">Target Role: Senior React Developer</p>
        </div>
        <div className="px-4 py-2 bg-primary-500/10 border border-primary-500/20 rounded-lg text-primary-300 text-sm font-medium">
          Coming in Phase 2
        </div>
      </div>

      <div className="space-y-6 relative before:absolute before:inset-0 before:ml-6 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-primary-500 before:via-surface-700 before:to-surface-800">
        
        {/* Completed Item */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
          <div className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-surface-950 bg-accent-emerald text-surface-950 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_0_4px_#020617] z-10">
            <CheckCircle className="w-5 h-5" />
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] glass-card p-6 border-accent-emerald/20">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-accent-emerald uppercase tracking-wider">Completed</span>
            </div>
            <h3 className="text-lg font-bold mb-2">React Fundamentals</h3>
            <p className="text-surface-300 text-sm mb-4">Master components, props, state, and hooks.</p>
            <div className="p-3 bg-surface-900/50 rounded-lg text-xs text-surface-400 border border-white/5">
              <span className="text-primary-300 font-medium">AI Note:</span> You breezed through this since you already had some JS experience!
            </div>
          </div>
        </div>

        {/* Current Item */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
          <div className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-surface-950 bg-primary-500 text-white shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_0_4px_#020617] z-10 shadow-primary-500/50">
            <BookOpen className="w-5 h-5" />
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] glass-card p-6 border-primary-500/50 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary-400 to-accent-cyan"></div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-primary-400 uppercase tracking-wider">In Progress</span>
            </div>
            <h3 className="text-lg font-bold mb-2">Advanced State Management</h3>
            <p className="text-surface-300 text-sm mb-4">Learn Redux Toolkit and Zustand for global state.</p>
            <button className="w-full btn-primary py-2 text-sm flex items-center justify-center gap-2">
              Continue Learning <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Locked Item */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
          <div className="flex items-center justify-center w-12 h-12 rounded-full border-4 border-surface-950 bg-surface-800 text-surface-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-[0_0_0_4px_#020617] z-10">
            <Lock className="w-5 h-5" />
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-3rem)] glass-card p-6 opacity-60">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-semibold text-surface-500 uppercase tracking-wider">Locked</span>
            </div>
            <h3 className="text-lg font-bold text-surface-400 mb-2">Performance Optimization</h3>
            <p className="text-surface-500 text-sm">Code splitting, memoization, and rendering optimization.</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default PathPage;
