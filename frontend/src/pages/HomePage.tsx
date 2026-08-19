import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, Route, LineChart } from 'lucide-react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center text-center px-4 animate-fade-in">
      <h1 className="text-5xl md:text-6xl font-bold mb-6">
        <span className="gradient-text">Your AI-Powered Learning</span>
        <br />
        <span className="text-white">Journey Starts Here</span>
      </h1>
      <p className="text-surface-300 text-xl max-w-2xl mb-12 animate-slide-up">
        Discover your personalized learning path with AI-curated course recommendations tailored to your goals.
      </p>

      <div className="grid md:grid-cols-3 gap-6 w-full max-w-5xl mb-16">
        <div className="glass-card p-8 flex flex-col items-center animate-slide-up" style={{ animationDelay: '0.1s' }}>
          <Route className="w-12 h-12 text-primary-400 mb-4" />
          <h3 className="text-xl font-semibold mb-2">Personalized Paths</h3>
          <p className="text-surface-300">Custom learning journeys based on your skills and career goals.</p>
        </div>
        <div className="glass-card p-8 flex flex-col items-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
          <Sparkles className="w-12 h-12 text-accent-cyan mb-4" />
          <h3 className="text-xl font-semibold mb-2">AI Explanations</h3>
          <p className="text-surface-300">Understand exactly why each course was recommended for you.</p>
        </div>
        <div className="glass-card p-8 flex flex-col items-center animate-slide-up" style={{ animationDelay: '0.3s' }}>
          <LineChart className="w-12 h-12 text-accent-emerald mb-4" />
          <h3 className="text-xl font-semibold mb-2">Progress Tracking</h3>
          <p className="text-surface-300">Monitor your milestones and adjust your path as you learn.</p>
        </div>
      </div>

      <Link to="/chat" className="btn-primary flex items-center gap-2 text-lg animate-slide-up" style={{ animationDelay: '0.4s' }}>
        <Sparkles className="w-5 h-5" />
        Start Your Journey
      </Link>
    </div>
  );
};

export default HomePage;
