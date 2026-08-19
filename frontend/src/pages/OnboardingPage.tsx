import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';
import { useUser } from '../context/UserContext';
import type { Skill } from '../types';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { ChevronRight, Target, Sparkles, Code, CheckCircle2 } from 'lucide-react';

const OnboardingPage: React.FC = () => {
  const navigate = useNavigate();
  const { setUserId } = useUser();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Data
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [skills, setSkills] = useState<Skill[]>([]);
  const [tracks, setTracks] = useState<string[]>([]);
  
  // Selections
  const [selectedTracks, setSelectedTracks] = useState<string[]>([]);
  const [skillLevels, setSkillLevels] = useState<Record<string, number>>({});
  const [goalText, setGoalText] = useState('');

  useEffect(() => {
    if (step === 2 && tracks.length === 0) {
      const loadInitialData = async () => {
        setLoading(true);
        try {
          const [fetchedSkills, fetchedTracks] = await Promise.all([
            api.getSkills(),
            api.getTracks()
          ]);
          setSkills(fetchedSkills);
          setTracks(fetchedTracks);
        } catch (e) {
          setError('Failed to load initial data');
        } finally {
          setLoading(false);
        }
      };
      loadInitialData();
    }
  }, [step]);

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const selectedSkills = Object.entries(skillLevels).map(([skill_name, proficiency_level]) => ({
        skill_name,
        proficiency_level
      }));
      
      const data = {
        name,
        email,
        skills: selectedSkills,
        interests: selectedTracks,
        goal_text: goalText
      };
      
      const response = await api.onboard(data);
      setUserId(response.user.id);
      navigate('/chat');
    } catch (e: any) {
      setError(e.message || 'Onboarding failed');
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (step === 1 && (!name || !email)) {
      setError('Please fill in your name and email');
      return;
    }
    if (step === 2 && selectedTracks.length === 0) {
      setError('Please select at least one track');
      return;
    }
    setError('');
    if (step < 4) setStep(step + 1);
    else handleSubmit();
  };

  return (
    <div className="max-w-2xl mx-auto w-full">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {[1, 2, 3, 4].map(s => (
            <div key={s} className={`flex-1 h-2 rounded-full mx-1 ${s <= step ? 'bg-primary-500' : 'bg-surface-800'}`} />
          ))}
        </div>
        <div className="mt-4 text-center">
          <h2 className="text-2xl font-bold text-white mb-2">
            {step === 1 && "Let's get to know you"}
            {step === 2 && "What are you interested in?"}
            {step === 3 && "Assess your current skills"}
            {step === 4 && "What is your main goal?"}
          </h2>
        </div>
      </div>

      <div className="glass-card p-6 md:p-8 relative min-h-[400px] flex flex-col">
        {error && (
          <div className="bg-accent-rose/20 text-accent-rose p-3 rounded-lg text-sm mb-6 border border-accent-rose/30">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex-1 flex items-center justify-center">
            <LoadingSpinner size="lg" text="Setting things up..." />
          </div>
        ) : (
          <div className="flex-1 animate-fade-in flex flex-col justify-center">
            {step === 1 && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-surface-300 mb-2">Full Name</label>
                  <input type="text" className="input-field" value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Jane Doe" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-surface-300 mb-2">Email Address</label>
                  <input type="email" className="input-field" value={email} onChange={e => setEmail(e.target.value)} placeholder="jane@example.com" />
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {tracks.map(track => (
                  <button
                    key={track}
                    onClick={() => {
                      if (selectedTracks.includes(track)) setSelectedTracks(selectedTracks.filter(t => t !== track));
                      else setSelectedTracks([...selectedTracks, track]);
                    }}
                    className={`p-4 rounded-xl border text-left transition-all ${
                      selectedTracks.includes(track)
                        ? 'border-primary-500 bg-primary-500/20 shadow-[0_0_15px_rgba(99,102,241,0.2)]'
                        : 'border-surface-700 bg-surface-800/50 hover:bg-surface-800'
                    }`}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <Code className={`w-6 h-6 ${selectedTracks.includes(track) ? 'text-primary-400' : 'text-surface-400'}`} />
                      {selectedTracks.includes(track) && <CheckCircle2 className="w-5 h-5 text-primary-400" />}
                    </div>
                    <span className="font-medium text-white">{track}</span>
                  </button>
                ))}
              </div>
            )}

            {step === 3 && (
              <div className="space-y-8 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {selectedTracks.map(track => (
                  <div key={track} className="space-y-4">
                    <h3 className="text-lg font-semibold text-primary-300">{track}</h3>
                    {skills.filter(s => s.track === track).map(skill => (
                      <div key={skill.id} className="bg-surface-900/50 p-4 rounded-xl border border-surface-800">
                        <div className="flex justify-between mb-2">
                          <label className="text-sm font-medium text-white">{skill.name}</label>
                          <span className="text-xs text-primary-400 font-semibold">{skillLevels[skill.name] || 0} / 5</span>
                        </div>
                        <input
                          type="range"
                          min="0"
                          max="5"
                          step="1"
                          value={skillLevels[skill.name] || 0}
                          onChange={e => setSkillLevels({...skillLevels, [skill.name]: parseInt(e.target.value)})}
                          className="w-full accent-primary-500 h-2 bg-surface-700 rounded-lg appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-xs text-surface-500 mt-2">
                          <span>Novice</span>
                          <span>Expert</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            )}

            {step === 4 && (
              <div className="space-y-4">
                <Target className="w-12 h-12 text-primary-400 mb-4 mx-auto" />
                <p className="text-surface-300 text-center mb-6">Describe what you want to achieve in 1-2 sentences.</p>
                <textarea
                  className="input-field min-h-[120px] resize-none"
                  placeholder="e.g., I want to become a Senior React Developer and master state management and performance optimization."
                  value={goalText}
                  onChange={e => setGoalText(e.target.value)}
                />
              </div>
            )}
          </div>
        )}

        <div className="mt-8 flex justify-end">
          <button
            onClick={handleNext}
            disabled={loading}
            className="btn-primary py-3 px-8 rounded-xl font-semibold flex items-center space-x-2"
          >
            <span>{step === 4 ? 'Complete Setup' : 'Continue'}</span>
            {step === 4 ? <Sparkles className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;
