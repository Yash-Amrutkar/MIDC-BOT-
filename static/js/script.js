// MIDC Chatbot - Interactive JavaScript
class MIDCChatbot {
    constructor() {
        this.chatWidget = document.getElementById('chatWidget');
        this.floatingBtn = document.getElementById('floatingChatBtn');
        this.chatToggle = document.getElementById('chatToggle');
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.contextModal = document.getElementById('contextModal');
        this.closeModal = document.getElementById('closeModal');
        this.contextContent = document.getElementById('contextContent');
        
        this.isOpen = false;
        this.initializeEventListeners();
        this.checkHealth();
        this.setWelcomeTime();
    }

    initializeEventListeners() {
        // Chat widget toggle functionality
        this.floatingBtn.addEventListener('click', () => this.toggleChat());
        this.chatToggle.addEventListener('click', () => this.closeChat());
        
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Handle suggestion clicks
        document.querySelectorAll('.suggestion').forEach(suggestion => {
            suggestion.addEventListener('click', () => {
                this.messageInput.value = suggestion.dataset.query;
                this.messageInput.focus();
            });
        });

        // Modal close functionality
        this.closeModal.addEventListener('click', () => this.closeContextModal());
        
        // Close modal on outside click
        this.contextModal.addEventListener('click', (e) => {
            if (e.target === this.contextModal) {
                this.closeContextModal();
            }
        });

        // Close modal on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                if (this.contextModal.style.display === 'block') {
                    this.closeContextModal();
                } else if (this.isOpen) {
                    this.closeChat();
                }
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        this.isOpen = true;
        this.chatWidget.classList.add('active');
        this.messageInput.focus();
    }

    closeChat() {
        this.isOpen = false;
        this.chatWidget.classList.remove('active');
    }

    async checkHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                console.log('✅ MIDC Chatbot is ready');
            } else {
                console.log('❌ Service unavailable');
            }
        } catch (error) {
            console.error('❌ Health check failed:', error);
        }
    }

    setWelcomeTime() {
        const welcomeTime = document.getElementById('welcomeTime');
        if (welcomeTime) {
            welcomeTime.textContent = new Date().toLocaleTimeString();
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.sendButton.disabled = true;
        this.showTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            this.hideTypingIndicator();

            if (data.success) {
                this.addMessage(data.response, 'bot', data.context_docs, data.language);
            } else {
                this.addMessage(`Sorry, I encountered an error: ${data.error}`, 'bot');
            }
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting. Please try again later.', 'bot');
            console.error('Chat error:', error);
        } finally {
            this.sendButton.disabled = false;
            this.messageInput.focus();
        }
    }

    addMessage(content, sender, contextDocs = [], language = 'english') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Format the content (handle line breaks and lists)
        if (typeof content === 'string') {
            messageText.innerHTML = this.formatMessage(content);
        } else {
            messageText.appendChild(content);
        }
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString();
        
        // Add language indicator for bot messages
        if (sender === 'bot' && language) {
            const languageIndicator = document.createElement('div');
            languageIndicator.className = 'language-indicator';
            languageIndicator.innerHTML = `<i class="fas fa-globe"></i> ${language === 'marathi' ? 'मराठी' : 'English'}`;
            messageTime.appendChild(languageIndicator);
        }
        
        // Add context docs button if available
        if (contextDocs && contextDocs.length > 0) {
            const contextButton = document.createElement('button');
            contextButton.className = 'context-button';
            contextButton.innerHTML = '<i class="fas fa-file-alt"></i> View Sources';
            contextButton.addEventListener('click', () => this.showContextDocs(contextDocs));
            messageContent.appendChild(contextButton);
        }
        
        messageContent.appendChild(messageText);
        messageContent.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Convert line breaks to <br>
        let formatted = content.replace(/\n/g, '<br>');
        
        // Convert bullet points
        formatted = formatted.replace(/^[\s]*•[\s]*/gm, '• ');
        formatted = formatted.replace(/^[\s]*\*[\s]*/gm, '• ');
        formatted = formatted.replace(/^[\s]*-[\s]*/gm, '• ');
        
        // Convert numbered lists
        formatted = formatted.replace(/^[\s]*\d+\./gm, (match) => match.trim());
        
        // Convert URLs to links
        formatted = formatted.replace(
            /(https?:\/\/[^\s]+)/g,
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );
        
        return formatted;
    }

    showContextDocs(contextDocs) {
        this.contextContent.innerHTML = '';
        
        contextDocs.forEach((doc, index) => {
            const docDiv = document.createElement('div');
            docDiv.className = 'context-doc';
            
            const title = document.createElement('h4');
            title.textContent = `Document ${index + 1}`;
            
            const content = document.createElement('p');
            content.textContent = doc.content || doc.text || 'No content available';
            
            docDiv.appendChild(title);
            docDiv.appendChild(content);
            this.contextContent.appendChild(docDiv);
        });
        
        this.contextModal.style.display = 'block';
    }

    closeContextModal() {
        this.contextModal.style.display = 'none';
    }

    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    // Utility method to add loading states
    showLoading() {
        this.sendButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        this.sendButton.disabled = true;
    }

    hideLoading() {
        this.sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
        this.sendButton.disabled = false;
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MIDCChatbot();
    
    // Add some interactive features
    console.log('🏢 MIDC Land Bank Chatbot initialized successfully!');
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('messageInput').focus();
        }
    });
});

// Add CSS for context button
const style = document.createElement('style');
style.textContent = `
    .context-button {
        background: var(--primary-color);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: var(--border-radius);
        font-size: 0.875rem;
        cursor: pointer;
        margin-top: 0.5rem;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .context-button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
    }
`;
document.head.appendChild(style);
