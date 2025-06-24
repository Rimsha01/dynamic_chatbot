function Chat({ messages }) {
  return (
    <div className="chat-container">
      {messages.length === 0 ? (
        <div className="empty-chat">Start a conversation with the chatbot</div>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.isUser ? 'user' : 'bot'}`}
          >
            <div className="message-content">{message.text}</div>
            <div className="message-time">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Chat;