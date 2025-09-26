<?php
/**
 * Plugin Name: Shopping Cart Recovery AI
 * Description: Integrates with Python agents for cart abandonment recovery.
 * Version: 1.0
 * Author: Your Name
 */

if (!defined('ABSPATH')) exit;

define('SCR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('SCR_PLUGIN_URL', plugin_dir_url(__FILE__));

// Include files
require_once SCR_PLUGIN_DIR . 'includes/api_handler.php';
require_once SCR_PLUGIN_DIR . 'includes/tracking.php';
require_once SCR_PLUGIN_DIR . 'admin/analytics.php';

// Hooks
add_action('woocommerce_add_to_cart', 'scr_track_cart');
add_action('woocommerce_cart_updated', 'scr_check_abandonment');
add_action('wp', 'scr_periodic_abandonment_check');
add_action('admin_menu', 'scr_admin_menu');

// Enqueue scripts
add_action('wp_enqueue_scripts', 'scr_enqueue_scripts');

// Activation hook
register_activation_hook(__FILE__, 'scr_activate');

function scr_activate() {
    scr_create_tables();
    // Set default API token if not already set
    if (!get_option('scr_api_token')) {
        update_option('scr_api_token', 'd405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379');
    }
    error_log('SCR: Plugin activated successfully');
}

function scr_create_tables() {
    global $wpdb;
    $table_name = $wpdb->prefix . 'cart_logs';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        user_id varchar(255) DEFAULT '' NOT NULL,
        email varchar(255) DEFAULT '' NOT NULL,
        items text NOT NULL,
        timestamp datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
        abandoned tinyint(1) DEFAULT 0 NOT NULL,
        email_sent tinyint(1) DEFAULT 0 NOT NULL,
        opened tinyint(1) DEFAULT 0 NOT NULL,
        clicked tinyint(1) DEFAULT 0 NOT NULL,
        converted tinyint(1) DEFAULT 0 NOT NULL,
        PRIMARY KEY (id)
    ) $charset_collate;";

    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}

function scr_enqueue_scripts() {
    wp_enqueue_script('scr-tracking', SCR_PLUGIN_URL . 'assets/js/tracking.js', array('jquery'), '1.0', true);
    wp_localize_script('scr-tracking', 'scr_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'is_user_logged_in' => is_user_logged_in()
    ));
}

function scr_admin_menu() {
    add_menu_page('Cart Recovery Analytics', 'Cart Recovery', 'manage_options', 'scr-analytics', 'scr_analytics_page', 'dashicons-chart-line');
}

function scr_analytics_page() {
    scr_display_analytics();
}
?>