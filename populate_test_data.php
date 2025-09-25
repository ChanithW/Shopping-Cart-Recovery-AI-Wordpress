<?php
/**
 * Manual Cart Test Script
 * This script simulates cart abandonment to populate the analytics dashboard
 */

// This should be run from WordPress admin or via WP-CLI
// For now, let's create a standalone test that populates the database

// Database connection (adjust these to your WordPress DB settings)
$db_host = 'localhost';
$db_name = 'cartdb';  // Your WordPress database name
$db_user = 'root';
$db_pass = '';

try {
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // WordPress table prefix (usually wp_)
    $table_prefix = 'wp_';
    $table_name = $table_prefix . 'cart_logs';
    
    // Create table if it doesn't exist
    $create_table_sql = "CREATE TABLE IF NOT EXISTS $table_name (
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
    )";
    
    $pdo->exec($create_table_sql);
    echo "✅ Table created/verified: $table_name\n";
    
    // Sample cart data to populate the analytics
    $sample_carts = [
        [
            'user_id' => 'user_001',
            'email' => 'john.doe@example.com',
            'items' => json_encode([
                ['product_id' => 1001, 'name' => 'Wireless Headphones', 'price' => 99.99, 'quantity' => 1],
                ['product_id' => 1002, 'name' => 'Phone Case', 'price' => 24.99, 'quantity' => 1]
            ]),
            'abandoned' => 1,
            'email_sent' => 1,
            'opened' => 1,
            'clicked' => 0,
            'converted' => 0
        ],
        [
            'user_id' => 'user_002',
            'email' => 'jane.smith@example.com',
            'items' => json_encode([
                ['product_id' => 2001, 'name' => 'Gaming Mouse', 'price' => 79.99, 'quantity' => 1]
            ]),
            'abandoned' => 1,
            'email_sent' => 1,
            'opened' => 1,
            'clicked' => 1,
            'converted' => 1
        ],
        [
            'user_id' => 'user_003',
            'email' => 'mike.wilson@example.com',
            'items' => json_encode([
                ['product_id' => 3001, 'name' => 'Laptop', 'price' => 1299.99, 'quantity' => 1],
                ['product_id' => 3002, 'name' => 'Laptop Bag', 'price' => 49.99, 'quantity' => 1]
            ]),
            'abandoned' => 1,
            'email_sent' => 1,
            'opened' => 0,
            'clicked' => 0,
            'converted' => 0
        ],
        [
            'user_id' => 'guest_004',
            'email' => 'guest.customer@example.com',
            'items' => json_encode([
                ['product_id' => 4001, 'name' => 'Bluetooth Speaker', 'price' => 59.99, 'quantity' => 2]
            ]),
            'abandoned' => 1,
            'email_sent' => 0,
            'opened' => 0,
            'clicked' => 0,
            'converted' => 0
        ],
        [
            'user_id' => 'user_005',
            'email' => 'sarah.johnson@example.com',
            'items' => json_encode([
                ['product_id' => 5001, 'name' => 'Smartwatch', 'price' => 299.99, 'quantity' => 1]
            ]),
            'abandoned' => 1,
            'email_sent' => 1,
            'opened' => 1,
            'clicked' => 1,
            'converted' => 0
        ]
    ];
    
    // Insert sample data
    $insert_sql = "INSERT INTO $table_name (user_id, email, items, timestamp, abandoned, email_sent, opened, clicked, converted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";
    $stmt = $pdo->prepare($insert_sql);
    
    $inserted_count = 0;
    foreach ($sample_carts as $cart) {
        // Generate timestamps from last 7 days
        $timestamp = date('Y-m-d H:i:s', time() - rand(0, 7 * 24 * 3600));
        
        $success = $stmt->execute([
            $cart['user_id'],
            $cart['email'],
            $cart['items'],
            $timestamp,
            $cart['abandoned'],
            $cart['email_sent'],
            $cart['opened'],
            $cart['clicked'],
            $cart['converted']
        ]);
        
        if ($success) {
            $inserted_count++;
        }
    }
    
    echo "✅ Inserted $inserted_count sample cart records\n";
    
    // Show current stats
    $stats_sql = "SELECT 
        COUNT(*) as total_abandoned,
        SUM(email_sent) as emails_sent,
        SUM(opened) as opened,
        SUM(clicked) as clicked,
        SUM(converted) as converted
        FROM $table_name WHERE abandoned = 1";
    
    $result = $pdo->query($stats_sql);
    $stats = $result->fetch(PDO::FETCH_ASSOC);
    
    echo "\n📊 Current Analytics Stats:\n";
    echo "  Total Abandoned Carts: {$stats['total_abandoned']}\n";
    echo "  Emails Sent: {$stats['emails_sent']}\n";
    echo "  Emails Opened: {$stats['opened']}\n";
    echo "  Links Clicked: {$stats['clicked']}\n";
    echo "  Conversions: {$stats['converted']}\n";
    
    if ($stats['emails_sent'] > 0) {
        $open_rate = round(($stats['opened'] / $stats['emails_sent']) * 100, 2);
        $click_rate = round(($stats['clicked'] / $stats['emails_sent']) * 100, 2);
        $conversion_rate = round(($stats['converted'] / $stats['emails_sent']) * 100, 2);
        
        echo "  Open Rate: {$open_rate}%\n";
        echo "  Click Rate: {$click_rate}%\n";
        echo "  Conversion Rate: {$conversion_rate}%\n";
    }
    
    echo "\n🎉 Sample data populated successfully!\n";
    echo "Now check your WordPress admin at:\n";
    echo "http://localhost/wordpress/wp-admin/admin.php?page=scr-analytics\n";
    
} catch (PDOException $e) {
    echo "❌ Database error: " . $e->getMessage() . "\n";
    echo "\nPlease check your database connection settings:\n";
    echo "- Host: $db_host\n";
    echo "- Database: $db_name\n";
    echo "- User: $db_user\n";
    echo "\nMake sure your WordPress database exists and is accessible.\n";
}
?>