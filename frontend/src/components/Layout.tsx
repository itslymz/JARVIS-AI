import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Layout({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/chat', label: 'Chat', icon: '💬' },
    { href: '/memory', label: 'Memory', icon: '🧠' },
    { href: '/settings', label: 'Settings', icon: '⚙️' },
  ];

  return (
    <div className="flex h-screen bg-jarvis-dark">
      {/* Sidebar */}
      <div className="w-64 bg-jarvis-darker border-r border-jarvis-accent/20 flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-jarvis-accent/20">
          <h1 className="text-2xl font-bold">
            <span className="text-jarvis-accent">J</span>
            <span className="text-jarvis-gold">AI</span>
          </h1>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-6 space-y-2">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <div
                className={`flex items-center gap-3 px-4 py-3 rounded transition ${
                  router.pathname === item.href
                    ? 'bg-jarvis-accent/20 text-jarvis-accent border border-jarvis-accent/50'
                    : 'text-gray-400 hover:text-jarvis-accent hover:bg-jarvis-dark/50'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span>{item.label}</span>
              </div>
            </Link>
          ))}
        </nav>

        {/* Footer */}
        <div className="p-6 border-t border-jarvis-accent/20 text-sm text-gray-500">
          <p>JARVIS-AI v0.1.0</p>
          <p className="mt-2">Built with ❤️</p>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {children}
      </div>
    </div>
  );
}
