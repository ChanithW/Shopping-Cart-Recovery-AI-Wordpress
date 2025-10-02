<?php
/**
 * Enhanced database helper functions for the Shopping Cart Recovery AI system.
 * Handles product data retrieval and cart item enrichment.
 */

// Verify WooCommerce is active and products exist
function scr_verify_woocommerce_setup() {
    if (!class_exists('WooCommerce')) {
        error_log('SCR: WooCommerce is not active!');
        return false;
    }
    
    // Check if there are any products
    $products_count = wp_count_posts('product');
    $published_count = $products_count->publish ?? 0;
    
    error_log("SCR: Found $published_count published WooCommerce products");
    
    if ($published_count == 0) {
        error_log('SCR: No WooCommerce products found. Please create some products first.');
        return false;
    }
    
    return true;
}

// Get product information using WooCommerce native functions
function scr_get_product_info($wc_product_id) {
    $wc_product = wc_get_product($wc_product_id);
    
    if (!$wc_product || !$wc_product->exists()) {
        error_log("SCR: Product not found: $wc_product_id");
        return null;
    }
    
    // Get product categories and map to our AI system categories
    $categories = $wc_product->get_category_ids();
    $category = 'general'; // default category
    
    if (!empty($categories)) {
        foreach ($categories as $cat_id) {
            $cat_term = get_term($cat_id);
            if ($cat_term && !is_wp_error($cat_term)) {
                $cat_name = strtolower($cat_term->name);
                
                // Map WooCommerce categories to AI system categories
                if (strpos($cat_name, 'phone') !== false || 
                    strpos($cat_name, 'mobile') !== false || 
                    strpos($cat_name, 'electronics') !== false ||
                    strpos($cat_name, 'tech') !== false ||
                    strpos($cat_name, 'gadget') !== false ||
                    strpos($cat_name, 'accessory') !== false ||
                    strpos($cat_name, 'headphone') !== false ||
                    strpos($cat_name, 'charger') !== false) {
                    $category = 'smartphone';
                    break;
                } elseif (strpos($cat_name, 'shoe') !== false || 
                         strpos($cat_name, 'footwear') !== false || 
                         strpos($cat_name, 'sneaker') !== false ||
                         strpos($cat_name, 'boot') !== false ||
                         strpos($cat_name, 'sport') !== false ||
                         strpos($cat_name, 'running') !== false ||
                         strpos($cat_name, 'athletic') !== false ||
                         strpos($cat_name, 'fitness') !== false) {
                    $category = 'shoes';
                    break;
                }
            }
        }
    }
    
    // Get comprehensive description
    $description = $wc_product->get_description();
    if (empty($description)) {
        $description = $wc_product->get_short_description();
    }
    if (empty($description)) {
        $description = 'High-quality product available in our store.';
    }
    
    // Clean HTML from description
    $description = wp_strip_all_tags($description);
    $description = wp_trim_words($description, 30, '...');
    
    return array(
        'product_id' => $wc_product_id,
        'name' => $wc_product->get_name(),
        'description' => $description,
        'price' => floatval($wc_product->get_price()),
        'regular_price' => floatval($wc_product->get_regular_price()),
        'sale_price' => $wc_product->is_on_sale() ? floatval($wc_product->get_sale_price()) : null,
        'category' => $category,
        'categories' => wp_get_post_terms($wc_product_id, 'product_cat', array('fields' => 'names')),
        'stock_quantity' => $wc_product->get_stock_quantity() ?: 0,
        'stock_status' => $wc_product->get_stock_status(),
        'in_stock' => $wc_product->is_in_stock(),
        'image_url' => wp_get_attachment_url($wc_product->get_image_id()),
        'permalink' => $wc_product->get_permalink(),
        'sku' => $wc_product->get_sku(),
        'weight' => $wc_product->get_weight(),
        'dimensions' => array(
            'length' => $wc_product->get_length(),
            'width' => $wc_product->get_width(),
            'height' => $wc_product->get_height()
        )
    );
}

// Enrich cart data with product information
function scr_enrich_cart_data($cart) {
    $enriched_items = array();
    
    foreach ($cart as $cart_item_key => $cart_item) {
        $product_id = $cart_item['product_id'];
        $product_info = scr_get_product_info($product_id);
        
        if ($product_info) {
            $enriched_items[] = array(
                'product_id' => (int) $product_id,
                'name' => $product_info['name'],
                'description' => $product_info['description'],
                'price' => $product_info['price'],
                'quantity' => (int) $cart_item['quantity'],
                'category' => $product_info['category'],
                'stock_quantity' => $product_info['stock_quantity']
            );
        } else {
            // Fallback with minimal data
            $product = $cart_item['data'];
            $enriched_items[] = array(
                'product_id' => (int) $product_id,
                'name' => method_exists($product, 'get_name') ? $product->get_name() : 'Unknown Product',
                'description' => 'Product description not available',
                'price' => method_exists($product, 'get_price') ? (float) $product->get_price() : 0.0,
                'quantity' => (int) $cart_item['quantity'],
                'category' => 'general',
                'stock_quantity' => 0
            );
        }
    }
    
    return $enriched_items;
}

