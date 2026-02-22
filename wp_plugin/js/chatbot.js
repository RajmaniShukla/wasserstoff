/**
 * Wasserstoff Chatbot - WordPress Integration
 * A sleek chatbot widget powered by GPT-2
 */
(function($) {
    'use strict';

    // Configuration
    const CONFIG = {
        apiUrl: 'http://127.0.0.1:5000/suggest',
        typingDelay: 50,
        maxMessageLength: 500
    };

    // Chatbot HTML template
    const chatbotHTML = `
        <div id="wasserstoff-chatbot" class="ws-chatbot">
            <div class="ws-chatbot-toggle" title="Chat with AI">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </div>
            <div class="ws-chatbot-window">
                <div class="ws-chatbot-header">
                    <div class="ws-chatbot-title">
                        <span class="ws-status-dot"></span>
                        AI Assistant
                    </div>
                    <button class="ws-chatbot-close" aria-label="Close chat">&times;</button>
                </div>
                <div class="ws-chatbot-messages">
                    <div class="ws-message ws-bot-message">
                        <div class="ws-message-content">
                            👋 Hi! I'm your AI assistant. How can I help you today?
                        </div>
                    </div>
                </div>
                <form class="ws-chatbot-input" id="ws-chat-form">
                    <input type="text" id="ws-chat-query" placeholder="Type your message..." maxlength="500" autocomplete="off">
                    <button type="submit" aria-label="Send message">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    `;

    // Chatbot styles
    const chatbotStyles = `
        <style>
            .ws-chatbot {
                --ws-primary: #0ea5e9;
                --ws-primary-dark: #0284c7;
                --ws-bg: #ffffff;
                --ws-text: #1e293b;
                --ws-text-light: #64748b;
                --ws-border: #e2e8f0;
                --ws-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
                
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 99999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }

            .ws-chatbot-toggle {
                width: 56px;
                height: 56px;
                border-radius: 50%;
                background: linear-gradient(135deg, var(--ws-primary), var(--ws-primary-dark));
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: var(--ws-shadow);
                transition: transform 0.3s, box-shadow 0.3s;
            }

            .ws-chatbot-toggle:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 50px rgba(14, 165, 233, 0.4);
            }

            .ws-chatbot.open .ws-chatbot-toggle {
                display: none;
            }

            .ws-chatbot-window {
                display: none;
                width: 360px;
                height: 500px;
                background: var(--ws-bg);
                border-radius: 16px;
                box-shadow: var(--ws-shadow);
                flex-direction: column;
                overflow: hidden;
            }

            .ws-chatbot.open .ws-chatbot-window {
                display: flex;
            }

            .ws-chatbot-header {
                padding: 16px 20px;
                background: linear-gradient(135deg, var(--ws-primary), var(--ws-primary-dark));
                color: white;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }

            .ws-chatbot-title {
                font-weight: 600;
                font-size: 15px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .ws-status-dot {
                width: 8px;
                height: 8px;
                background: #22c55e;
                border-radius: 50%;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            .ws-chatbot-close {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                line-height: 1;
                opacity: 0.8;
                transition: opacity 0.2s;
            }

            .ws-chatbot-close:hover {
                opacity: 1;
            }

            .ws-chatbot-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 12px;
            }

            .ws-message {
                max-width: 85%;
                animation: slideIn 0.3s ease;
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .ws-message-content {
                padding: 12px 16px;
                border-radius: 16px;
                font-size: 14px;
                line-height: 1.5;
            }

            .ws-user-message {
                align-self: flex-end;
            }

            .ws-user-message .ws-message-content {
                background: linear-gradient(135deg, var(--ws-primary), var(--ws-primary-dark));
                color: white;
                border-bottom-right-radius: 4px;
            }

            .ws-bot-message .ws-message-content {
                background: #f1f5f9;
                color: var(--ws-text);
                border-bottom-left-radius: 4px;
            }

            .ws-typing-indicator {
                display: flex;
                gap: 4px;
                padding: 12px 16px;
            }

            .ws-typing-indicator span {
                width: 8px;
                height: 8px;
                background: var(--ws-text-light);
                border-radius: 50%;
                animation: typing 1.4s infinite both;
            }

            .ws-typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .ws-typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

            @keyframes typing {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-4px); }
            }

            .ws-chatbot-input {
                padding: 16px;
                border-top: 1px solid var(--ws-border);
                display: flex;
                gap: 10px;
            }

            .ws-chatbot-input input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid var(--ws-border);
                border-radius: 12px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.2s;
            }

            .ws-chatbot-input input:focus {
                border-color: var(--ws-primary);
            }

            .ws-chatbot-input button {
                width: 44px;
                height: 44px;
                border: none;
                background: linear-gradient(135deg, var(--ws-primary), var(--ws-primary-dark));
                color: white;
                border-radius: 12px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .ws-chatbot-input button:hover {
                transform: scale(1.05);
            }

            .ws-chatbot-input button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            @media (max-width: 480px) {
                .ws-chatbot-window {
                    width: calc(100vw - 40px);
                    height: calc(100vh - 100px);
                    border-radius: 12px;
                }
            }
        </style>
    `;

    // Initialize chatbot
    function initChatbot() {
        // Inject styles and HTML
        $('head').append(chatbotStyles);
        $('body').append(chatbotHTML);

        const $chatbot = $('#wasserstoff-chatbot');
        const $toggle = $chatbot.find('.ws-chatbot-toggle');
        const $close = $chatbot.find('.ws-chatbot-close');
        const $form = $('#ws-chat-form');
        const $input = $('#ws-chat-query');
        const $messages = $chatbot.find('.ws-chatbot-messages');

        // Toggle chat window
        $toggle.on('click', () => {
            $chatbot.addClass('open');
            $input.focus();
        });

        $close.on('click', () => {
            $chatbot.removeClass('open');
        });

        // Handle form submission
        $form.on('submit', function(e) {
            e.preventDefault();
            
            const query = $input.val().trim();
            if (!query) return;

            // Add user message
            addMessage(query, 'user');
            $input.val('').focus();

            // Show typing indicator
            const $typing = showTypingIndicator();

            // Send to API
            $.ajax({
                url: CONFIG.apiUrl,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ query: query }),
                success: function(response) {
                    $typing.remove();
                    addMessage(response.suggestion, 'bot');
                },
                error: function() {
                    $typing.remove();
                    addMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            });
        });

        // Add message to chat
        function addMessage(text, type) {
            const $message = $(`
                <div class="ws-message ws-${type}-message">
                    <div class="ws-message-content">${escapeHtml(text)}</div>
                </div>
            `);
            $messages.append($message);
            scrollToBottom();
        }

        // Show typing indicator
        function showTypingIndicator() {
            const $typing = $(`
                <div class="ws-message ws-bot-message ws-typing">
                    <div class="ws-message-content ws-typing-indicator">
                        <span></span><span></span><span></span>
                    </div>
                </div>
            `);
            $messages.append($typing);
            scrollToBottom();
            return $typing;
        }

        // Scroll to bottom of messages
        function scrollToBottom() {
            $messages.scrollTop($messages[0].scrollHeight);
        }

        // Escape HTML to prevent XSS
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    }

    // Initialize when DOM is ready
    $(document).ready(initChatbot);

})(jQuery);
