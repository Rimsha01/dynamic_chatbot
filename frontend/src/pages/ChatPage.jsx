import { useState, useEffect, useRef } from 'react';
import Chat from '../components/Chat';
import { createWebSocket } from '../api/api';
import { FiSend, FiUser, FiMessageSquare, FiMessageCircle, FiZap } from 'react-icons/fi';

function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const ws = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');

    ws.current.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.current.onmessage = (event) => {
      setIsTyping(false);
      const newMessage = {
        text: event.data,
        isUser: false,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, newMessage]);
    };

    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages change
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = () => {
    if (inputMessage.trim() && ws.current) {
      const newMessage = {
        text: inputMessage,
        isUser: true,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, newMessage]);
      ws.current.send(inputMessage);
      setInputMessage('');
      setIsTyping(true);
    }
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <FiMessageSquare size={24} />
        <h1>Dynamic Chatbot</h1>
      </div>
      <div className="chat-container" ref={chatContainerRef}>
        {messages.length === 0 ? (
          <div className="empty-chat">
            <FiMessageSquare size={48} />
            <h3>Start a conversation</h3>
            <p>Send a message to begin chatting with the AI assistant</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.isUser ? 'user' : 'bot'}`}
            >
              <div className="message-content">{message.text}</div>
              <div className="message-time">
                {message.isUser ? (
                  <FiUser size={14} />
                ) : (
                  <FiMessageSquare size={14} /> // or use FiMessageCircle or FiZap
                )}
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>
          ))
        )}
        {isTyping && (
          <div className="message bot">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="message-input-container">
        <div className="message-input">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Type your message..."
          />
          <button onClick={handleSendMessage} disabled={!inputMessage.trim()}>
            <FiSend size={18} />
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;