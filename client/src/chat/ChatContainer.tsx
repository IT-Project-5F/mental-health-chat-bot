import { useState, useRef, useEffect } from 'react';
import ChatInput from './ChatInput';
import SendBubble from './SenderBubble';
import ResponseBubble from './ResponseBubble';
import TypingAnimation from './TypingAnimation';

/* Types and Interfaces */
interface Message {
    id: number;
    text: string;
    sender: 'user' | 'chatbot'
}

/**
 * Functionalities:
 * - Timeout and typing animation before Chatbot sends response.
 * - Auto scroll to the bottom when a new chat is sent. 
 * - Chat Container is draggable to max 50% of screen.
 * - Chat Container can be collapsed completely and expanded again. 
 */
const ChatContainer: React.FC = () => {    
    // Example Messages
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, text: 'Find me mental health services in Parkville.', sender: 'user' },
        { id: 2, text: 'I found five clinics within 5km of Parkville.', sender: 'chatbot' },
        { id: 3, text: 'I want to find clinics specialising in treatment for anxiety.', sender: 'user' },
        { id: 4, text: 'View the map.', sender: 'chatbot' },
    ])

    /* State */
    const [isOpen, setIsOpen] = useState(true);
    const [typing, setTyping] = useState(false);

    /* Refs */
    // End Position of Latest Message
    const messageEndRef = useRef<HTMLDivElement | null>(null);

    /* Effects */
    // Auto scroll to bottom of latest sent message
    useEffect(() => {
      messageEndRef.current?.scrollIntoView({behavior: 'smooth' });
    }, [messages, typing]);

    /* Functions */
    // Send message
    const handleSend = (text: string) => {
    const newMessage: Message = {
      id: messages.length + 1,
      text,
      sender: 'user',
    };
    setMessages([...messages, newMessage]);

    // Display typing animation
    setTyping(true);

    // After delay, typing animation is hidden and response message is displayed
    setTimeout(() => {
      setTyping(false);
      setMessages((prev: Message[]) => [
        ...prev,
        { id: prev.length + 1, text: "I found the following results.", sender: 'chatbot' },
      ]);
    }, 2000);
  };


  /* Rendering: Case - Chat container is closed */
  if (!isOpen) {
    return (
      <button
        className="fixed top-1/2 right-0 -translate-y-1/2 bg-[#014532] text-white px-2.5 py-6 rounded-l-lg shadow-md hover:bg-[#026b4c] 
          transition-transform duration-300 ease-in-out hover:scale-110"
        onClick={() => setIsOpen(true)}
      >
        {/* Left-pointing arrow */}
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">
          <path d="M17.5 20L12.5 15L17.5 10" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    );
  }


  /* Rendering */
  return (
    <div className="relative flex flex-col h-screen w-0.3 bg-[#014532]">
      {/* Tab to collaspe chat container */}
      <button
        className="absolute -left-9.5 top-1/2 -translate-y-1/2 bg-[#014532] p-1 py-4 rounded-l-lg hover:bg-[#026b4c] z-10"
        onClick={() => setIsOpen(false)}
      >
        {/* Right-pointing arrow */}
        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">
          <path d="M12.5 10L17.5 15L12.5 20" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
      
      {/* Header */}
      <div className="flex p-1.5 bg-[#013F2D] border-t border-gray-700">
        <button 
          className="ml-auto p-1 rounded-full hover:bg-[#215B4B] transition-transform duration-300 ease-in-out hover:scale-90"
          onClick = {() => setIsOpen(false)}
        >
          {/* Close chat container button */}
          <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 30 30" fill="none">
            <path d="M22.5 22.5L15 15M15 15L7.5 7.5M15 15L22.5 7.5M15 15L7.5 22.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) =>
          msg.sender === 'user' ? (
            <SendBubble key={msg.id} text={msg.text} />
          ) : (
            <ResponseBubble key={msg.id} text={msg.text} />
          )
        )}
        {typing && <TypingAnimation />}
        <div ref={messageEndRef} />
      </div>
      {/* Input */}
      <ChatInput sendMessage={handleSend} responsePending={typing} />
    </div>
  );
};

export default ChatContainer;