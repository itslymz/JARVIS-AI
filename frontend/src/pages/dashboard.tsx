import React from 'react';
import Head from 'next/head';
import Layout from '@/components/Layout';
import { motion } from 'framer-motion';

export default function Dashboard() {
  const stats = [
    { label: 'Conversations', value: '0' },
    { label: 'Messages', value: '0' },
    { label: 'Memories', value: '0' },
    { label: 'Tasks Completed', value: '0' },
  ];

  return (
    <>
      <Head>
        <title>Dashboard - JARVIS-AI</title>
      </Head>

      <Layout>
        <div className="p-6 space-y-6">
          {/* Welcome Section */}
          <div className="card border border-jarvis-accent/30">
            <h1 className="text-3xl font-bold mb-2">
              Welcome to <span className="text-jarvis-accent">JARVIS</span>
            </h1>
            <p className="text-gray-400">Your personal AI operating system</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {stats.map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className="card border border-jarvis-accent/20 hover:border-jarvis-accent/60 cursor-pointer"
              >
                <p className="text-gray-400 text-sm">{stat.label}</p>
                <p className="text-3xl font-bold text-jarvis-accent mt-2">{stat.value}</p>
              </motion.div>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="card border border-jarvis-accent/30">
            <h2 className="text-xl font-semibold mb-4 text-jarvis-accent">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { label: 'New Chat', icon: '💬' },
                { label: 'View Memories', icon: '🧠' },
                { label: 'Task History', icon: '📋' },
                { label: 'Settings', icon: '⚙️' },
              ].map((action, idx) => (
                <button
                  key={idx}
                  className="p-4 border border-jarvis-accent/20 rounded hover:border-jarvis-accent/60 hover:bg-jarvis-dark/50 transition"
                >
                  <span className="text-2xl block mb-2">{action.icon}</span>
                  <span className="text-sm">{action.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </Layout>
    </>
  );
}
