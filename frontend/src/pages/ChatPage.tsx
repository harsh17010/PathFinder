import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { api } from '../services/api';
import type { ChatMessage } from '../types';
import { Send, User, Compass } from 'lucide-react';

const ChatPage: React.FC = () => {
  const { userId, sessionId, setSessionId, userProfile } = useUser();
  const navigate = useNavigate();
  
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!userId) {
      navigate('/onboarding');
      return;
    }
    
    // Initial welcome message if no messages
    if (messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          role: 'assistant',
          content: `Hi ${userProfile?.name || 'there'}! I'm Pathfinder. I can help you find the right courses or generate a personalized learning path. What would you like to learn today?`,
          created_at: new Date().toISOString()
        }
      ]);
    }
  }, [userId, navigate, messages.length, userProfile]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!input.trim() || !userId || loading) return;
    
    const userMsg: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      created_at: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    
    try {
      const response = await api.sendMessage(userId, userMsg.content, sessionId || undefined);
      if (response.session_id && response.session_id !== sessionId) {
        setSessionId(response.session_id);
      }
      
      const assistantMsg: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.reply,
        created_at: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, assistantMsg]);
      
      if (response.actions_taken && response.actions_taken.includes('generate_path')) {
        setTimeout(() => navigate('/path'), 2000);
      }
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        created_at: new Date().toISOString()
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-8rem)]">
      <div className="flex-1 overflow-y-auto pr-4 custom-scrollbar space-y-6 pb-6">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`flex max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                msg.role === 'user' ? 'bg-primary-600 ml-3' : 'bg-surface-800 border border-white/10 mr-3'
              }`}>
                {msg.role === 'user' ? <User className="w-4 h-4 text-white" /> : <Compass className="w-4 h-4 text-primary-400" />}
              </div>
              <div className={`p-4 ${
                msg.role === 'user' ? 'bg-primary-600 text-white rounded-2xl rounded-tr-none' : 'glass-card rounded-2xl rounded-tl-none'
              }`}>
                <p className="whitespace-pre-wrap text-sm md:text-base">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="flex flex-row max-w-[80%]">
              <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-surface-800 border border-white/10 mr-3">
                <Compass className="w-4 h-4 text-primary-400" />
              </div>
              <div className="glass-card rounded-2xl rounded-tl-none p-4 flex space-x-2 items-center h-12">
                <div className="w-2 h-2 bg-surface-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                <div className="w-2 h-2 bg-surface-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                <div className="w-2 h-2 bg-surface-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="mt-4 bg-surface-900/50 p-2 rounded-2xl border border-surface-800 flex items-end">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="Ask me anything..."
          className="flex-1 bg-transparent border-none focus:ring-0 resize-none max-h-32 text-sm md:text-base p-3 text-white placeholder-surface-500"
          rows={1}
          style={{ minHeight: '44px' }}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="m-2 p-3 bg-primary-600 hover:bg-primary-500 disabled:opacity-50 disabled:hover:bg-primary-600 rounded-xl text-white transition-colors"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatPage;
