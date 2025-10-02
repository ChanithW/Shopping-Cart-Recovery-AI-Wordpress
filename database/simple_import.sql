-- Simple import script for Shopping Cart Recovery AI
-- Use this in phpMyAdmin or MySQL command line

-- Drop table if exists (optional)
DROP TABLE IF EXISTS `wp_products`;

-- Create the products table
CREATE TABLE `wp_products` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `item_name` varchar(255) NOT NULL,
    `description` text NOT NULL,
    `price` decimal(10,2) NOT NULL,
    `category` varchar(100) NOT NULL,
    `stock_status` enum('in_stock','out_of_stock') DEFAULT 'in_stock',
    `stock_quantity` int(11) DEFAULT 0,
    `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
    `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_category` (`category`),
    KEY `idx_stock_status` (`stock_status`),
    KEY `idx_price` (`price`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data (just a few items to test)
INSERT INTO `wp_products` (`item_name`, `description`, `price`, `category`, `stock_status`, `stock_quantity`) VALUES
('iPhone 15 Pro Max 256GB', 'Experience the ultimate iPhone with titanium design, advanced camera system, and A17 Pro chip for unmatched performance.', 1299.99, 'smartphone', 'in_stock', 45),
('Samsung Galaxy S24 Ultra 512GB', 'Premium Android flagship with S Pen, 200MP camera, AI-enhanced photography, and stunning 6.8-inch Dynamic AMOLED display.', 1399.99, 'smartphone', 'in_stock', 29),
('Apple AirPods Pro 2nd Gen', 'Premium wireless earbuds with active noise cancellation, spatial audio, and personalized listening experience.', 249.99, 'smartphone', 'in_stock', 128),
('Anker PowerCore 26800mAh', 'Ultra-high capacity power bank with fast charging technology, multiple USB ports, and premium safety features.', 79.99, 'smartphone', 'in_stock', 156),
('Apple Lightning to USB-C Cable 2m', 'Official Apple cable with premium braided design, fast data transfer, and MFi certification for reliability.', 39.99, 'smartphone', 'in_stock', 345),

('Nike Air Zoom Pegasus 40', 'Iconic running shoe with responsive Zoom Air units, breathable mesh upper, and reliable traction for daily miles.', 129.99, 'shoes', 'in_stock', 87),
('Adidas Ultraboost 23', 'Energy-returning running shoe with BOOST midsole, Primeknit upper, and Continental rubber outsole for superior grip.', 189.99, 'shoes', 'in_stock', 64),
('Nike Air Force 1 07', 'Classic basketball-inspired sneaker with leather upper, Air-Sole cushioning, and timeless court-ready style.', 109.99, 'shoes', 'in_stock', 156),
('Converse Chuck Taylor All Star', 'Timeless canvas sneaker with rubber toe cap, classic silhouette, and authentic street-style heritage design.', 59.99, 'shoes', 'in_stock', 267),
('Balega Hidden Comfort No-Show', 'Premium running socks with seamless toe closure, moisture-wicking fabric, and blister prevention technology.', 14.99, 'shoes', 'in_stock', 456);

-- Verify the data was inserted
SELECT COUNT(*) as total_products FROM wp_products;
SELECT category, COUNT(*) as count_per_category FROM wp_products GROUP BY category;