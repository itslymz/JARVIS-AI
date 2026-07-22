import React, { useState, useRef, useEffect } from 'react';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import toast from 'react-hot-toast';
import Layout from '@/components/Layout';
import ChatMessage from '@/components/ChatMessage';
import ChatInput from '@/components/ChatInput';
import { useChat } from '@/hooks/useChat';

export default function ChatPage() {
  const { messages, isLoading, sendMessage } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    try {
      await sendMessage(content);
    } catch (error) {
      toast.error('Failed to send message');
    }
  };

  return (
    <>
      <Head>
        <title>Chat - JARVIS-AI</title>
      </Head>

      <Layout>
        <div className="flex flex-col h-screen bg-jarvis-dark">
          {/* Header */}
          <div className="border-b border-jarvis-accent/20 p-6 bg-jarvis-darker">
            <h1 className="text-2xl font-bold">
              <span className="text-jarvis-accent">Chat</span> with JARVIS
            </h1>
            <p className="text-gray-400 text-sm mt-1">Have a conversation with your AI assistant</p>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full text-center">
                <div>
                  <p className="text-gray-400 text-lg">No messages yet</p>
                  <p className="text-gray-500 text-sm mt-2">Start a conversation with JARVIS</p>
                </div>
              </div>
            ) : (
              <AnimatePresence>
                {messages.map((message, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    transition={{ duration: 0.3 }}
                  >
                    <ChatMessage message={message} />
                  </motion.div>
                ))}
              </AnimatePresence>
            )}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-2 text-jarvis-accent"
              >
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-jarvis-accent rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-jarvis-accent rounded-full animate-bounce delay-100" />
                  <div className="w-2 h-2 bg-jarvis-accent rounded-full animate-bounce delay-200" />
                </div>
                <span>JARVIS is thinking...</span>
              </motion.div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t border-jarvis-accent/20 p-6 bg-jarvis-darker">
            <ChatInput onSend={handleSendMessage} disabled={isLoading} />
          </div>
        </div>
      </Layout>
    </>
  );
}
