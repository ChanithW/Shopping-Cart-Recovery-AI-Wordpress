<?php
/**
 * Manual setup script for the products table
 * Run this if the plugin activation didn't create the table
 */

// WordPress configuration
require_once('../../../wp-config.php');
require_once('../../../wp-load.php');

if (!defined('ABSPATH')) {
    die('Direct access not allowed');
}

echo "<h2>Shopping Cart Recovery AI - Database Setup</h2>";

// Include our database helper
require_once(dirname(__FILE__) . '/includes/database_helper.php');

// Create products table
echo "<h3>Creating products table...</h3>";
scr_create_products_table();

global $wpdb;
$table_name = $wpdb->prefix . 'products';

// Check if table was created
$table_exists = $wpdb->get_var("SHOW TABLES LIKE '$table_name'") == $table_name;

if ($table_exists) {
    echo "<p style='color: green;'>✓ Products table created successfully!</p>";
    
    // Check if products exist
    $count = $wpdb->get_var("SELECT COUNT(*) FROM $table_name");
    echo "<p>Current products in table: $count</p>";
    
    if ($count == 0) {
        echo "<h3>Populating sample products...</h3>";
        scr_populate_sample_products();
        
        $new_count = $wpdb->get_var("SELECT COUNT(*) FROM $table_name");
        if ($new_count > 0) {
            echo "<p style='color: green;'>✓ Sample products added successfully! ($new_count products)</p>";
        } else {
            echo "<p style='color: red;'>✗ Failed to add sample products</p>";
        }
    }
    
    // Show sample products
    $sample_products = $wpdb->get_results("SELECT item_name, price, category, stock_quantity FROM $table_name LIMIT 10");
    if ($sample_products) {
        echo "<h3>Sample Products:</h3>";
        echo "<table border='1' cellpadding='5'>";
        echo "<tr><th>Name</th><th>Price</th><th>Category</th><th>Stock</th></tr>";
        foreach ($sample_products as $product) {
            echo "<tr>";
            echo "<td>" . esc_html($product->item_name) . "</td>";
            echo "<td>$" . number_format($product->price, 2) . "</td>";
            echo "<td>" . esc_html($product->category) . "</td>";
            echo "<td>" . $product->stock_quantity . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    }
    
} else {
    echo "<p style='color: red;'>✗ Failed to create products table</p>";
    echo "<p>Database error: " . $wpdb->last_error . "</p>";
}

echo "<hr>";
echo "<p><a href='../../../wp-admin/plugins.php'>← Back to Plugins</a></p>";
?>