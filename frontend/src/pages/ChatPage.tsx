import React from 'react';
import { Send, User, Bot, AlertCircle } from 'lucide-react';

const ChatPage: React.FC = () => {
  return (
    <div className="flex h-[calc(100vh-6rem)] gap-6 p-4 animate-fade-in">
      {/* Sidebar Placeholder */}
      <div className="hidden md:flex w-64 glass-card p-4 flex-col gap-4">
        <h2 className="text-lg font-semibold text-white/90">History</h2>
        <div className="space-y-2">
          <div className="p-3 bg-white/5 rounded-lg text-sm text-surface-300">Front-end Basics</div>
          <div className="p-3 bg-white/5 rounded-lg text-sm text-surface-300">Advanced React Path</div>
        </div>
        <div className="mt-auto p-4 bg-primary-900/50 border border-primary-500/20 rounded-xl flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-primary-400 shrink-0" />
          <p className="text-xs text-primary-200">Conversation history coming in Phase 2</p>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 glass-card flex flex-col relative overflow-hidden">
        {/* Chat Messages Placeholder */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="flex gap-4">
            <div className="w-10 h-10 rounded-full bg-primary-600/20 flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5 text-primary-400" />
            </div>
            <div className="glass-card p-4 rounded-tl-none max-w-2xl">
              <p className="text-surface-100">Hello! I'm Pathfinder. What are your learning goals for today?</p>
            </div>
          </div>
          
          <div className="flex gap-4 flex-row-reverse">
            <div className="w-10 h-10 rounded-full bg-surface-700 flex items-center justify-center shrink-0">
              <User className="w-5 h-5 text-surface-300" />
            </div>
            <div className="bg-primary-600 p-4 rounded-2xl rounded-tr-none max-w-2xl">
              <p className="text-white">I want to learn modern React and Tailwind CSS.</p>
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="p-4 bg-surface-900/50 border-t border-white/5">
          <div className="relative">
            <input
              type="text"
              placeholder="Type your message..."
              className="w-full input-field pr-12"
              disabled
            />
            <button className="absolute right-2 top-2 p-2 bg-primary-600 hover:bg-primary-500 rounded-lg text-white transition-colors disabled:opacity-50">
              <Send className="w-4 h-4" />
            </button>
          </div>
          <p className="text-center text-xs text-surface-400 mt-2">Chat functionality coming in Phase 2</p>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
