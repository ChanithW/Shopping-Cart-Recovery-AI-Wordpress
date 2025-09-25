<?php
function scr_call_detector_api($cart_data) {
    $api_url = 'http://localhost:8004/detect-abandonment';  // Updated port
    $token = get_option('scr_api_token', 'd405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379');  // Fallback token

    error_log('SCR: Making API call to: ' . $api_url);
    error_log('SCR: API request data: ' . json_encode($cart_data));

    $response = wp_remote_post($api_url, array(
        'body' => json_encode($cart_data),
        'headers' => array(
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer ' . $token
        ),
        'timeout' => 30  // Increase timeout
    ));

    if (is_wp_error($response)) {
        error_log('SCR API Error: ' . $response->get_error_message());
        return false;
    }

    $response_code = wp_remote_retrieve_response_code($response);
    error_log('SCR: API response code: ' . $response_code);

    $body = wp_remote_retrieve_body($response);
    error_log('SCR: API raw response body: ' . $body);

    $decoded = json_decode($body, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log('SCR API JSON Error: ' . json_last_error_msg());
        return false;
    }

    error_log('SCR: API decoded response: ' . print_r($decoded, true));
    return $decoded;
}

function scr_call_email_api($email_data) {
    $api_url = 'http://localhost:8002/generate-email';  // Adjust
    $token = get_option('scr_api_token', 'd405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379');

    error_log('SCR: Making EMAIL API call to: ' . $api_url);
    error_log('SCR: EMAIL API request data: ' . json_encode($email_data));

    $response = wp_remote_post($api_url, array(
        'body' => json_encode($email_data),
        'headers' => array(
            'Content-Type' => 'application/json',
            'Authorization' => 'Bearer ' . $token
        ),
        'timeout' => 30
    ));

    if (is_wp_error($response)) {
        error_log('SCR Email API Error: ' . $response->get_error_message());
        return false;
    }

    $response_code = wp_remote_retrieve_response_code($response);
    error_log('SCR: EMAIL API response code: ' . $response_code);

    $body = wp_remote_retrieve_body($response);
    error_log('SCR: EMAIL API raw response body: ' . $body);

    $decoded = json_decode($body, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        error_log('SCR Email API JSON Error: ' . json_last_error_msg());
        return false;
    }

    error_log('SCR: EMAIL API decoded response: ' . print_r($decoded, true));
    return $decoded;
}

