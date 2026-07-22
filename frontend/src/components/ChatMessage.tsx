import React from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export default function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
          isUser
            ? 'bg-jarvis-accent/20 border border-jarvis-accent/50 text-white'
            : 'bg-jarvis-darker border border-jarvis-accent/20 text-gray-300'
        }`}
      >
        <p className="text-sm leading-relaxed">{message.content}</p>
        {message.timestamp && (
          <p className="text-xs text-gray-500 mt-1">
            {new Date(message.timestamp).toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}
