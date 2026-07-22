import React from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function Home() {
  const router = useRouter();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.3,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: 'easeOut' },
    },
  };

  return (
    <>
      <Head>
        <title>JARVIS-AI - Autonomous AI Operating System</title>
        <meta name="description" content="JARVIS-AI: Your personal AI assistant" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gradient-to-b from-jarvis-dark to-jarvis-darker flex flex-col items-center justify-center px-4">
        {/* Animated background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-jarvis-accent opacity-5 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-jarvis-gold opacity-5 rounded-full blur-3xl animate-pulse" />
        </div>

        {/* Content */}
        <motion.div
          className="relative z-10 text-center max-w-2xl"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Logo/Title */}
          <motion.h1 variants={itemVariants} className="text-6xl font-bold mb-4">
            <span className="text-jarvis-accent">JARVIS</span>
            <span className="text-jarvis-gold">-AI</span>
          </motion.h1>

          {/* Subtitle */}
          <motion.p variants={itemVariants} className="text-xl text-gray-300 mb-8">
            Autonomous AI Operating System
          </motion.p>

          {/* Description */}
          <motion.p variants={itemVariants} className="text-gray-400 mb-12 leading-relaxed">
            Experience the future of AI assistance. JARVIS-AI is a production-ready autonomous system that
            understands natural language, learns from experience, and helps you accomplish your goals.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div variants={itemVariants} className="flex gap-4 justify-center flex-wrap">
            <Link href="/dashboard">
              <button className="btn btn-primary text-lg px-8 py-3">
                Enter Dashboard
              </button>
            </Link>
            <Link href="/chat">
              <button className="btn btn-secondary text-lg px-8 py-3">
                Start Chat
              </button>
            </Link>
          </motion.div>

          {/* Features Grid */}
          <motion.div variants={itemVariants} className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                title: 'Natural Language',
                description: 'Understands and responds to natural language queries',
              },
              {
                title: 'Long-term Memory',
                description: 'Remembers conversations and learns your preferences',
              },
              {
                title: 'Autonomous',
                description: 'Executes tasks and improves continuously',
              },
            ].map((feature, idx) => (
              <div key={idx} className="card border border-jarvis-accent/30 hover:border-jarvis-accent/60 cursor-pointer">
                <h3 className="text-jarvis-accent font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-gray-400">{feature.description}</p>
              </div>
            ))}
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.footer
          variants={itemVariants}
          className="absolute bottom-6 text-center text-gray-500 text-sm"
        >
          <p>JARVIS-AI © 2024 | Built with ❤️ for autonomous intelligence</p>
        </motion.footer>
      </div>
    </>
  );
}
