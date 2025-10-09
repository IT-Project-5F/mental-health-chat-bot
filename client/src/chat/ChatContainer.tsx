import { useState, useRef, useEffect } from 'react';
import ChatInput from './ChatInput';
import SendBubble from './SenderBubble';
import ResponseBubble from './ResponseBubble';
import TypingAnimation from './TypingAnimation';
import SuggestedQueryButton from './SuggestedQueryButton.tsx';
import { request } from '../api.ts';

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
 * - Chat Container can be enlarged by dragging using mouse (desktop only) or touch screen (for mobile or desktop)
 */
const ChatContainer: React.FC = () => {    
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: 'Hello 👋, how can I help you today?', sender: 'chatbot' },
  ])
  const [sessionID, setSessionID] = useState<string | null>(null);

  // Suggested Queries
  const suggestedQueries = [
    "Find health services and clinics near me",
    "Add a new service",
  ];


  /* State */
  const [isOpen, setIsOpen] = useState(true);
  const [typing, setTyping] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [containerWidth, setContainerWidth] = useState(window.innerWidth * 0.45); // Default Width of Chat Container (Desktop)
  const [containerHeight, setContainerHeight] = useState(window.innerHeight * 0.5); // Default Height of Chat Container (Mobile)
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  const [delayShowingSuggestions, setDelayShowingSuggestions] = useState(false); // For delaying when suggested query options are shown
  const [showScrollToBottomArrow, setShowScrollToBottomArrow] = useState(false); // Indicates when 'Scroll to Bottom' arrow is displayed in container

  /* Derived values for UI conditional rendering */
  const lastMessageFromChatbot = messages.length > 0 && messages[messages.length - 1].sender === 'chatbot';
  const showSuggestedQueries = !typing && lastMessageFromChatbot && suggestedQueries.length > 0 && delayShowingSuggestions;

  /* Refs */
  const messageEndRef = useRef<HTMLDivElement | null>(null); // End Position of Latest Message
  const scrollContainerRef = useRef<HTMLDivElement | null>(null); // Track how much user has scrolled up in container

  /* Animation for message entry in chat container */
  // Keyframes for send/response message entry animation
  const messageAnimation = `
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulseArrow {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); } 
  }
  `;
  // Keyframes in style tag
  useEffect(() => {
    const styleTag = document.createElement('style');
    styleTag.innerHTML = messageAnimation;
    document.head.appendChild(styleTag);
    return () => {
      document.head.removeChild(styleTag);
    };
  }, []);


  /* Effects */
  // When message is sent, auto scroll to bottom of chat history
  useEffect(() => {
    messageEndRef.current?.scrollIntoView({behavior: 'smooth' });
  }, [messages, typing]);


  // When user opens chat container using the side arrow tab, auto scroll to bottom of chat history
  useEffect(() => {
    if (isOpen) {
      messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, typing, isOpen]);


  // Track how far above the user has scrolled in the chat container to show 'Scroll to Bottom' arrow
  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const checkScroll = () => {
    const distanceFromBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight;
    setShowScrollToBottomArrow(distanceFromBottom > 1000); // adjust threshold as needed
    };

    checkScroll();

    container.addEventListener('scroll', checkScroll);
    return () => container.removeEventListener('scroll', checkScroll);
  }, [isOpen, messages]);


  // Updating the state for mobile screen width
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);


  // Delay showing of suggested queries after the chatbot has sent a response
  useEffect(() => {
    if (!typing && lastMessageFromChatbot) {
      const timeout = setTimeout(() => {
        setDelayShowingSuggestions(true);
        }, 800);
      return () => clearTimeout(timeout);
    } else {
      setDelayShowingSuggestions(false);
    }
  }, [typing, lastMessageFromChatbot]);


  // Dragging functionality to resize the chat container
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;

      // Mobile Screen: Chat container is at the bottom and can be dragged upwards to enlarge
      if (isMobile) {
        const newHeight = window.innerHeight - e.clientY;
        const minHeight = 100;
        const maxHeight = window.innerHeight;
        setContainerHeight(Math.min(Math.max(newHeight, minHeight), maxHeight));
      }
      // Desktop Screen: Chat container is at the right of the screen and can be dragged towards the middle to enlarge
      else {
        const maxWidth = window.innerWidth >= 1920 ? window.innerWidth * 0.33 : window.innerWidth * 0.5;
        const minWidth = 300;
        const newWidth = Math.min(Math.max(window.innerWidth - e.clientX, minWidth), maxWidth);
        setContainerWidth(newWidth);
      }
    };

    // Handling of Touchscreen Action instead of mouse down
    const handleTouchMove = (e: TouchEvent) => {
      if (!isDragging) return;
      if (isMobile) {
        const newHeight = window.innerHeight - e.touches[0].clientY;
        setContainerHeight(Math.min(Math.max(newHeight, 100), window.innerHeight));
      } 
      // Desktop that is Touchscreen
      else {
        const maxWidth = window.innerWidth >= 1920 ? window.innerWidth * 0.33 : window.innerWidth * 0.5;
        const newWidth = Math.min(Math.max(window.innerWidth - e.touches[0].clientX, 300), maxWidth);
        setContainerWidth(newWidth);
      }
    };

    const stopDragging = () => setIsDragging(false);

    // Tracking of mouse movement for drag functionality
    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', stopDragging);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', stopDragging);
    }
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', stopDragging);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', stopDragging);
    };
  }, [isDragging, isMobile]);


  /* Helper Function - Handle sending of suggested queries */
  const handleSuggestedQuery = (query: string) => {
    handleSend(query);
  };

  /* Helper Function - Handle scrolling to bottom */
  const handleScrollToBottom = () => {
    messageEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };


  /* Send Message Function 
   * Once a user sends a message, the helper function is called to handle the request to the backend
   */
  const handleSend = async (text: string) => {
    const newMessage: Message = {
      id: messages.length + 1,
      text,
      sender: 'user',
    };
    setMessages([...messages, newMessage]);

    // Display typing animation
    setTyping(true);
    const start = Date.now();

    // API creates a new chat session automatically
    try {
      const body: any = { message: text };
      if (sessionID) {
        body.session_id = sessionID;
      }

      const response = await request('POST', '/api/chat', body);

      // Minimum typing animation is 1000ms
      const elapsed = Date.now() - start;
      const minDelay = 700;
      const waitTime = elapsed < minDelay ? minDelay - elapsed : 0;

      setTimeout(() => {
        if (response?.response) {
          setSessionID(response.session_id);
          setMessages((prev: Message[]) => [
            ...prev,
            { id: prev.length + 1, text: response.response, sender: 'chatbot' },
          ]);
        } 
        else {
          setMessages((prev: Message[]) => [
            ...prev,
            { id: prev.length + 1, text: "Sorry, something went wrong. Please try again.", sender: 'chatbot' },
          ]);
        }
        setTyping(false);
      }, waitTime);
    } catch (e) {
      setMessages((prev: Message[]) => [
        ...prev,
        { id: prev.length + 1, text: "Sorry, something went wrong. Please try again.", sender: "chatbot" },
      ]);
      setTyping(false);
    };
  };

  
  /********************************************************************************/
  /* Rendering: Case - Chat Container is closed */
  if (!isOpen) {
    return (
      <button
      style={{ animation: 'pulseArrow 1.5s ease-in-out infinite',}}  
      className={`fixed right-0 ${isMobile ? 'bottom-0 w-full flex justify-center items-center' : 'top-1/2 -translate-y-1/2'} 
          bg-[#014532] text-white px-2.5 py-5 rounded-l-lg shadow-md hover:bg-[#026b4c] 
          transition-transform duration-300 ease-in-out hover:scale-110`}
        onClick={() => setIsOpen(true)}
      >
        {isMobile ? (
          // Up-pointing arrow for mobile
          <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M10 17.5L15 12.5L20 17.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        ) : (
          // Left-pointing arrow for desktop
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">
            <path d="M17.5 20L12.5 15L17.5 10" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </button>
    );
  }


  /* Rendering: Case - Chat Container is open */
  return (
    <div 
      style={isMobile ? { height: containerHeight } : { width: containerWidth }}
      className={`fixed ${isMobile ? 'bottom-0 left-0 w-full rounded-t-lg' : 'right-0 top-0 h-full'}
        flex flex-col bg-[#014532] shadow-2xl border-l border-gray-700`}
    >
      {/* Tab to drag or collapse chat container */}
      <button
        onMouseDown={() => setIsDragging(true)}
        onTouchStart={() => setIsDragging(true)}
        className={`absolute z-10 p-1 py-2 bg-[#014532] hover:bg-[#026b4c] transition-colors duration-200
          ${isMobile 
            ? 'top-0 left-1/2 -translate-x-1/2 rounded-b-lg cursor-ns-resize' 
            : '-left-9.5 top-1/2 -translate-y-1/2 rounded-l-lg cursor-ew-resize'}`}
        onClick={() => setIsOpen(false)}
      >
        {isMobile ? (
          // Down-pointing arrow for mobile when chat is open
          <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 12.5L15 17.5L10 12.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          ) : (
          // Right-pointing arrow for desktop when chat is open
          <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30" fill="none">
            <path d="M12.5 10L17.5 15L12.5 20" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          )}
      </button>
      
      {/* Header */}
      <div className="flex px-3 py-2 bg-gradient-to-r from-[#FDB4C6] to-[#62BB46] bg-[#013F2D]">
        <h1 className="text-[#014532] text-lg font-bold ml-1">Health Navigator</h1>
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
      <div 
        ref={scrollContainerRef}
        className="flex-1 flex-col overflow-y-auto p-4 space-y-6">
        <div className="max-w-[600px] mx-auto space-y-6">
          {messages.map((msg) =>
            msg.sender === 'user' ? (
            <SendBubble key={msg.id} text={msg.text} />
            ) : (
              <ResponseBubble key={msg.id} text={msg.text} />
            )
          )}
          {typing && <TypingAnimation />}

          {/* Suggested Query Buttons */}
          {showSuggestedQueries && (
            <div className="flex flex-wrap justify-center mt-4 pt-4 gap-3">
              {suggestedQueries.map((q, index) => (
                <SuggestedQueryButton key={index} text={q}
                  onClick={handleSuggestedQuery}
                />
              ))}
            </div>
          )}

          {/* Conditional Rendering - Scroll to Bottom Arrow */}
          {showScrollToBottomArrow && (
            <div className={`sticky bottom-4 w-full flex justify-center z-50 pointer-events-none"`}>
              <button
                onClick={handleScrollToBottom}
                className="bg-[#026b4c] hover:bg-[#03855f] text-white p-2 rounded-full shadow-lg
                          transition-transform duration-200 hover:scale-110 pointer-events-auto"
                style={{ animation: 'pulseArrow 1.5s ease-in-out infinite' }}
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M18 15l-6 6-6-6" />
                  <path d="M12 3v18" />
                </svg>
              </button>
            </div>
          )}

          <div ref={messageEndRef} />
        </div>
      </div>
      
      {/* Input */}
      <ChatInput sendMessage={handleSend} responsePending={typing} />
    </div>
  );
};

export default ChatContainer;