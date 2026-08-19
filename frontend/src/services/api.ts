import type { Course, FeedbackEvent } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return response.json();
}

// Export typed API functions for each endpoint
export const api = {
  // Users
  createUser: (data: { name: string; email: string }) => fetchAPI('/users', { method: 'POST', body: JSON.stringify(data) }),
  
  // Courses
  getCourses: () => fetchAPI<Course[]>('/courses'),
  searchCourses: (query: string) => fetchAPI('/courses/search', { method: 'POST', body: JSON.stringify({ query }) }),
  
  // Goals
  createGoal: (userId: string, data: any) => fetchAPI('/goals', { method: 'POST', body: JSON.stringify({ user_id: userId, ...data }) }),
  
  // Paths
  getUserPaths: (userId: string) => fetchAPI(`/paths/${userId}`),
  
  // Chat
  sendMessage: (userId: string, message: string, sessionId: string) => 
    fetchAPI('/chat', { method: 'POST', body: JSON.stringify({ user_id: userId, message, session_id: sessionId }) }),
  
  // Feedback
  sendFeedback: (data: FeedbackEvent & { user_id: string }) => 
    fetchAPI('/feedback', { method: 'POST', body: JSON.stringify(data) }),
};