function scr_check_abandonment() {
    // Add debugging
    error_log('SCR: scr_check_abandonment called');

    $cart = WC()->cart->get_cart();
    error_log('SCR: Cart items count: ' . count($cart));

    if (empty($cart)) {
        error_log('SCR: Cart is empty, returning');
        return;
    }

    $user_id = (string) (get_current_user_id() ?: session_id());

    // Ensure user_id is never empty for API calls
    if (empty($user_id)) {
        $user_id = 'guest_' . time(); // Fallback user ID
        error_log('SCR: Generated fallback user_id: ' . $user_id);
    }

    // Check if we already checked recently (prevent too frequent calls)
    $last_check = get_transient('scr_last_check_' . $user_id);
    if ($last_check && (time() - $last_check) < 30) { // Only check every 30 seconds
        error_log('SCR: Checked recently, skipping');
        return;
    }
    set_transient('scr_last_check_' . $user_id, time(), 300); // 5 minutes

    $email = '';
    if (is_user_logged_in()) {
        $email = wp_get_current_user()->user_email;
    } else {
        // For guest users, try to get email from various sources
        $email = get_transient('scr_guest_email_' . $user_id) ?: '';
        if (empty($email)) {
            // Try to get from WooCommerce session or billing email
            $email = WC()->session->get('billing_email') ?: '';
        }
        if (empty($email)) {
            // Try to get from cart session
            $email = WC()->session->get('guest_email') ?: '';
        }
        if (empty($email)) {
            // Last resort - use a placeholder that will be updated later
            $email = 'guest_' . $user_id . '@temp.local';
            error_log('SCR: No email found for guest user, using placeholder: ' . $email);
        }
    }

    error_log('SCR: User ID: ' . $user_id . ', Email: ' . $email);

    $cart_data = array(
        'user_id' => (string) $user_id,  // Convert to string as expected by API
        'email' => $email,
        'items' => array_values(array_map(function($item) {  // Convert associative array to numeric array
            $product = $item['data'];
            return array(
                'product_id' => (int) $item['product_id'],
                'name' => method_exists($product, 'get_name') ? $product->get_name() : ($item['name'] ?? 'Unknown Product'),
                'price' => method_exists($product, 'get_price') ? (float) $product->get_price() : (float) ($item['line_total'] ?? $item['price'] ?? 0),
                'quantity' => (int) $item['quantity']
            );
        }, $cart)),
        'timestamp' => (float) time(),
        'behavior' => array_map(function($value) {
            return (int) $value;
        }, get_transient('scr_behavior_' . $user_id) ?: array('pages_viewed' => 0, 'idle_time' => 0, 'session_duration' => 0))
    );

    error_log('SCR: Cart data before API call: ' . print_r($cart_data, true));

    $result = scr_call_detector_api($cart_data);
    error_log('SCR: API call result: ' . print_r($result, true));

    if ($result && isset($result['abandoned']) && $result['abandoned']) {
        error_log('SCR: Cart abandoned, calling email API');

        // Check if email already sent for this user/cart session (prevent duplicates)
        $email_sent_key = 'scr_email_sent_' . $user_id . '_' . md5(serialize($cart));
        if (get_transient($email_sent_key)) {
            error_log('SCR: Email already sent for this cart session, skipping');
            return;
        }

        // Call email generator
        $email_user_id = strval($user_id); // Force conversion to string
        error_log('SCR: DEBUG - Original user_id: ' . $user_id . ' (type: ' . gettype($user_id) . ')');
        error_log('SCR: DEBUG - Email user_id: ' . $email_user_id . ' (type: ' . gettype($email_user_id) . ')');
        $email_data = array(
            'user_id' => $email_user_id,
            'email' => $email,
            'name' => wp_get_current_user()->display_name ?: 'Valued Customer',
            'items' => $result['data']['items'],
            'recommendations' => $result['data']['recommendations'],
            'behavior' => $result['data']['behavior'],
            'persona' => scr_determine_persona($user_id)
        );
        error_log('SCR: DEBUG - Final email_data user_id: ' . $email_data['user_id'] . ' (type: ' . gettype($email_data['user_id']) . ')');

        $email_result = scr_call_email_api($email_data);
        error_log('SCR: Email API result: ' . print_r($email_result, true));

        // Mark email as sent (expires in 24 hours)
        if ($email_result && !isset($email_result['detail'])) {
            set_transient($email_sent_key, true, 86400); // 24 hours
            error_log('SCR: Email sent successfully, marked as sent');

            // Log to database for analytics
            global $wpdb;
            $table = $wpdb->prefix . 'cart_logs';
            $items_json = json_encode($cart_data['items']);

            $wpdb->insert(
                $table,
                array(
                    'user_id' => $user_id,
                    'email' => $email,
                    'items' => $items_json,
                    'timestamp' => current_time('mysql'),
                    'abandoned' => 1,
                    'email_sent' => 1,
                    'opened' => 0,
                    'clicked' => 0,
                    'converted' => 0
                ),
                array('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d')
            );

            if ($wpdb->last_error) {
                error_log('SCR: Database insert error: ' . $wpdb->last_error);
            } else {
                error_log('SCR: Cart logged to database with ID: ' . $wpdb->insert_id);
            }
        }
    } else {
        error_log('SCR: Cart not abandoned or API error');
    }
}

function scr_determine_persona($user_id) {
    // Simple: check order count
    if (wc_get_customer_order_count($user_id) > 5) return 'loyal';
    return 'first_time';
}

// AJAX handlers
add_action('wp_ajax_scr_cart_update', 'scr_cart_update_handler');
add_action('wp_ajax_nopriv_scr_cart_update', 'scr_cart_update_handler');

function scr_cart_update_handler() {
    error_log('SCR: AJAX cart update handler called');
    scr_check_abandonment();
    wp_die();
}

add_action('wp_ajax_scr_save_guest_email', 'scr_save_guest_email_handler');
add_action('wp_ajax_nopriv_scr_save_guest_email', 'scr_save_guest_email_handler');

function scr_save_guest_email_handler() {
    $user_id = get_current_user_id() ?: session_id();
    $email = sanitize_email($_POST['email']);

    if ($email) {
        // Store guest email for 24 hours
        set_transient('scr_guest_email_' . $user_id, $email, 86400); // 24 hours
        error_log('SCR: Guest email saved: ' . $email . ' for user: ' . $user_id);
    }

    wp_die();
}

add_action('wp_ajax_scr_update_behavior', 'scr_update_behavior_handler');
add_action('wp_ajax_nopriv_scr_update_behavior', 'scr_update_behavior_handler');

function scr_update_behavior_handler() {
    $user_id = get_current_user_id() ?: session_id();
    $idle_time = intval($_POST['idle_time']);
    $pages_viewed = intval($_POST['pages_viewed']);
    $session_duration = intval($_POST['session_duration']);

    set_transient('scr_behavior_' . $user_id, array(
        'idle_time' => $idle_time,
        'pages_viewed' => $pages_viewed,
        'session_duration' => $session_duration
    ), 3600); // 1 hour

    wp_die();
}
?>