import type { Course, UserProfile, Skill, CourseRecommendation, LearningPathDetail, OnboardingData, ChatResponse, Goal } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error: ${response.status} - ${text}`);
  }
  return response.json();
}

export const api = {
  // Users
  onboard: (data: OnboardingData) => fetchAPI<{ user: UserProfile; goal: Goal }>('/users/onboard', { method: 'POST', body: JSON.stringify(data) }),
  getProfile: (userId: string) => fetchAPI<UserProfile>(`/users/${userId}/profile`),
  
  // Skills
  getSkills: () => fetchAPI<Skill[]>('/skills/'),
  getTracks: () => fetchAPI<string[]>('/skills/tracks'),
  
  // Courses
  getCourses: () => fetchAPI<Course[]>('/courses'),
  searchCourses: (query: string) => fetchAPI('/courses/search', { method: 'POST', body: JSON.stringify({ query }) }),
  
  // Recommendations & Paths
  generateRecommendations: (userId: string, goalId: string) => fetchAPI<CourseRecommendation[]>('/recommendations/generate', { method: 'POST', body: JSON.stringify({ user_id: userId, goal_id: goalId }) }),
  generatePath: (userId: string, goalId: string) => fetchAPI<LearningPathDetail>('/paths/generate', { method: 'POST', body: JSON.stringify({ user_id: userId, goal_id: goalId }) }),
  getPathDetail: (pathId: string) => fetchAPI<LearningPathDetail>(`/paths/${pathId}/detail`),
  updateItemStatus: (itemId: string, status: string) => fetchAPI(`/paths/items/${itemId}/status`, { method: 'PATCH', body: JSON.stringify({ status }) }),
  
  // Chat
  sendMessage: (userId: string, message: string, sessionId?: string) => 
    fetchAPI<ChatResponse>('/chat/', { method: 'POST', body: JSON.stringify({ user_id: userId, message, session_id: sessionId }) }),
  
  // Feedback
  sendFeedback: (data: { user_id: string; path_item_id: string; feedback_type: string }) => 
    fetchAPI('/feedback/', { method: 'POST', body: JSON.stringify(data) }),
};
