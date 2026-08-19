import React, { createContext, useContext, useEffect, useState } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';
import type { UserProfile, Goal } from '../types';
import { api } from '../services/api';

interface UserContextType {
  userId: string | null;
  sessionId: string | null;
  userProfile: UserProfile | null;
  activeGoal: Goal | null;
  setUserId: (id: string | null) => void;
  setSessionId: (id: string | null) => void;
  setUserProfile: (profile: UserProfile | null) => void;
  setActiveGoal: (goal: Goal | null) => void;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [userId, setUserId] = useLocalStorage<string | null>('pathfinder_user_id', null);
  const [sessionId, setSessionId] = useLocalStorage<string | null>('pathfinder_session_id', null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [activeGoal, setActiveGoal] = useState<Goal | null>(null);

  const refreshProfile = async () => {
    if (!userId) return;
    try {
      const profile = await api.getProfile(userId);
      setUserProfile(profile);
      if (profile.goals && profile.goals.length > 0) {
        setActiveGoal(profile.goals.find(g => g.status === 'active') || profile.goals[0]);
      }
    } catch (error) {
      console.error("Failed to fetch user profile:", error);
    }
  };

  useEffect(() => {
    if (userId) {
      refreshProfile();
    }
  }, [userId]);

  const logout = () => {
    setUserId(null);
    setSessionId(null);
    setUserProfile(null);
    setActiveGoal(null);
  };

  return (
    <UserContext.Provider value={{ userId, sessionId, userProfile, activeGoal, setUserId, setSessionId, setUserProfile, setActiveGoal, logout, refreshProfile }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
