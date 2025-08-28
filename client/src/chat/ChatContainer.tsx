import { useState } from 'react';
import ChatInput from './ChatInput';
import SendBubble from './SenderBubble';
import ResponseBubble from './ResponseBubble';

// Types for message object
interface Message {
    id: number;
    text: string;
    sender: 'user' | 'chatbot'
}

const ChatContainer: React.FC = () => {
    // Functionalities
    // Need to add chatbot typing animation
    // Need to add chat input typing box expansion and scrolling
    // Need to add dragging to expand and close chat - draggable
    
    // Example Messages
    const [messages, setMessages] = useState<Message[]>([
        { id: 1, text: 'Find me mental health services in Parkville.', sender: 'user' },
        { id: 2, text: 'I found five clinics within 5km of Parkville.', sender: 'chatbot' },
        { id: 3, text: 'I want to find clinics specialising in treatment for anxiety.', sender: 'user' },
        { id: 4, text: 'View the map.', sender: 'chatbot' },
    ])

    const handleSend = (text: string) => {
    const newMessage: Message = {
      id: messages.length + 1,
      text,
      sender: 'user',
    };
    setMessages([...messages, newMessage]);

    // Chatbot timeout and response to sender's message    
    setTimeout(() => {
      setMessages((prev: Message[]) => [
        ...prev,
        { id: prev.length + 1, text: "This is a response!", sender: 'chatbot' },
      ]);
    }, 1000);
  };

  // Styling
  return (
    <div className="flex flex-col h-screen w-100 bg-[#014532]">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) =>
          msg.sender === 'user' ? (
            <SendBubble key={msg.id} text={msg.text} />
          ) : (
            <ResponseBubble key={msg.id} text={msg.text} />
          )
        )}
      </div>
      <ChatInput sendMessage={handleSend} />
    </div>
  );
};

export default ChatContainer;