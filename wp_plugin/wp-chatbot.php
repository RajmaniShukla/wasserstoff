<?php
/*
Plugin Name: WordPress Chatbot
Description: Integrate a chatbot into your WordPress site.
Version: 1.0
Author: Raj Mani Shukla
*/

// Enqueue chatbot script
function wp_chatbot_enqueue_scripts() {
    wp_enqueue_script('chatbot-script', plugins_url('/js/chatbot.js', __FILE__), array('jquery'), null, true);
}
add_action('wp_enqueue_scripts', 'wp_chatbot_enqueue_scripts');

// Shortcode to display the chatbot
function wp_chatbot_shortcode() {
    return '<div id="chatbot"></div>';
}
add_shortcode('chatbot', 'wp_chatbot_shortcode');
?>
