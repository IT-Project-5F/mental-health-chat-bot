import { useState } from 'react';
import type React from 'react';

/* Types and Interfaces */
interface ChatInputProps {
  sendMessage: (message: string) => void;
  responsePending?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ sendMessage, responsePending }) => {
  /* States */
  const [input, updateInput] = useState('');
  const sendable = input.trim() !== '' && !responsePending;

  /* Functions */
  const handleSend = () => {
    // Message cannot be sent if it is blank or a response from Chatbot is pending
    if (input.trim() === '' || responsePending) return;
    // Call parent function to send the message
    sendMessage(input);
    // Chat input is cleared after message is sent
    updateInput('');
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };


  /* Rendering */
  return (
    <div className="p-4 bg-[#013F2D] border-t border-gray-700">
      <div className="relative h-[20vh]">
        {/* Text Input Box */}
        <textarea
          value={input}
          onChange={(e) => updateInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          className="w-full h-full p-3 pr-10 pb-10 rounded-3xl bg-[#01563E] text-white placeholder-gray-300 
                    focus:ring-2 focus:ring-[#DCEAAB] focus:outline-none resize-none overflow-y-auto whitespace-pre-wrap"
        />
        {/* Send Button Inside Textarea */}
        <button
          onClick={handleSend}
          disabled={!sendable}
          className={`absolute bottom-3 right-3 p-2 rounded-full shadow-md items-center transition-colors duration-200 ${
            sendable ? 'bg-white hover:bg-gray-100 hover:scale-110 cursor-pointer' : 'bg-[#D9D9D9] opacity-80 cursor-default'
          }`}
        >
          {/* Send Arrow and Loading Square animations */}
          {responsePending ? (
            <svg className="w-5 h-5 animate-pulse" viewBox="0 0 10 10" xmlns="http://www.w3.org/2000/svg">
              <rect width="8" height="8" x="1" y="1" rx="2" ry="2" fill="#FF5151" />
            </svg>
          ) : (
            <svg
              className={`w-5 h-5 transition-transform duration-200 ease-in-out ${
                sendable ? 'hover:scale-110 hover:strokeWidth={4}' : ''
              }`}
              stroke={sendable ? '#62BB46' : 'gray'} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M12 19V5M12 5L5 12M12 5L19 12" />
            </svg>
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
