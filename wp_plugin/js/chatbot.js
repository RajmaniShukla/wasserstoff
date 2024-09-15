jQuery(document).ready(function($) {
    $('#chatbot').html('<form id="chat-form"><input type="text" id="chat-query" placeholder="Ask me anything..."/><button type="submit">Send</button></form><div id="chat-response"></div>');

    $('#chat-form').submit(function(e) {
        e.preventDefault();
        
        var query = $('#chat-query').val();
        
        $.ajax({
            url: 'http://127.0.0.1:5000/chat',  // Adjust the URL if needed
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: query }),
            success: function(response) {
                $('#chat-response').text(response.response);
            },
            error: function() {
                $('#chat-response').text('Error occurred. Please try again.');
            }
        });
    });
});
