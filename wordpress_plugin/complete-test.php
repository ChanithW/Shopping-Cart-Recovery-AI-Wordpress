<?php
/**
 * Complete System Test for Shopping Cart Recovery AI
 * This tests the entire flow from WordPress to AI agents
 */

// Load WordPress
$wp_paths = [
    __DIR__ . '/../../../../wp-load.php',
    __DIR__ . '/../../../wp-load.php',
    __DIR__ . '/../../wp-load.php'
];

foreach ($wp_paths as $path) {
    if (file_exists($path)) {
        require_once($path);
        break;
    }
}

if (!defined('ABSPATH')) {
    die('WordPress not found. Please check your installation.');
}

// Include our functions
require_once(__DIR__ . '/includes/database_helper.php');
require_once(__DIR__ . '/includes/api_handler.php');

?>
<!DOCTYPE html>
<html>
<head>
    <title>Shopping Cart Recovery AI - Complete System Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .test-section { margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        .warning { color: orange; font-weight: bold; }
        .info { color: blue; font-weight: bold; }
        table { border-collapse: collapse; width: 100%; margin: 15px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
        .badge { background: #0073aa; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.9em; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto; }
        .test-pass { background: #d4edda; border-left: 5px solid #28a745; }
        .test-fail { background: #f8d7da; border-left: 5px solid #dc3545; }
        .test-warning { background: #fff3cd; border-left: 5px solid #ffc107; }
    </style>
</head>
<body>
    <h1>🧪 Complete System Test - Shopping Cart Recovery AI</h1>
    
    <?php
    $all_tests_passed = true;
    $test_results = [];
    
    // Test 1: WordPress & WooCommerce
    echo "<div class='test-section'>";
    echo "<h2>📋 Test 1: WordPress & WooCommerce Setup</h2>";
    
    $wp_version = get_bloginfo('version');
    echo "<p><strong>WordPress Version:</strong> $wp_version</p>";
    
    if (class_exists('WooCommerce')) {
        $wc_version = WC()->version ?? 'Unknown';
        echo "<p class='success'>✅ WooCommerce Active (Version: $wc_version)</p>";
        $test_results['woocommerce'] = true;
    } else {
        echo "<p class='error'>❌ WooCommerce Not Active</p>";
        $test_results['woocommerce'] = false;
        $all_tests_passed = false;
    }
    
    $products_count = wp_count_posts('product');
    $published_count = $products_count->publish ?? 0;
    
    if ($published_count > 0) {
        echo "<p class='success'>✅ WooCommerce Products Found: $published_count</p>";
        $test_results['products'] = true;
    } else {
        echo "<p class='error'>❌ No WooCommerce Products Found</p>";
        $test_results['products'] = false;
        $all_tests_passed = false;
    }
    echo "</div>";
    
    // Test 2: Database Tables
    echo "<div class='test-section'>";
    echo "<h2>🗄️ Test 2: Database Tables</h2>";
    
    global $wpdb;
    $cart_logs_table = $wpdb->prefix . 'cart_logs';
    $table_exists = $wpdb->get_var("SHOW TABLES LIKE '$cart_logs_table'") == $cart_logs_table;
    
    if ($table_exists) {
        echo "<p class='success'>✅ Cart Logs Table Exists: $cart_logs_table</p>";
        $test_results['database'] = true;
        
        $log_count = $wpdb->get_var("SELECT COUNT(*) FROM $cart_logs_table");
        echo "<p><strong>Cart Log Entries:</strong> $log_count</p>";
    } else {
        echo "<p class='error'>❌ Cart Logs Table Missing: $cart_logs_table</p>";
        $test_results['database'] = false;
        $all_tests_passed = false;
    }
    echo "</div>";
    
    // Test 3: AI Agents Status
    echo "<div class='test-section'>";
    echo "<h2>🤖 Test 3: AI Agents Status</h2>";
    
    function test_agent_connection($port, $name) {
        $urls_to_try = [
            "http://localhost:$port/docs",
            "http://localhost:$port/",
            "http://127.0.0.1:$port/docs",
            "http://127.0.0.1:$port/"
        ];
        
        foreach ($urls_to_try as $url) {
            $context = stream_context_create([
                'http' => [
                    'timeout' => 3,
                    'method' => 'GET',
                    'ignore_errors' => true
                ]
            ]);
            
            $response = @file_get_contents($url, false, $context);
            if ($response !== false) {
                return ['status' => true, 'url' => $url, 'response' => substr($response, 0, 200)];
            }
        }
        return ['status' => false, 'url' => null, 'response' => null];
    }
    
    // Test Abandonment Detector
    $detector_ports = [8005, 8006, 8001];
    $detector_found = false;
    $detector_port = null;
    
    foreach ($detector_ports as $port) {
        $result = test_agent_connection($port, 'Abandonment Detector');
        if ($result['status']) {
            echo "<p class='success'>✅ Abandonment Detector Running on Port $port</p>";
            $detector_found = true;
            $detector_port = $port;
            break;
        }
    }
    
    if (!$detector_found) {
        echo "<p class='error'>❌ Abandonment Detector Not Found (tried ports: " . implode(', ', $detector_ports) . ")</p>";
        $all_tests_passed = false;
    }
    
    // Test Email Generator
    $email_ports = [8002, 8003];
    $email_found = false;
    $email_port = null;
    
    foreach ($email_ports as $port) {
        $result = test_agent_connection($port, 'Email Generator');
        if ($result['status']) {
            echo "<p class='success'>✅ Email Generator Running on Port $port</p>";
            $email_found = true;
            $email_port = $port;
            break;
        }
    }
    
    if (!$email_found) {
        echo "<p class='error'>❌ Email Generator Not Found (tried ports: " . implode(', ', $email_ports) . ")</p>";
        $all_tests_passed = false;
    }
    
    $test_results['agents'] = ($detector_found && $email_found);
    echo "</div>";
    
    // Test 4: Product Data Processing
    if ($published_count > 0) {
        echo "<div class='test-section'>";
        echo "<h2>📦 Test 4: Product Data Processing</h2>";
        
        $test_product_args = array(
            'post_type' => 'product',
            'post_status' => 'publish',
            'posts_per_page' => 1
        );
        
        $test_products = get_posts($test_product_args);
        if (!empty($test_products)) {
            $test_product = $test_products[0];
            $product_info = scr_get_product_info($test_product->ID);
            
            if ($product_info) {
                echo "<p class='success'>✅ Product Data Processing Working</p>";
                echo "<p><strong>Test Product:</strong> {$product_info['name']}</p>";
                echo "<p><strong>AI Category:</strong> <span class='badge'>{$product_info['category']}</span></p>";
                echo "<p><strong>Price:</strong> $" . number_format($product_info['price'], 2) . "</p>";
                $test_results['product_processing'] = true;
            } else {
                echo "<p class='error'>❌ Product Data Processing Failed</p>";
                $test_results['product_processing'] = false;
                $all_tests_passed = false;
            }
        }
        echo "</div>";
    }
    
    // Test 5: Cart Simulation & API Calls
    if ($published_count > 0 && $detector_found && $email_found) {
        echo "<div class='test-section'>";
        echo "<h2>🛒 Test 5: Cart Simulation & API Integration</h2>";
        
        $test_product = $test_products[0];
        $product_info = scr_get_product_info($test_product->ID);
        
        if ($product_info) {
            // Simulate cart data
            $simulated_cart = array(
                'cart_item_key_1' => array(
                    'product_id' => $test_product->ID,
                    'quantity' => 2,
                    'data' => wc_get_product($test_product->ID)
                )
            );
            
            // Test cart enrichment
            $enriched_cart = scr_enrich_cart_data($simulated_cart);
            
            if (!empty($enriched_cart)) {
                echo "<p class='success'>✅ Cart Data Enrichment Working</p>";
                echo "<p><strong>Enriched Cart Items:</strong> " . count($enriched_cart) . "</p>";
                
                // Test API call to abandonment detector
                echo "<h4>Testing Abandonment Detector API...</h4>";
                
                $cart_data = array(
                    'user_id' => 'test_user_123',
                    'email' => 'test@example.com',
                    'items' => $enriched_cart,
                    'timestamp' => time(),
                    'behavior' => array('pages_viewed' => 5, 'idle_time' => 120, 'session_duration' => 600)
                );
                
                $api_result = scr_call_detector_api($cart_data);
                
                if ($api_result && isset($api_result['abandoned'])) {
                    echo "<p class='success'>✅ Abandonment Detection API Working</p>";
                    echo "<p><strong>API Response:</strong> " . ($api_result['abandoned'] ? 'Cart Abandoned' : 'Cart Active') . "</p>";
                    
                    // Test email generation if abandoned
                    if ($api_result['abandoned']) {
                        echo "<h4>Testing Email Generation API...</h4>";
                        
                        $email_data = array(
                            'user_id' => 'test_user_123',
                            'email' => 'test@example.com',
                            'name' => 'Test Customer',
                            'items' => $api_result['data']['items'] ?? $enriched_cart,
                            'recommendations' => $api_result['data']['recommendations'] ?? array(),
                            'behavior' => array('pages_viewed' => 5, 'idle_time' => 120, 'session_duration' => 600),
                            'persona' => scr_determine_persona('test_user_123')
                        );
                        
                        $email_result = scr_call_email_api($email_data);
                        
                        if ($email_result && isset($email_result['subject'])) {
                            echo "<p class='success'>✅ Email Generation API Working</p>";
                            echo "<p><strong>Generated Subject:</strong> " . esc_html($email_result['subject']) . "</p>";
                            echo "<p><strong>Email Length:</strong> " . strlen($email_result['body']) . " characters</p>";
                            $test_results['api_integration'] = true;
                        } else {
                            echo "<p class='error'>❌ Email Generation API Failed</p>";
                            echo "<p><strong>Error:</strong> " . (is_array($email_result) ? json_encode($email_result) : 'No response') . "</p>";
                            $test_results['api_integration'] = false;
                            $all_tests_passed = false;
                        }
                    } else {
                        echo "<p class='info'>ℹ️ Cart not flagged as abandoned, skipping email test</p>";
                        $test_results['api_integration'] = true;
                    }
                } else {
                    echo "<p class='error'>❌ Abandonment Detection API Failed</p>";
                    echo "<p><strong>Response:</strong> " . json_encode($api_result) . "</p>";
                    $test_results['api_integration'] = false;
                    $all_tests_passed = false;
                }
            } else {
                echo "<p class='error'>❌ Cart Data Enrichment Failed</p>";
                $test_results['api_integration'] = false;
                $all_tests_passed = false;
            }
        }
        echo "</div>";
    }
    
    // Test Summary
    echo "<div class='test-section " . ($all_tests_passed ? 'test-pass' : 'test-fail') . "'>";
    echo "<h2>📊 Test Summary</h2>";
    
    if ($all_tests_passed) {
        echo "<h3 class='success'>🎉 All Tests Passed! System is Fully Operational</h3>";
        echo "<p>Your Shopping Cart Recovery AI system is working correctly and ready to handle real cart abandonment scenarios.</p>";
    } else {
        echo "<h3 class='error'>⚠️ Some Tests Failed</h3>";
        echo "<p>Please review the failed tests above and fix the issues before using the system in production.</p>";
    }
    
    echo "<table>";
    echo "<tr><th>Component</th><th>Status</th></tr>";
    
    $test_labels = [
        'woocommerce' => 'WooCommerce Active',
        'products' => 'Products Available', 
        'database' => 'Database Tables',
        'agents' => 'AI Agents Running',
        'product_processing' => 'Product Processing',
        'api_integration' => 'API Integration'
    ];
    
    foreach ($test_labels as $key => $label) {
        $status = isset($test_results[$key]) && $test_results[$key];
        $status_text = $status ? '<span class="success">✅ Pass</span>' : '<span class="error">❌ Fail</span>';
        echo "<tr><td>$label</td><td>$status_text</td></tr>";
    }
    echo "</table>";
    echo "</div>";
    
    // Next Steps
    echo "<div class='test-section'>";
    echo "<h2>🚀 Next Steps</h2>";
    
    if ($all_tests_passed) {
        ?>
        <h3>✅ System Ready! Here's how to use it:</h3>
        <ol>
            <li><strong>Real Testing:</strong> Add products to cart on your WooCommerce site and abandon them</li>
            <li><strong>Monitor Logs:</strong> Check WordPress debug.log for API calls and responses</li>
            <li><strong>View Analytics:</strong> Go to WordPress Admin → Cart Recovery → Analytics</li>
            <li><strong>Customize:</strong> Adjust abandonment thresholds and email templates as needed</li>
        </ol>
        
        <h4>🎯 Test the Real Flow:</h4>
        <ol>
            <li>Open your WooCommerce shop in an incognito browser</li>
            <li>Add products to cart (mix of electronics and shoes for different personas)</li>
            <li>Stay idle for 60+ seconds or navigate away</li>
            <li>Check your email for recovery messages</li>
            <li>Monitor the cart_logs table for tracking data</li>
        </ol>
        <?php
    } else {
        ?>
        <h3>⚠️ Fix These Issues First:</h3>
        <ul>
            <?php
            if (!$test_results['woocommerce']) echo "<li>Install and activate WooCommerce plugin</li>";
            if (!$test_results['products']) echo "<li>Create some WooCommerce products</li>";
            if (!$test_results['database']) echo "<li>Reactivate the plugin to create database tables</li>";
            if (!$test_results['agents']) echo "<li>Start the AI agents using the terminal commands</li>";
            ?>
        </ul>
        
        <h4>🔧 Agent Startup Commands:</h4>
        <pre>python -m uvicorn agents.abandonment_detector.app:app --host 0.0.0.0 --port 8006
python -m uvicorn agents.email_generator_offer_suggestor.app:app --host 0.0.0.0 --port 8002</pre>
        <?php
    }
    echo "</div>";
    ?>
    
    <hr>
    <p><small>Test completed at <?php echo date('Y-m-d H:i:s'); ?></small></p>
    
</body>
</html>