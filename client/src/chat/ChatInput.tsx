import { useState, KeyboardEvent } from 'react';

interface ChatInputProps {
  sendMessage: (message: string) => void;
}

const ChatInput: React.FC<ChatInputProps> = ({ sendMessage }) => {
  const [input, updateInput] = useState('');

  const handleSend = () => {
    if (input.trim() === '') return;
    // Call parent function to send the message
    sendMessage(input);
    // Chat input is cleared after message is sent
    updateInput('');
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="flex p-4 bg-[#013F2D] border-t border-gray-700">
      <input
        type="text"
        value={input}
        onChange={(e) => updateInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message..."
        className="flex-1 p-3 rounded-xl bg-[#01563E] text-white placeholder-gray-300 focus:outline-none"
      />
      <button
        onClick={handleSend}
        className="bg-[#62BB46] rounded-full hover:bg-green-500 transition flex items-center justify-center p-3 ml-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"
        >
          <path d="M12 19V5M12 5L5 12M12 5L19 12" />
        </svg>
</button>
    </div>
  );
};

export default ChatInput;
