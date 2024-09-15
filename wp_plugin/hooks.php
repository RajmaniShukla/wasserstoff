<?php
// Add action hook to call our custom function when a post is saved
add_action('save_post', 'update_embeddings_on_save_post', 10, 3);

function update_embeddings_on_save_post($post_id, $post, $update) {
    // Check if this is an autosave or a revision
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
    if ($post->post_type != 'post') return; // Only update for posts

    // Get the post content
    $text = $post->post_content;

    // Generate embeddings and update vector database
    $embeddings = generate_embeddings($text);
    update_vector_database($post_id, $embeddings);
}

function generate_embeddings($text) {
    // Call external service to generate embeddings (this needs to be implemented)
    // Example placeholder code
    $response = wp_remote_post('https://your-embedding-service.com/generate', array(
        'body' => json_encode(array('text' => $text)),
        'headers' => array(
            'Content-Type' => 'application/json'
        )
    ));
    
    if (is_wp_error($response)) {
        return [];
    }
    
    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    return $data['embeddings'] ?? [];
}

function update_vector_database($post_id, $embeddings) {
    // Call external service or update your database with embeddings (this needs to be implemented)
    // Example placeholder code
    wp_remote_post('https://your-vector-database.com/update', array(
        'body' => json_encode(array(
            'post_id' => $post_id,
            'embeddings' => $embeddings
        )),
        'headers' => array(
            'Content-Type' => 'application/json'
        )
    ));
}
?>