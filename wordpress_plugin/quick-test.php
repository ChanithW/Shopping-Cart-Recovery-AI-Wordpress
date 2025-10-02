<?php
/**
 * Plugin Name: SCR Quick Test
 * Description: Quick test page accessible via URL
 */

// Handle the test page request
if (isset($_GET['scr_test']) && $_GET['scr_test'] === 'woocommerce') {
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
    ?>
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shopping Cart Recovery AI - WooCommerce Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            .success { color: green; font-weight: bold; }
            .error { color: red; font-weight: bold; }
            .warning { color: orange; font-weight: bold; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .badge { background: #0073aa; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.9em; }
            .notice { padding: 15px; border-radius: 5px; margin: 15px 0; }
            .notice-success { background: #d4edda; border: 1px solid #c3e6cb; }
            .notice-error { background: #f8d7da; border: 1px solid #f5c6cb; }
            .notice-warning { background: #fff3cd; border: 1px solid #ffeaa7; }
        </style>
    </head>
    <body>
        <h1>🚀 Shopping Cart Recovery AI - WooCommerce Integration Test</h1>
        
        <?php
        // Check WooCommerce
        if (!class_exists('WooCommerce')) {
            echo '<div class="notice notice-error"><p class="error">❌ WooCommerce is not active!</p><p>Please install and activate WooCommerce first.</p></div>';
            exit;
        } else {
            echo '<div class="notice notice-success"><p class="success">✅ WooCommerce is active and ready!</p></div>';
        }
        
        // Get WooCommerce products
        $products_count = wp_count_posts('product');
        $published_count = $products_count->publish ?? 0;
        
        echo "<p><strong>WooCommerce Products Found:</strong> $published_count</p>";
        
        if ($published_count == 0) {
            ?>
            <div class="notice notice-warning">
                <h3 class="warning">⚠️ No Products Found</h3>
                <p>You need to create some WooCommerce products first. Here's how:</p>
                <ol>
                    <li>Go to WordPress Admin → <strong>Products → Add New</strong></li>
                    <li>Create products in categories like 'Electronics', 'Smartphones', 'Shoes', 'Sports' etc.</li>
                    <li>Make sure to set prices and stock quantities</li>
                    <li>Publish the products</li>
                </ol>
                <h4>Sample products to create:</h4>
                <ul>
                    <li>iPhone 15 Pro Max (Category: Electronics) - $1299</li>
                    <li>Samsung Galaxy S24 (Category: Electronics) - $999</li>
                    <li>Nike Air Max (Category: Shoes) - $129</li>
                    <li>Adidas Ultraboost (Category: Shoes) - $189</li>
                </ul>
                <p><a href="<?php echo admin_url('post-new.php?post_type=product'); ?>" target="_blank">Create Products Now →</a></p>
            </div>
            <?php
        } else {
            // Test our functions with real WooCommerce products
            echo "<h2>✅ Product Integration Test Results</h2>";
            
            // Get first 5 products
            $args = array(
                'post_type' => 'product',
                'post_status' => 'publish',
                'posts_per_page' => 5
            );
            
            $products = get_posts($args);
            
            if (!empty($products)) {
                ?>
                <table>
                    <thead>
                        <tr>
                            <th>Product ID</th>
                            <th>Product Name</th>
                            <th>Price</th>
                            <th>AI Category</th>
                            <th>Stock Status</th>
                            <th>AI Description</th>
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
                                    <td><span class="badge"><?php echo $product_info['category']; ?></span></td>
                                    <td><?php echo $product_info['in_stock'] ? '✅ In Stock (' . $product_info['stock_quantity'] . ')' : '❌ Out of Stock'; ?></td>
                                    <td><?php echo esc_html(wp_trim_words($product_info['description'], 8)); ?></td>
                                </tr>
                                <?php
                            }
                        }
                        ?>
                    </tbody>
                </table>
                
                <?php
                // Test cart simulation
                $test_product = $products[0];
                $product_info = scr_get_product_info($test_product->ID);
                
                if ($product_info) {
                    echo "<h3>🛒 Cart Simulation Test</h3>";
                    echo "<p><strong>Simulating abandoned cart with:</strong> " . $product_info['name'] . "</p>";
                    
                    // Simulate cart data
                    $simulated_cart = array(
                        'cart_item_key_1' => array(
                            'product_id' => $test_product->ID,
                            'quantity' => 1,
                            'data' => wc_get_product($test_product->ID)
                        )
                    );
                    
                    // Test cart enrichment
                    $enriched_cart = scr_enrich_cart_data($simulated_cart);
                    
                    echo "<h4>📦 Enriched Cart Data (sent to AI agents):</h4>";
                    echo "<pre style='background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto;'>";
                    echo json_encode($enriched_cart, JSON_PRETTY_PRINT);
                    echo "</pre>";
                }
            }
        }
        
        // Check agents status
        echo "<h2>🤖 AI Agents Status</h2>";
        
        // Try multiple ports and endpoints
        $detector_ports = [8005, 8006, 8001];
        $email_ports = [8002, 8003];
        
        $detector_status = false;
        $detector_port = null;
        foreach ($detector_ports as $port) {
            $response = @file_get_contents("http://localhost:$port/docs");
            if ($response !== false || @file_get_contents("http://localhost:$port/") !== false) {
                $detector_status = true;
                $detector_port = $port;
                break;
            }
        }
        
        $email_status = false;
        $email_port = null;
        foreach ($email_ports as $port) {
            $response = @file_get_contents("http://localhost:$port/docs");
            if ($response !== false || @file_get_contents("http://localhost:$port/") !== false) {
                $email_status = true;
                $email_port = $port;
                break;
            }
        }
        
        echo "<table>";
        echo "<tr><th>Component</th><th>Status</th><th>Details</th></tr>";
        echo "<tr><td>Abandonment Detector</td><td>" . ($detector_status ? '<span class="success">✅ Running</span>' : '<span class="error">❌ Stopped</span>') . "</td><td>" . ($detector_port ? "Port $detector_port" : "Not detected") . "</td></tr>";
        echo "<tr><td>Email Generator</td><td>" . ($email_status ? '<span class="success">✅ Running</span>' : '<span class="error">❌ Stopped</span>') . "</td><td>" . ($email_port ? "Port $email_port" : "Not detected") . "</td></tr>";
        echo "</table>";
        
        if (!$detector_status || !$email_status) {
            ?>
            <div class="notice notice-error">
                <h3>⚠️ Some AI Agents Are Not Running</h3>
                <p>To start the agents, run these commands in your terminal from the project root:</p>
                <pre style="background: #f1f1f1; padding: 10px; border-radius: 5px; margin: 10px 0;">python -m uvicorn agents.abandonment_detector.app:app --host 0.0.0.0 --port 8006
python -m uvicorn agents.email_generator_offer_suggestor.app:app --host 0.0.0.0 --port 8002</pre>
            </div>
            <?php
        } else {
            ?>
            <div class="notice notice-success">
                <h3>🎉 All Systems Running!</h3>
                <p>Your Shopping Cart Recovery AI system is fully operational and ready to recover abandoned carts!</p>
            </div>
            <?php
        }
        ?>
        
        <h2>🎯 How The System Works</h2>
        <ol>
            <li><strong>Product Setup:</strong> Create products in WooCommerce (Electronics/Smartphones for tech personas, Shoes/Sports for fitness personas)</li>
            <li><strong>Cart Tracking:</strong> When customers add items to cart, the system starts monitoring</li>
            <li><strong>Abandonment Detection:</strong> AI analyzes user behavior patterns to detect abandonment</li>
            <li><strong>Personalized Recovery:</strong> AI generates custom emails with:
                <ul>
                    <li>Dynamic discounts (5%-20% based on cart value)</li>
                    <li>Smart product recommendations</li>
                    <li>Personalized messaging based on customer persona</li>
                </ul>
            </li>
            <li><strong>Email Delivery:</strong> Recovery emails are sent via WordPress/WooCommerce</li>
            <li><strong>Conversion Tracking:</strong> System tracks email opens, clicks, and purchases</li>
        </ol>
        
        <hr>
        <p><strong>Access Points:</strong></p>
        <ul>
            <li><a href="<?php echo admin_url('admin.php?page=scr-analytics'); ?>" target="_blank">WordPress Admin Dashboard →</a></li>
            <li><a href="<?php echo admin_url('post-new.php?post_type=product'); ?>" target="_blank">Create WooCommerce Products →</a></li>
        </ul>
        
    </body>
    </html>
    <?php
    exit;
}
?>