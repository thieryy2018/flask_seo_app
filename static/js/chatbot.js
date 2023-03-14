function openChatbot() {
    var chatWindow = window.open("/chatbot", "chatWindow", "width=350,height=500");
    chatWindow.focus();
}

$(document).ready(function() {
    var chatWindow;

    function openChatbot() {
        chatWindow = window.open("/chatbot", "chatWindow", "width=350,height=500");
    }

    $("#open-chatbot").click(function(event) {
        event.preventDefault();
        openChatbot();
    });

    $("#clear-chat").click(function(event) {
        event.preventDefault();
        // Exclude the initial message when clearing the chat history
        $(".chat-history .message:not(#initial-message)").remove();

        // Send an AJAX request to clear the chat history on the server
        $.post("/clear_chat", function() {
            console.log("Chat history cleared");
        });
    });
});
