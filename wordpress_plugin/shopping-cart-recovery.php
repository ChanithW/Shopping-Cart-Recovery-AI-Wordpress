<?php
/**
 * Plugin Name: Shopping Cart Recovery AI
 * Description: Integrates with Python agents for cart abandonment recovery.
 * Version: 1.0
 * Author: Your Name
 * Plugin URI: https://github.com/ChanithW/Shopping-Cart-Recovery-AI-Wordpress
 */

if (!defined('ABSPATH')) exit;

define('SCR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('SCR_PLUGIN_URL', plugin_dir_url(__FILE__));

// Include files
require_once SCR_PLUGIN_DIR . 'includes/api_handler.php';
require_once SCR_PLUGIN_DIR . 'includes/tracking.php';
require_once SCR_PLUGIN_DIR . 'includes/database_helper.php';
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
    scr_init_woocommerce_integration();  // Initialize WooCommerce integration
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
    add_submenu_page('scr-analytics', 'WooCommerce Test', 'WooCommerce Test', 'manage_options', 'scr-woocommerce-test', 'scr_woocommerce_test_page');
    add_submenu_page('scr-analytics', 'System Status', 'System Status', 'manage_options', 'scr-system-status', 'scr_system_status_page');
}

function scr_analytics_page() {
    scr_display_analytics();
}

function scr_woocommerce_test_page() {
    ?>
    <div class="wrap">
        <h1>WooCommerce Integration Test</h1>
        
        <?php
        // Include our database helper
        require_once SCR_PLUGIN_DIR . 'includes/database_helper.php';
        
        // Check WooCommerce
        if (!class_exists('WooCommerce')) {
            echo '<div class="notice notice-error"><p><strong>❌ WooCommerce is not active!</strong><br>Please install and activate WooCommerce first.</p></div>';
            return;
        } else {
            echo '<div class="notice notice-success"><p><strong>✅ WooCommerce is active</strong></p></div>';
        }
        
        // Get WooCommerce products
        $products_count = wp_count_posts('product');
        $published_count = $products_count->publish ?? 0;
        
        echo "<p><strong>WooCommerce Products Found:</strong> $published_count</p>";
        
        if ($published_count == 0) {
            ?>
            <div class="notice notice-warning">
                <h3>⚠️ No Products Found</h3>
                <p>You need to create some WooCommerce products first. Here's how:</p>
                <ol>
                    <li>Go to <strong>Products → Add New</strong></li>
                    <li>Create products in categories like 'Electronics', 'Smartphones', 'Shoes', 'Sports' etc.</li>
                    <li>Make sure to set prices and stock quantities</li>
                    <li>Publish the products</li>
                </ol>
                <p><strong>Sample products to create:</strong></p>
                <ul>
                    <li>iPhone 15 Pro Max (Category: Electronics/Smartphones) - $1299</li>
                    <li>Samsung Galaxy S24 (Category: Electronics/Smartphones) - $999</li>
                    <li>Apple AirPods Pro (Category: Electronics/Accessories) - $249</li>
                    <li>Nike Air Max (Category: Shoes/Sports) - $129</li>
                    <li>Adidas Ultraboost (Category: Shoes/Running) - $189</li>
                </ul>
            </div>
            <?php
        } else {
            // Test our functions with real WooCommerce products
            echo "<h3>Testing Product Integration</h3>";
            
            // Get first 5 products
            $args = array(
                'post_type' => 'product',
                'post_status' => 'publish',
                'posts_per_page' => 5
            );
            
            $products = get_posts($args);
            
            if (!empty($products)) {
                ?>
                <table class="wp-list-table widefat fixed striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Price</th>
                            <th>AI Category</th>
                            <th>Stock</th>
                            <th>Description (AI)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        foreach ($products as $product_post) {
                            $product_info = scr_get_product_info($product_post->ID);
                            
                            if ($product_info) {
                                ?>
                                <tr>
                                    <td><?php echo $product_info['product_id']; ?></td>
                                    <td><strong><?php echo esc_html($product_info['name']); ?></strong></td>
                                    <td>$<?php echo number_format($product_info['price'], 2); ?></td>
                                    <td><span class="badge" style="background: #0073aa; color: white; padding: 3px 8px; border-radius: 3px;"><?php echo $product_info['category']; ?></span></td>
                                    <td><?php echo $product_info['in_stock'] ? '✅ ' . $product_info['stock_quantity'] : '❌ Out of Stock'; ?></td>
                                    <td><?php echo esc_html(wp_trim_words($product_info['description'], 10)); ?></td>
                                </tr>
                                <?php
                            }
                        }
                        ?>
                    </tbody>
                </table>
                
                <?php
                // Test popular products function
                echo "<h3>Popular Products (AI Recommendations)</h3>";
                $popular = scr_get_popular_products(3);
                
                if (!empty($popular)) {
                    echo "<ul>";
                    foreach ($popular as $product) {
                        echo "<li><strong>" . esc_html($product['item_name']) . "</strong> - $" . number_format($product['price'], 2) . " (Category: " . $product['category'] . ")</li>";
                    }
                    echo "</ul>";
                }
            }
        }
        ?>
    </div>
    <?php
}

