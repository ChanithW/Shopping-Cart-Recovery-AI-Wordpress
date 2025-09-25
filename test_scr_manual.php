<?php
/**
 * Test script to manually trigger abandonment check
 * Run this from WordPress root directory: php test_scr_manual.php
 */

require_once('wp-load.php');

if (!function_exists('WC')) {
    echo "WooCommerce not active!\n";
    exit(1);
}

// Simulate cart data
$cart_items = array(
    array(
        'product_id' => 1,
        'variation_id' => 0,
        'quantity' => 2,
        'line_total' => 50.00,
        'data' => (object) array('get_name' => function() { return 'Test Product'; })
    )
);

// Mock WC()->cart
class MockCart {
    public function get_cart() {
        return array(
            'item1' => array(
                'product_id' => 1,
                'variation_id' => 0,
                'quantity' => 2,
                'line_total' => 50.00,
                'data' => (object) array('get_name' => function() { return 'Test Product'; })
            )
        );
    }
}

$original_cart = WC()->cart;
WC()->cart = new MockCart();

// Include our plugin
require_once('wp-content/plugins/shopping-cart-recovery/includes/api_handler.php');

echo "Testing abandonment check...\n";
scr_check_abandonment();

echo "Test completed. Check debug logs.\n";

// Restore original cart
WC()->cart = $original_cart;