import React, { useState, useEffect, useRef } from 'react';

function ChatPanel({ soundEnabled }) {
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [onlineCount, setOnlineCount] = useState(0);
  const [username, setUsername] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const ws = useRef(null);

  useEffect(() => {
    const savedUsername = localStorage.getItem('chatUsername');
    if (savedUsername) {
      setUsername(savedUsername);
    } else {
      const newUsername = prompt('Enter your username:') || 'Anonymous';
      setUsername(newUsername);
      localStorage.setItem('chatUsername', newUsername);
    }
  }, []);

  useEffect(() => {
    connectChat();
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [username]);

  const connectChat = () => {
    if (!username) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    ws.current = new WebSocket(`${protocol}//${window.location.host}/ws/chat?username=${encodeURIComponent(username)}`);
    
    ws.current.onopen = () => {
      console.log('Chat connected');
      setIsConnected(true);
    };
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleChatMessage(data);
    };
    
    ws.current.onclose = () => {
      console.log('Chat disconnected, reconnecting...');
      setIsConnected(false);
      setTimeout(connectChat, 3000);
    };
    
    ws.current.onerror = (error) => {
      console.error('Chat error:', error);
    };
  };

  const handleChatMessage = (data) => {
    if (data.type === 'history') {
      setMessages(data.messages || []);
    } else if (data.type === 'message') {
      setMessages(prev => [...prev, data]);
    } else if (data.type === 'system') {
      setMessages(prev => [...prev, { ...data, type: 'system' }]);
      if (data.online_count !== undefined) {
        setOnlineCount(data.online_count);
      }
    } else if (data.type === 'online_users') {
      setOnlineCount(data.count);
    }
  };

  const sendMessage = () => {
    const message = inputMessage.trim();
    
    if (message && ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message);
      setInputMessage('');
    }
  };

  const toggleChat = () => {
    setIsMinimized(!isMinimized);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const escapeHtml = (text) => {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  };

  return (
    <div className={`chat-container ${isMinimized ? 'minimized' : ''}`}>
      <div className="chat-header" onClick={toggleChat}>
        <h3>
          💬 Live Chat
          <span className="online-badge">{onlineCount} online</span>
        </h3>
        <span>{isMinimized ? '▫' : '_'}</span>
      </div>
      
      <div className="chat-messages">
        <div className="chat-message system">
          Welcome to AllCanLearn! Chat with other learners...
        </div>
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.type === 'system' ? 'system' : msg.username === username ? 'user' : 'other'}`}>
            {msg.type !== 'system' && msg.username !== username && (
              <div className="chat-username">{msg.username}</div>
            )}
            <div className="chat-text">{escapeHtml(msg.message || msg.text)}</div>
            <div className="chat-timestamp">{formatTime(msg.timestamp)}</div>
          </div>
        ))}
      </div>
      
      <div className="chat-input-container">
        <input 
          type="text" 
          className="chat-input" 
          placeholder="Type a message..." 
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button 
          className="chat-send-btn" 
          onClick={sendMessage}
          disabled={!isConnected}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;
