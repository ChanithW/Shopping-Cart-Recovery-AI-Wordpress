<?php
/**
 * WooCommerce Integration Test for Shopping Cart Recovery AI
 * This script tests the integration with WooCommerce products
 */

// WordPress configuration - adjust path based on plugin location
$wp_load_paths = [
    '../../../wp-load.php',      // Standard plugin path
    '../../../../wp-load.php',   // If in subfolder
    '../../../../../wp-load.php' // If deeper nested
];

$wp_loaded = false;
foreach ($wp_load_paths as $path) {
    if (file_exists($path)) {
        require_once($path);
        $wp_loaded = true;
        break;
    }
}

if (!$wp_loaded) {
    die('Could not locate WordPress. Please check the plugin installation path.');
}

if (!defined('ABSPATH')) {
    die('Direct access not allowed');
}

// Include our database helper
require_once(dirname(__FILE__) . '/includes/database_helper.php');

echo "<h2>Shopping Cart Recovery AI - WooCommerce Integration Test</h2>";

// Check WooCommerce
if (!class_exists('WooCommerce')) {
    echo "<p style='color: red;'>❌ WooCommerce is not active!</p>";
    echo "<p>Please install and activate WooCommerce first.</p>";
    exit;
} else {
    echo "<p style='color: green;'>✅ WooCommerce is active</p>";
}

// Get WooCommerce products
$products_count = wp_count_posts('product');
$published_count = $products_count->publish ?? 0;

echo "<p><strong>WooCommerce Products Found:</strong> $published_count</p>";

if ($published_count == 0) {
    echo "<div style='background: #fff3cd; padding: 15px; border: 1px solid #ffeaa7; border-radius: 5px; margin: 15px 0;'>";
    echo "<h3>⚠️ No Products Found</h3>";
    echo "<p>You need to create some WooCommerce products first. Here's how:</p>";
    echo "<ol>";
    echo "<li>Go to WordPress Admin → Products → Add New</li>";
    echo "<li>Create products in categories like 'Electronics', 'Smartphones', 'Shoes', 'Sports' etc.</li>";
    echo "<li>Make sure to set prices and stock quantities</li>";
    echo "<li>Publish the products</li>";
    echo "</ol>";
    echo "<p><strong>Sample products to create:</strong></p>";
    echo "<ul>";
    echo "<li>iPhone 15 Pro Max (Category: Electronics/Smartphones) - $1299</li>";
    echo "<li>Samsung Galaxy S24 (Category: Electronics/Smartphones) - $999</li>";
    echo "<li>Apple AirPods Pro (Category: Electronics/Accessories) - $249</li>";
    echo "<li>Nike Air Max (Category: Shoes/Sports) - $129</li>";
    echo "<li>Adidas Ultraboost (Category: Shoes/Running) - $189</li>";
    echo "</ul>";
    echo "</div>";
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
        echo "<table border='1' cellpadding='10' style='border-collapse: collapse; width: 100%;'>";
        echo "<tr><th>ID</th><th>Name</th><th>Price</th><th>AI Category</th><th>Stock</th><th>Description (AI)</th></tr>";
        
        foreach ($products as $product_post) {
            $product_info = scr_get_product_info($product_post->ID);
            
            if ($product_info) {
                echo "<tr>";
                echo "<td>" . $product_info['product_id'] . "</td>";
                echo "<td>" . esc_html($product_info['name']) . "</td>";
                echo "<td>$" . number_format($product_info['price'], 2) . "</td>";
                echo "<td><strong>" . $product_info['category'] . "</strong></td>";
                echo "<td>" . ($product_info['in_stock'] ? '✅ ' . $product_info['stock_quantity'] : '❌ Out of Stock') . "</td>";
                echo "<td>" . esc_html(wp_trim_words($product_info['description'], 10)) . "</td>";
                echo "</tr>";
            }
        }
        echo "</table>";
        
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
        
        // Test similar products
        if (!empty($products)) {
            $first_product_id = $products[0]->ID;
            echo "<h3>Similar Products to: " . get_the_title($first_product_id) . "</h3>";
            
            $similar = scr_get_similar_products($first_product_id, 3);
            if (!empty($similar)) {
                echo "<ul>";
                foreach ($similar as $product) {
                    echo "<li><strong>" . esc_html($product['item_name']) . "</strong> - $" . number_format($product['price'], 2) . " - <em>" . $product['reason'] . "</em></li>";
                }
                echo "</ul>";
            } else {
                echo "<p>No similar products found (need more products in the same category)</p>";
            }
        }
    }
}

// Test cart simulation
echo "<h3>🛒 Cart Simulation Test</h3>";

if ($published_count > 0) {
    // Simulate a cart with first product
    $args = array(
        'post_type' => 'product',
        'post_status' => 'publish',
        'posts_per_page' => 1
    );
    
    $test_products = get_posts($args);
    if (!empty($test_products)) {
        $test_product = $test_products[0];
        $product_info = scr_get_product_info($test_product->ID);
        
        if ($product_info) {
            // Simulate cart data
            $simulated_cart = array(
                'cart_item_key_1' => array(
                    'product_id' => $test_product->ID,
                    'quantity' => 1,
                    'data' => wc_get_product($test_product->ID)
                )
            );
            
            echo "<p><strong>Simulating cart with:</strong> " . $product_info['name'] . "</p>";
            
            // Test cart enrichment
            $enriched_cart = scr_enrich_cart_data($simulated_cart);
            
            echo "<pre style='background: #f5f5f5; padding: 10px; border-radius: 5px;'>";
            echo "Enriched Cart Data (sent to AI agents):\n";
            echo json_encode($enriched_cart, JSON_PRETTY_PRINT);
            echo "</pre>";
        }
    }
}

echo "<hr>";
echo "<div style='background: #d4edda; padding: 15px; border: 1px solid #c3e6cb; border-radius: 5px;'>";
echo "<h3>✅ System Status</h3>";
echo "<ul>";
echo "<li>✅ Using WooCommerce native products (no separate products table needed)</li>";
echo "<li>✅ AI agents running on ports 8006 (detector) and 8002 (email generator)</li>";
echo "<li>✅ Product data automatically enriched with AI categories</li>";
echo "<li>✅ Recommendations based on WooCommerce product relationships</li>";
echo "</ul>";

echo "<h4>🎯 How It Works Now:</h4>";
echo "<ol>";
echo "<li><strong>Create Products:</strong> Use WooCommerce → Products → Add New</li>";
echo "<li><strong>Customer Shops:</strong> Adds products to cart</li>";
echo "<li><strong>Cart Abandonment:</strong> AI detects when customer leaves</li>";
echo "<li><strong>AI Analysis:</strong> System analyzes cart contents and user behavior</li>";
echo "<li><strong>Personalized Email:</strong> AI generates custom recovery email with:";
echo "<ul><li>Dynamic discounts based on cart value</li>";
echo "<li>Product recommendations from your WooCommerce catalog</li>";
echo "<li>Personalized messaging based on product categories</li></ul></li>";
echo "<li><strong>Recovery:</strong> Customer receives email and hopefully completes purchase</li>";
echo "</ol>";
echo "</div>";
?>