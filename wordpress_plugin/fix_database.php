<?php
/**
 * Quick database fix script
 * This will check your WordPress table prefix and create the correct table
 */

// WordPress configuration
require_once('../../../wp-config.php');
require_once('../../../wp-load.php');

if (!defined('ABSPATH')) {
    die('Direct access not allowed');
}

global $wpdb;

echo "<h2>Shopping Cart Recovery - Database Fix</h2>";
echo "<p>Your WordPress table prefix: <strong>" . $wpdb->prefix . "</strong></p>";

$correct_table_name = $wpdb->prefix . 'products';
echo "<p>Correct table name should be: <strong>$correct_table_name</strong></p>";

// Check if table exists
$table_exists = $wpdb->get_var("SHOW TABLES LIKE '$correct_table_name'") == $correct_table_name;

if ($table_exists) {
    echo "<p style='color: green;'>✓ Table exists!</p>";
    
    $count = $wpdb->get_var("SELECT COUNT(*) FROM $correct_table_name");
    echo "<p>Products in table: $count</p>";
    
} else {
    echo "<p style='color: red;'>✗ Table does not exist. Creating it now...</p>";
    
    // Create table with correct name
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $correct_table_name (
        id int(11) NOT NULL AUTO_INCREMENT,
        item_name varchar(255) NOT NULL,
        description text NOT NULL,
        price decimal(10,2) NOT NULL,
        category varchar(100) NOT NULL,
        stock_status enum('in_stock','out_of_stock') DEFAULT 'in_stock',
        stock_quantity int(11) DEFAULT 0,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP,
        updated_at timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY idx_category (category),
        KEY idx_stock_status (stock_status),
        KEY idx_price (price)
    ) $charset_collate;";
    
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
    
    // Check if it was created
    $table_exists = $wpdb->get_var("SHOW TABLES LIKE '$correct_table_name'") == $correct_table_name;
    
    if ($table_exists) {
        echo "<p style='color: green;'>✓ Table created successfully!</p>";
        
        // Insert sample data
        echo "<p>Inserting sample products...</p>";
        
        $sample_products = [
            ['iPhone 15 Pro Max 256GB', 'Experience the ultimate iPhone with titanium design, advanced camera system, and A17 Pro chip for unmatched performance.', 1299.99, 'smartphone', 45],
            ['Samsung Galaxy S24 Ultra 512GB', 'Premium Android flagship with S Pen, 200MP camera, AI-enhanced photography, and stunning 6.8-inch Dynamic AMOLED display.', 1399.99, 'smartphone', 29],
            ['Apple AirPods Pro 2nd Gen', 'Premium wireless earbuds with active noise cancellation, spatial audio, and personalized listening experience.', 249.99, 'smartphone', 128],
            ['Nike Air Zoom Pegasus 40', 'Iconic running shoe with responsive Zoom Air units, breathable mesh upper, and reliable traction for daily miles.', 129.99, 'shoes', 87],
            ['Adidas Ultraboost 23', 'Energy-returning running shoe with BOOST midsole, Primeknit upper, and Continental rubber outsole for superior grip.', 189.99, 'shoes', 64],
            ['Nike Air Force 1 07', 'Classic basketball-inspired sneaker with leather upper, Air-Sole cushioning, and timeless court-ready style.', 109.99, 'shoes', 156]
        ];
        
        foreach ($sample_products as $product) {
            $wpdb->insert(
                $correct_table_name,
                [
                    'item_name' => $product[0],
                    'description' => $product[1],
                    'price' => $product[2],
                    'category' => $product[3],
                    'stock_status' => 'in_stock',
                    'stock_quantity' => $product[4]
                ],
                ['%s', '%s', '%f', '%s', '%s', '%d']
            );
        }
        
        $count = $wpdb->get_var("SELECT COUNT(*) FROM $correct_table_name");
        echo "<p style='color: green;'>✓ Inserted $count sample products!</p>";
        
    } else {
        echo "<p style='color: red;'>✗ Failed to create table. Error: " . $wpdb->last_error . "</p>";
    }
}

// Show sample data
if ($table_exists) {
    $sample_products = $wpdb->get_results("SELECT * FROM $correct_table_name LIMIT 5");
    if ($sample_products) {
        echo "<h3>Sample Products:</h3>";
        echo "<table border='1' cellpadding='5' style='border-collapse: collapse;'>";
        echo "<tr><th>ID</th><th>Name</th><th>Price</th><th>Category</th><th>Stock</th></tr>";
        foreach ($sample_products as $product) {
            echo "<tr>";
            echo "<td>" . $product->id . "</td>";
            echo "<td>" . esc_html($product->item_name) . "</td>";
            echo "<td>$" . number_format($product->price, 2) . "</td>";
            echo "<td>" . esc_html($product->category) . "</td>";
            echo "<td>" . $product->stock_quantity . "</td>";
            echo "</tr>";
        }
        echo "</table>";
    }
}

echo "<hr><p><strong>Next Steps:</strong></p>";
echo "<ol>";
echo "<li>The table is now created with the correct WordPress prefix</li>";
echo "<li>Your agents are running on ports 8006 (detector) and 8002 (email generator)</li>";
echo "<li>Test the system by adding items to cart in WooCommerce</li>";
echo "</ol>";
?>