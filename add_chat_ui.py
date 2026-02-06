#!/usr/bin/env python3
"""Add chat panel to index.html"""

import re

# Read current file
with open('app/static/index.html', 'r') as f:
    content = f.read()

# Chat CSS to add before </style>
chat_css = '''
        /* ============= CHAT PANEL ============= */
        .chat-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: rgba(26, 31, 58, 0.95);
            backdrop-filter: blur(20px);
            border: 2px solid rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            z-index: 1000;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s;
        }
        
        .chat-container.minimized {
            height: 60px;
            overflow: hidden;
        }
        
        body.bright-mode .chat-container {
            background: rgba(255, 255, 255, 0.95);
            border-color: rgba(0, 0, 0, 0.1);
        }
        
        .chat-header {
            padding: 15px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        
        .chat-header h3 {
            margin: 0;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .online-badge {
            background: #43e97b;
            color: #000;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .chat-message {
            padding: 10px 12px;
            border-radius: 12px;
            max-width: 80%;
            word-wrap: break-word;
            animation: fadeInUp 0.3s;
        }
        
        .chat-message.user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            align-self: flex-end;
            margin-left: auto;
        }
        
        .chat-message.other {
            background: rgba(255, 255, 255, 0.1);
            align-self: flex-start;
        }
        
        body.bright-mode .chat-message.other {
            background: rgba(0, 0, 0, 0.05);
        }
        
        .chat-message.system {
            background: rgba(255, 255, 255, 0.05);
            align-self: center;
            font-size: 0.85rem;
            font-style: italic;
            opacity: 0.7;
        }
        
        .chat-username {
            font-weight: bold;
            font-size: 0.85rem;
            margin-bottom: 4px;
            color: #667eea;
        }
        
        .chat-text {
            font-size: 0.95rem;
        }
        
        .chat-timestamp {
            font-size: 0.7rem;
            opacity: 0.6;
            margin-top: 4px;
        }
        
        .chat-input-container {
            padding: 15px;
            border-top: 2px solid rgba(255, 255, 255, 0.1);
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px;
            border-radius: 8px;
            font-size: 0.9rem;
        }
        
        body.bright-mode .chat-input {
            background: rgba(0, 0, 0, 0.05);
            border-color: rgba(0, 0, 0, 0.1);
            color: #000;
        }
        
        .chat-send-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        
        .chat-send-btn:hover {
            transform: scale(1.05);
        }
        
        .chat-send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        @media (max-width: 768px) {
            .chat-container {
                width: calc(100% - 40px);
                left: 20px;
                right: 20px;
            }
        }
'''

# Chat HTML to add before </body>
chat_html = '''
    <!-- ============= CHAT PANEL ============= -->
    <div class="chat-container" id="chatContainer">
        <div class="chat-header" onclick="toggleChat()">
            <h3>
                💬 Live Chat
                <span class="online-badge" id="onlineBadge">0 online</span>
            </h3>
            <span id="chatToggle">_</span>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message system">
                Welcome to AllCanLearn! Chat with other learners...
            </div>
        </div>
        
        <div class="chat-input-container">
            <input 
                type="text" 
                class="chat-input" 
                id="chatInput" 
                placeholder="Type a message..."
                onkeypress="if(event.key==='Enter') sendMessage()"
            >
            <button class="chat-send-btn" onclick="sendMessage()" id="sendBtn">Send</button>
        </div>
    </div>
'''

# Chat JavaScript to add before </script> (at the end)
chat_js = '''
        // ============= CHAT WEBSOCKET =============
        let chatSocket = null;
        let chatUsername = localStorage.getItem('chatUsername') || prompt('Enter your username:') || 'Anonymous';
        localStorage.setItem('chatUsername', chatUsername);
        
        function connectChat() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            chatSocket = new WebSocket(`${protocol}//${window.location.host}/ws/chat?username=${encodeURIComponent(chatUsername)}`);
            
            chatSocket.onopen = () => {
                console.log('Chat connected');
                document.getElementById('sendBtn').disabled = false;
            };
            
            chatSocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleChatMessage(data);
            };
            
            chatSocket.onclose = () => {
                console.log('Chat disconnected, reconnecting...');
                document.getElementById('sendBtn').disabled = true;
                setTimeout(connectChat, 3000);
            };
            
            chatSocket.onerror = (error) => {
                console.error('Chat error:', error);
            };
        }
        
        function handleChatMessage(data) {
            const messagesDiv = document.getElementById('chatMessages');
            
            if (data.type === 'history') {
                // Load message history
                data.messages.forEach(msg => displayMessage(msg));
            } else if (data.type === 'message') {
                displayMessage(data);
            } else if (data.type === 'system') {
                displaySystemMessage(data.message);
                if (data.online_count !== undefined) {
                    updateOnlineCount(data.online_count);
                }
            } else if (data.type === 'online_users') {
                updateOnlineCount(data.count);
            }
            
            // Auto-scroll to bottom
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function displayMessage(data) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            const isOwn = data.username === chatUsername;
            
            messageDiv.className = `chat-message ${isOwn ? 'user' : 'other'}`;
            messageDiv.innerHTML = `
                ${!isOwn ? `<div class="chat-username">${data.username}</div>` : ''}
                <div class="chat-text">${escapeHtml(data.message)}</div>
                <div class="chat-timestamp">${formatTime(data.timestamp)}</div>
            `;
            
            messagesDiv.appendChild(messageDiv);
        }
        
        function displaySystemMessage(message) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message system';
            messageDiv.textContent = message;
            messagesDiv.appendChild(messageDiv);
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message && chatSocket && chatSocket.readyState === WebSocket.OPEN) {
                chatSocket.send(message);
                input.value = '';
            }
        }
        
        function toggleChat() {
            const container = document.getElementById('chatContainer');
            const toggle = document.getElementById('chatToggle');
            container.classList.toggle('minimized');
            toggle.textContent = container.classList.contains('minimized') ? '▫' : '_';
        }
        
        function updateOnlineCount(count) {
            document.getElementById('onlineBadge').textContent = `${count} online`;
        }
        
        function formatTime(timestamp) {
            const date = new Date(timestamp);
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Connect chat on page load
        connectChat();
'''

# Add CSS before </style>
if '/* ============= CHAT PANEL ============= */' not in content:
    content = content.replace('    </style>', chat_css + '    </style>')
    print('✅ Chat CSS added')

# Add HTML before </body>
if '<!-- ============= CHAT PANEL ============= -->' not in content:
    content = content.replace('</body>', chat_html + '</body>')
    print('✅ Chat HTML added')

# Add JavaScript before </script> at the end
if '// ============= CHAT WEBSOCKET =============' not in content:
    # Find the last </script> tag
    last_script_pos = content.rfind('</script>')
    if last_script_pos != -1:
        content = content[:last_script_pos] + chat_js + content[last_script_pos:]
        print('✅ Chat JavaScript added')

# Write back
with open('app/static/index.html', 'w') as f:
    f.write(content)

print('✅ Chat panel successfully added to podcast page!')
