import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useUser } from '../../context/UserContext';
import { Compass, User, LogOut } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { userProfile, logout } = useUser();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard' },
    { name: 'Path', path: '/path' },
    { name: 'Chat', path: '/chat' },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-surface-950/80 backdrop-blur-lg border-b border-white/5">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Compass className="w-8 h-8 text-primary-500" />
            <span className="text-xl font-bold gradient-text">Pathfinder</span>
          </Link>

          <div className="flex items-center space-x-8">
            {userProfile ? (
              <>
                <div className="hidden md:flex space-x-6">
                  {navLinks.map((link) => (
                    <Link
                      key={link.path}
                      to={link.path}
                      className={`text-sm font-medium transition-colors hover:text-white ${
                        location.pathname === link.path ? 'text-white border-b-2 border-primary-500 pb-1' : 'text-surface-400'
                      }`}
                    >
                      {link.name}
                    </Link>
                  ))}
                </div>
                <div className="flex items-center space-x-4 border-l border-white/10 pl-6">
                  <div className="flex items-center space-x-2 text-surface-300">
                    <div className="w-8 h-8 rounded-full bg-primary-900/50 flex items-center justify-center border border-primary-500/30">
                      <User className="w-4 h-4 text-primary-400" />
                    </div>
                    <span className="text-sm font-medium hidden sm:block">{userProfile.name}</span>
                  </div>
                  <button onClick={handleLogout} className="text-surface-500 hover:text-white transition-colors">
                    <LogOut className="w-5 h-5" />
                  </button>
                </div>
              </>
            ) : (
              <Link to="/onboarding" className="btn-primary py-2 px-4 rounded-lg text-sm font-semibold">
                Get Started
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