function scr_system_status_page() {
    ?>
    <div class="wrap">
        <h1>System Status</h1>
        
        <?php
        // Check agents status - try multiple ports
        $detector_ports = [8005, 8006, 8001];
        $email_ports = [8002, 8003];
        
        $detector_status = false;
        $detector_port = 'Not detected';
        foreach ($detector_ports as $port) {
            if (@file_get_contents("http://localhost:$port/docs") !== false || @file_get_contents("http://localhost:$port/") !== false) {
                $detector_status = true;
                $detector_port = "Port $port";
                break;
            }
        }
        
        $email_status = false;
        $email_port = 'Not detected';
        foreach ($email_ports as $port) {
            if (@file_get_contents("http://localhost:$port/docs") !== false || @file_get_contents("http://localhost:$port/") !== false) {
                $email_status = true;
                $email_port = "Port $port";
                break;
            }
        }
        ?>
        
        <table class="form-table">
            <tr>
                <th>WooCommerce</th>
                <td><?php echo class_exists('WooCommerce') ? '✅ Active' : '❌ Not Active'; ?></td>
            </tr>
            <tr>
                <th>Abandonment Detector Agent</th>
                <td><?php echo $detector_status ? "✅ Running ($detector_port)" : '❌ Not Running'; ?></td>
            </tr>
            <tr>
                <th>Email Generator Agent</th>
                <td><?php echo $email_status ? "✅ Running ($email_port)" : '❌ Not Running'; ?></td>
            </tr>
            <tr>
                <th>Products</th>
                <td>
                    <?php
                    $products_count = wp_count_posts('product');
                    $published_count = $products_count->publish ?? 0;
                    echo "$published_count WooCommerce products";
                    ?>
                </td>
            </tr>
            <tr>
                <th>Cart Logs Table</th>
                <td>
                    <?php
                    global $wpdb;
                    $table_name = $wpdb->prefix . 'cart_logs';
                    $table_exists = $wpdb->get_var("SHOW TABLES LIKE '$table_name'") == $table_name;
                    echo $table_exists ? '✅ Exists' : '❌ Missing';
                    ?>
                </td>
            </tr>
        </table>
        
        <h3>🎯 How The System Works:</h3>
        <ol>
            <li><strong>Create Products:</strong> Use WooCommerce → Products → Add New</li>
            <li><strong>Customer Shops:</strong> Adds products to cart</li>
            <li><strong>Cart Abandonment:</strong> AI detects when customer leaves</li>
            <li><strong>AI Analysis:</strong> System analyzes cart contents and user behavior</li>
            <li><strong>Personalized Email:</strong> AI generates custom recovery email</li>
            <li><strong>Recovery:</strong> Customer receives email and hopefully completes purchase</li>
        </ol>
        
        <?php if (!$detector_status || !$email_status): ?>
            <div class="notice notice-error">
                <p><strong>⚠️ AI Agents Not Running</strong></p>
                <p>To start the agents, run these commands in your terminal:</p>
                <pre style="background: #f1f1f1; padding: 10px; border-radius: 5px;">
python -m uvicorn agents.abandonment_detector.app:app --host 0.0.0.0 --port 8006
python -m uvicorn agents.email_generator_offer_suggestor.app:app --host 0.0.0.0 --port 8002
                </pre>
            </div>
        <?php endif; ?>
    </div>
    <?php
}
?>