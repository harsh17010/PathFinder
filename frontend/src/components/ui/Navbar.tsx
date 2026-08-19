import React from 'react';
import { NavLink } from 'react-router-dom';
import { Compass, Home, MessageSquare, LayoutDashboard, Map } from 'lucide-react';

const Navbar: React.FC = () => {
  return (
    <nav className="sticky top-0 z-50 w-full glass-card rounded-none border-t-0 border-x-0 border-b-white/10 px-4 py-3">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2 group">
          <div className="p-2 bg-primary-600/20 rounded-xl group-hover:bg-primary-600/30 transition-colors">
            <Compass className="w-6 h-6 text-primary-400" />
          </div>
          <span className="text-xl font-bold tracking-tight gradient-text">Pathfinder</span>
        </NavLink>

        <div className="flex items-center gap-1 md:gap-2">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive ? 'bg-white/10 text-white' : 'text-surface-300 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <Home className="w-4 h-4" />
            <span className="hidden md:inline">Home</span>
          </NavLink>
          
          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive ? 'bg-white/10 text-white' : 'text-surface-300 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <MessageSquare className="w-4 h-4" />
            <span className="hidden md:inline">Chat</span>
          </NavLink>
          
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive ? 'bg-white/10 text-white' : 'text-surface-300 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <LayoutDashboard className="w-4 h-4" />
            <span className="hidden md:inline">Dashboard</span>
          </NavLink>
          
          <NavLink
            to="/path"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive ? 'bg-white/10 text-white' : 'text-surface-300 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <Map className="w-4 h-4" />
            <span className="hidden md:inline">Path</span>
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