// Populate sample products (run once)
function scr_populate_sample_products() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'products';
    
    // Check if products already exist
    $count = $wpdb->get_var("SELECT COUNT(*) FROM $table_name");
    if ($count > 0) {
        error_log('SCR: Products table already populated');
        return;
    }
    
    // Include the SQL file and execute it
    $sql_file = plugin_dir_path(__FILE__) . '../../database/schema.sql';
    if (file_exists($sql_file)) {
        $sql_content = file_get_contents($sql_file);
        
        // Split by semicolons and execute each statement
        $statements = array_filter(array_map('trim', explode(';', $sql_content)));
        
        foreach ($statements as $statement) {
            if (!empty($statement) && strpos($statement, 'INSERT INTO products') === 0) {
                // Replace 'products' with the WordPress table name
                $statement = str_replace('INSERT INTO products', "INSERT INTO $table_name", $statement);
                $wpdb->query($statement);
            }
        }
        
        error_log('SCR: Sample products populated successfully');
    } else {
        error_log('SCR: Schema file not found: ' . $sql_file);
    }
}

// Get popular products from WooCommerce (by sales or views)
function scr_get_popular_products($limit = 5) {
    // Get best-selling products
    $args = array(
        'post_type' => 'product',
        'post_status' => 'publish',
        'posts_per_page' => $limit,
        'meta_query' => array(
            array(
                'key' => '_visibility',
                'value' => array('catalog', 'visible'),
                'compare' => 'IN'
            )
        ),
        'meta_key' => 'total_sales',
        'orderby' => 'meta_value_num',
        'order' => 'DESC'
    );
    
    $products = get_posts($args);
    $popular_items = array();
    
    foreach ($products as $product_post) {
        $product_info = scr_get_product_info($product_post->ID);
        if ($product_info && $product_info['in_stock']) {
            $popular_items[] = array(
                'id' => $product_post->ID,
                'item_name' => $product_info['name'],
                'description' => $product_info['description'],
                'price' => $product_info['price'],
                'category' => $product_info['category'],
                'stock_quantity' => $product_info['stock_quantity'],
                'image_url' => $product_info['image_url'],
                'permalink' => $product_info['permalink']
            );
        }
    }
    
    // If no best sellers found, get recent products
    if (empty($popular_items)) {
        $args = array(
            'post_type' => 'product',
            'post_status' => 'publish',
            'posts_per_page' => $limit,
            'orderby' => 'date',
            'order' => 'DESC'
        );
        
        $products = get_posts($args);
        foreach ($products as $product_post) {
            $product_info = scr_get_product_info($product_post->ID);
            if ($product_info && $product_info['in_stock']) {
                $popular_items[] = array(
                    'id' => $product_post->ID,
                    'item_name' => $product_info['name'],
                    'description' => $product_info['description'],
                    'price' => $product_info['price'],
                    'category' => $product_info['category'],
                    'stock_quantity' => $product_info['stock_quantity']
                );
            }
        }
    }
    
    return $popular_items;
}

// Get similar products based on category and price range
function scr_get_similar_products($product_id, $limit = 5) {
    $product_info = scr_get_product_info($product_id);
    if (!$product_info) {
        return array();
    }
    
    $category = $product_info['category'];
    $price = $product_info['price'];
    $price_min = $price * 0.7; // 30% lower
    $price_max = $price * 1.3; // 30% higher
    
    // Find products in same category with similar price range
    $args = array(
        'post_type' => 'product',
        'post_status' => 'publish',
        'posts_per_page' => $limit + 1, // +1 to account for excluding current product
        'post__not_in' => array($product_id), // Exclude current product
        'meta_query' => array(
            'relation' => 'AND',
            array(
                'key' => '_price',
                'value' => array($price_min, $price_max),
                'type' => 'DECIMAL',
                'compare' => 'BETWEEN'
            ),
            array(
                'key' => '_stock_status',
                'value' => 'instock'
            )
        )
    );
    
    // Add category filter if we have WooCommerce categories
    $wc_categories = wp_get_post_terms($product_id, 'product_cat', array('fields' => 'ids'));
    if (!empty($wc_categories)) {
        $args['tax_query'] = array(
            array(
                'taxonomy' => 'product_cat',
                'field'    => 'term_id',
                'terms'    => $wc_categories[0], // Use first category
            )
        );
    }
    
    $products = get_posts($args);
    $similar_items = array();
    
    foreach ($products as $product_post) {
        if (count($similar_items) >= $limit) break;
        
        $similar_info = scr_get_product_info($product_post->ID);
        if ($similar_info && $similar_info['in_stock']) {
            $similar_items[] = array(
                'id' => $product_post->ID,
                'item_name' => $similar_info['name'],
                'description' => $similar_info['description'],
                'price' => $similar_info['price'],
                'category' => $similar_info['category'],
                'stock_quantity' => $similar_info['stock_quantity'],
                'similarity_score' => 0.8, // High similarity for same category
                'reason' => 'Similar product in ' . $category . ' category'
            );
        }
    }
    
    return $similar_items;
}

// Initialize the WooCommerce integration
function scr_init_woocommerce_integration() {
    if (!scr_verify_woocommerce_setup()) {
        add_action('admin_notices', function() {
            echo '<div class="notice notice-error"><p><strong>Shopping Cart Recovery AI:</strong> Please activate WooCommerce and create some products first.</p></div>';
        });
        return false;
    }
    
    error_log('SCR: WooCommerce integration initialized successfully');
    return true;
}
?>