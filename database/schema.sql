-- Products table for the Shopping Cart Recovery AI system
CREATE TABLE wp_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    stock_status ENUM('in_stock', 'out_of_stock') DEFAULT 'in_stock',
    stock_quantity INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_stock_status (stock_status),
    INDEX idx_price (price)
);

-- Insert smartphone-related products (75 items)
INSERT INTO wp_products (item_name, description, price, category, stock_status, stock_quantity) VALUES
-- Apple phones
('iPhone 15 Pro Max 256GB', 'Experience the ultimate iPhone with titanium design, advanced camera system, and A17 Pro chip for unmatched performance.', 1299.99, 'smartphone', 'in_stock', 45),
('iPhone 15 Pro 128GB', 'Professional-grade iPhone featuring titanium build, ProRAW photography, and lightning-fast A17 Pro processor.', 999.99, 'smartphone', 'in_stock', 38),
('iPhone 15 Plus 256GB', 'Large-screen iPhone with exceptional battery life, advanced dual-camera system, and vibrant Super Retina XDR display.', 899.99, 'smartphone', 'in_stock', 52),
('iPhone 15 128GB', 'The newest iPhone with Dynamic Island, 48MP main camera, and all-day battery life in a sleek aluminum design.', 799.99, 'smartphone', 'in_stock', 67),
('iPhone 14 Pro 256GB', 'Previous-generation Pro iPhone with A16 Bionic chip, ProRAW capabilities, and premium stainless steel construction.', 899.99, 'smartphone', 'in_stock', 23),
('iPhone 14 128GB', 'Reliable iPhone with advanced dual-camera system, Crash Detection, and beautiful Ceramic Shield front.', 699.99, 'smartphone', 'in_stock', 41),
('iPhone SE 3rd Gen 128GB', 'Compact powerhouse iPhone with A15 Bionic chip, Touch ID, and classic home button design for maximum efficiency.', 429.99, 'smartphone', 'in_stock', 89),

-- Samsung phones
('Samsung Galaxy S24 Ultra 512GB', 'Premium Android flagship with S Pen, 200MP camera, AI-enhanced photography, and stunning 6.8-inch Dynamic AMOLED display.', 1399.99, 'smartphone', 'in_stock', 29),
('Samsung Galaxy S24+ 256GB', 'High-performance Galaxy phone with advanced AI features, exceptional night photography, and fast wireless charging.', 999.99, 'smartphone', 'in_stock', 34),
('Samsung Galaxy S24 128GB', 'Flagship Galaxy experience with AI-powered camera, vibrant AMOLED display, and all-day intelligent battery.', 849.99, 'smartphone', 'in_stock', 56),
('Samsung Galaxy S23 FE 256GB', 'Fan Edition Galaxy with flagship features, versatile triple camera system, and premium build quality at great value.', 699.99, 'smartphone', 'in_stock', 47),
('Samsung Galaxy A54 5G 128GB', 'Mid-range Galaxy with impressive triple camera, smooth 120Hz display, and reliable 5G connectivity for everyday use.', 449.99, 'smartphone', 'in_stock', 73),
('Samsung Galaxy A34 5G 128GB', 'Affordable 5G smartphone with long-lasting battery, vibrant Super AMOLED display, and versatile camera system.', 349.99, 'smartphone', 'in_stock', 82),
('Samsung Galaxy Z Fold5 512GB', 'Revolutionary foldable phone that transforms into a tablet with multitasking capabilities and S Pen support.', 1899.99, 'smartphone', 'in_stock', 15),
('Samsung Galaxy Z Flip5 256GB', 'Compact foldable smartphone with iconic flip design, external cover screen, and premium camera features.', 999.99, 'smartphone', 'in_stock', 21),

-- Power banks
('Anker PowerCore 26800mAh', 'Ultra-high capacity power bank with fast charging technology, multiple USB ports, and premium safety features.', 79.99, 'smartphone', 'in_stock', 156),
('RAVPower 20000mAh PD Charger', 'Portable power bank with Power Delivery, USB-C fast charging, and LED display showing precise battery percentage.', 49.99, 'smartphone', 'in_stock', 203),
('Belkin Boost Charge 10000mAh', 'Compact wireless power bank with Qi charging pad, USB-C input/output, and sleek premium design.', 59.99, 'smartphone', 'in_stock', 127),
('Xiaomi Mi Power Bank 3 20000mAh', 'High-capacity portable charger with dual USB output, fast charging support, and durable aluminum construction.', 35.99, 'smartphone', 'in_stock', 189),
('AUKEY 30000mAh Solar Power Bank', 'Outdoor adventure power bank with solar charging, rugged design, LED flashlight, and multiple device support.', 89.99, 'smartphone', 'in_stock', 94),

-- Chargers
('Apple 20W USB-C Power Adapter', 'Official Apple fast charger with USB-C output, optimized for iPhone and iPad charging efficiency.', 29.99, 'smartphone', 'in_stock', 287),
('Samsung 25W Super Fast Charger', 'Original Samsung charger with adaptive fast charging technology and USB-C cable included for Galaxy devices.', 24.99, 'smartphone', 'in_stock', 234),
('Anker PowerPort III 65W Charger', 'Multi-port wall charger with GaN technology, foldable design, and simultaneous fast charging for multiple devices.', 54.99, 'smartphone', 'in_stock', 167),
('Belkin 3-in-1 Wireless Charger', 'Premium wireless charging station for iPhone, Apple Watch, and AirPods with elegant design and fast charging.', 149.99, 'smartphone', 'in_stock', 76),
('RAVPower 61W PD Wall Charger', 'Compact USB-C wall charger with Power Delivery, foldable plug design, and universal device compatibility.', 39.99, 'smartphone', 'in_stock', 198),

-- Cables
('Apple Lightning to USB-C Cable 2m', 'Official Apple cable with premium braided design, fast data transfer, and MFi certification for reliability.', 39.99, 'smartphone', 'in_stock', 345),
('Samsung USB-C to USB-C Cable 1.5m', 'Durable Samsung cable with fast charging support, data sync capability, and tangle-resistant design.', 19.99, 'smartphone', 'in_stock', 456),
('Anker Powerline III USB-C Cable', 'Ultra-durable charging cable with 25000+ bend lifespan, fast charging support, and premium nylon braiding.', 24.99, 'smartphone', 'in_stock', 278),
('Belkin DuraTek Lightning Cable 3m', 'Extra-long Lightning cable with DuraTek fiber reinforcement, MFi certification, and tangle-free design.', 34.99, 'smartphone', 'in_stock', 189),
('AUKEY USB-C to Lightning Cable', 'MFi-certified cable with braided nylon construction, fast charging capability, and excellent durability rating.', 22.99, 'smartphone', 'in_stock', 312),

-- Headphones
('Apple AirPods Pro 2nd Gen', 'Premium wireless earbuds with active noise cancellation, spatial audio, and personalized listening experience.', 249.99, 'smartphone', 'in_stock', 128),
('Samsung Galaxy Buds2 Pro', 'Professional wireless earbuds with intelligent ANC, 360 Audio, and seamless Galaxy device integration.', 199.99, 'smartphone', 'in_stock', 94),
('Sony WH-1000XM5 Headphones', 'Industry-leading noise canceling over-ear headphones with exceptional sound quality and 30-hour battery life.', 399.99, 'smartphone', 'in_stock', 67),
('Bose QuietComfort 45', 'Premium noise-canceling headphones with balanced sound, comfortable design, and impressive 24-hour battery.', 329.99, 'smartphone', 'in_stock', 52),
('Sennheiser Momentum 4 Wireless', 'Audiophile-grade wireless headphones with adaptive noise cancellation and exceptional 60-hour battery life.', 349.99, 'smartphone', 'in_stock', 41),
('JBL Tune 770NC Headphones', 'Affordable noise-canceling headphones with powerful JBL sound, quick charge, and hands-free calling features.', 149.99, 'smartphone', 'in_stock', 156),

-- Handsfree/Earphones
('Apple EarPods with Lightning', 'Classic Apple wired earphones with Lightning connector, built-in remote, and comfortable ergonomic design.', 29.99, 'smartphone', 'in_stock', 289),
('Samsung AKG Type-C Earphones', 'Premium wired earphones tuned by AKG with USB-C connector and superior audio quality for Galaxy devices.', 34.99, 'smartphone', 'in_stock', 234),
('Panasonic ErgoFit Earbuds', 'Comfortable in-ear headphones with ergonomic design, rich bass sound, and tangle-resistant cord.', 19.99, 'smartphone', 'in_stock', 378),
('Skullcandy Ink\'d+ Earbuds', 'Stylish wired earbuds with noise-isolating fit, powerful drivers, and built-in microphone for calls.', 24.99, 'smartphone', 'in_stock', 267),
('Audio-Technica ATH-CKS5TW', 'True wireless earbuds with solid bass response, secure fit, and IPX4 water resistance for active use.', 99.99, 'smartphone', 'in_stock', 89),

-- Phone cases
('Apple iPhone 15 Pro Silicone Case', 'Official Apple silicone case with perfect fit, soft-touch finish, and built-in MagSafe compatibility.', 49.99, 'smartphone', 'in_stock', 167),
('Samsung Galaxy S24 Protective Case', 'Official Samsung case with military-grade protection, raised edges, and precise cutouts for all features.', 39.99, 'smartphone', 'in_stock', 198),
('OtterBox Defender Pro iPhone Case', 'Ultimate protection case with multi-layer defense, holster clip, and dust/drop protection certification.', 79.99, 'smartphone', 'in_stock', 123),
('Spigen Ultra Hybrid Clear Case', 'Crystal clear hybrid case with air cushion technology, wireless charging compatibility, and scratch resistance.', 29.99, 'smartphone', 'in_stock', 245),
('Peak Design Mobile Case', 'Photographer-friendly case with SlimLink mounting system, premium materials, and everyday carry optimization.', 59.99, 'smartphone', 'in_stock', 87),
('Bellroy Leather Case Wallet', 'Premium leather case with card storage, elegant design, and environmental leather sourcing commitment.', 89.99, 'smartphone', 'in_stock', 76),

-- Screen protectors and accessories
('Zagg InvisibleShield Glass Elite+', 'Premium tempered glass screen protector with antimicrobial treatment and advanced impact protection technology.', 44.99, 'smartphone', 'in_stock', 234),
('Belkin UltraGlass Screen Protector', 'Double-ion exchange strengthened glass with easy installation tray and case-friendly design for perfect fit.', 39.99, 'smartphone', 'in_stock', 189),
('PopSocket Collapsible Grip', 'Expandable phone grip and stand with strong 3M adhesive, stylish designs, and hands-free viewing capability.', 14.99, 'smartphone', 'in_stock', 456),
('Anker Magnetic Phone Mount', 'Strong magnetic car mount with 360-degree rotation, one-handed operation, and secure hold for navigation.', 24.99, 'smartphone', 'in_stock', 167),
('Apple MagSafe Car Vent Mount', 'Official Apple car mount with MagSafe compatibility, secure magnetic hold, and adjustable viewing angles.', 49.99, 'smartphone', 'in_stock', 98);

-- Insert shoes-related products (75 items)
INSERT INTO wp_products (item_name, description, price, category, stock_status, stock_quantity) VALUES
-- Running shoes
('Nike Air Zoom Pegasus 40', 'Iconic running shoe with responsive Zoom Air units, breathable mesh upper, and reliable traction for daily miles.', 129.99, 'shoes', 'in_stock', 87),
('Adidas Ultraboost 23', 'Energy-returning running shoe with BOOST midsole, Primeknit upper, and Continental rubber outsole for superior grip.', 189.99, 'shoes', 'in_stock', 64),
('Brooks Glycerin 21', 'Luxurious neutral running shoe with DNA LOFT v3 cushioning, seamless transitions, and plush comfort experience.', 159.99, 'shoes', 'in_stock', 52),
('ASICS Gel-Nimbus 25', 'Premium cushioned running shoe with FF BLAST+ foam, PureGEL technology, and enhanced comfort for long distances.', 179.99, 'shoes', 'in_stock', 43),
('New Balance Fresh Foam X 1080v12', 'Maximum cushioned running shoe with Fresh Foam X midsole, Hypoknit upper, and smooth heel-to-toe transition.', 149.99, 'shoes', 'in_stock', 76),
('Hoka Clifton 9', 'Lightweight daily trainer with maximum cushioning, early stage Meta-Rocker, and incredibly soft landing experience.', 139.99, 'shoes', 'in_stock', 89),
('Saucony Triumph 21', 'Ultra-cushioned running shoe with PWRRUN+ foam, FORMFIT technology, and luxurious comfort for easy runs.', 169.99, 'shoes', 'in_stock', 38),
('Mizuno Wave Rider 27', 'Smooth-riding shoe with Mizuno Wave plate, ENERZY foam, and premium comfort for recreational runners.', 134.99, 'shoes', 'in_stock', 67),
('Under Armour HOVR Phantom 3', 'Connected running shoe with HOVR foam, UA MapMyRun integration, and real-time coaching feedback capability.', 139.99, 'shoes', 'in_stock', 45),
('Puma Velocity Nitro 3', 'Responsive running shoe with NITRO foam, PUMAGRIP outsole, and lightweight design for speed training sessions.', 99.99, 'shoes', 'in_stock', 134),

-- Sports shoes  
('Nike Air Force 1 \'07', 'Classic basketball-inspired sneaker with leather upper, Air-Sole cushioning, and timeless court-ready style.', 109.99, 'shoes', 'in_stock', 156),
('Adidas Stan Smith Original', 'Iconic tennis shoe with clean leather design, perforated 3-Stripes, and minimalist court-inspired aesthetic.', 89.99, 'shoes', 'in_stock', 198),
('Converse Chuck Taylor All Star', 'Timeless canvas sneaker with rubber toe cap, classic silhouette, and authentic street-style heritage design.', 59.99, 'shoes', 'in_stock', 267),
('Vans Old Skool Classic', 'Skateboarding legend with durable canvas and suede construction, signature side stripe, and waffle outsole grip.', 69.99, 'shoes', 'in_stock', 189),
('Reebok Classic Leather', 'Retro athletic shoe with soft garment leather upper, comfortable foam midsole, and vintage sports styling.', 74.99, 'shoes', 'in_stock', 143),
('Puma Suede Classic XXI', 'Heritage basketball shoe with premium suede upper, rubber cupsole, and iconic PUMA Formstrip branding.', 79.99, 'shoes', 'in_stock', 167),
('Jordan Air Jordan 1 Low', 'Basketball-inspired sneaker with premium materials, Air-Sole cushioning, and legendary Jordan brand heritage.', 89.99, 'shoes', 'in_stock', 98),
('Fila Disruptor II', 'Chunky retro sneaker with leather upper, thick platform sole, and bold 90s-inspired fashion statement design.', 64.99, 'shoes', 'in_stock', 234),

-- Gym shoes
('Nike Metcon 9', 'Cross-training shoe with dual-density foam, rope-climb tread, and stability for high-intensity workout sessions.', 139.99, 'shoes', 'in_stock', 76),
('Adidas Adipower Weightlifting 4', 'Professional weightlifting shoe with raised heel, BOA closure system, and maximum stability for heavy lifting.', 199.99, 'shoes', 'in_stock', 34),
('Reebok Nano X3', 'Versatile training shoe with Flexweave upper, responsive cushioning, and grip for diverse gym activities.', 129.99, 'shoes', 'in_stock', 89),
('Under Armour TriBase Reign 5', 'Training shoe with TriBase technology, rock-solid heel, and flexibility for explosive gym movements.', 119.99, 'shoes', 'in_stock', 67),
('NOBULL Trainer', 'Minimalist training shoe with SuperFabric upper, durable construction, and versatile performance for CrossFit.', 149.99, 'shoes', 'in_stock', 52),
('Inov-8 F-Lite 235 V3', 'Functional fitness shoe with natural fit, sticky grip outsole, and lightweight design for varied training.', 109.99, 'shoes', 'in_stock', 94),
('New Balance Minimus Prevail', 'Barefoot-inspired training shoe with Vibram outsole, zero drop design, and natural ground connection feel.', 99.99, 'shoes', 'in_stock', 123),

-- Casual athletic shoes
('Allbirds Tree Runners', 'Sustainable running shoe made from eucalyptus fiber with merino wool lining and carbon-neutral shipping.', 98.99, 'shoes', 'in_stock', 107),
('Rothy\'s The Sneaker', 'Eco-friendly shoe made from recycled plastic bottles with machine-washable design and comfortable fit.', 149.99, 'shoes', 'in_stock', 78),
('Adidas Ultraboost 22 Slip-On', 'Laceless lifestyle shoe with BOOST cushioning, Primeknit upper, and easy slip-on convenience for daily wear.', 179.99, 'shoes', 'in_stock', 56),
('Nike React Infinity Run Flyknit 3', 'Injury-reduction focused shoe with React foam, Flyknit upper, and rocker geometry for natural running motion.', 159.99, 'shoes', 'in_stock', 43),
('Hoka Bondi 8', 'Maximum cushioned lifestyle shoe with EVA midsole, breathable mesh, and all-day comfort for walking.', 164.99, 'shoes', 'in_stock', 67),

-- Specialized athletic shoes
('Salomon Speedcross 5', 'Trail running shoe with aggressive grip, precise fit, and protective upper for technical terrain adventures.', 134.99, 'shoes', 'in_stock', 45),
('Merrell Trail Glove 7', 'Minimalist trail shoe with Vibram outsole, barefoot feel, and natural movement for trail connection.', 119.99, 'shoes', 'in_stock', 89),
('La Sportiva Bushido II', 'Technical trail running shoe with FriXion grip, precise fit, and protection for mountain running adventures.', 159.99, 'shoes', 'in_stock', 34),
('Altra Lone Peak 7', 'Zero-drop trail shoe with FootShape toe box, balanced cushioning, and natural running form promotion.', 139.99, 'shoes', 'in_stock', 62),
('Topo Athletic Ultraventure 3', 'Trail running shoe with generous toe box, versatile traction, and comfortable fit for long adventures.', 149.99, 'shoes', 'in_stock', 47),

-- Socks (athletic)
('Balega Hidden Comfort No-Show', 'Premium running socks with seamless toe closure, moisture-wicking fabric, and blister prevention technology.', 14.99, 'shoes', 'in_stock', 456),
('Smartwool PhD Run Light Elite', 'Merino wool running socks with targeted cushioning, odor resistance, and temperature regulation properties.', 21.99, 'shoes', 'in_stock', 378),
('Darn Tough Vermont Running Socks', 'Lifetime guaranteed running socks with merino wool blend, cushioned sole, and unconditional durability promise.', 24.99, 'shoes', 'in_stock', 289),
('Stance Icon No Show Athletic', 'Performance athletic socks with moisture-wicking technology, targeted cushioning, and seamless toe construction.', 16.99, 'shoes', 'in_stock', 345),
('Thorlos Experia Multi-Sport', 'Cushioned athletic socks with THORWICK moisture-wicking, blister protection, and sport-specific padding zones.', 18.99, 'shoes', 'in_stock', 267),
('Bombas Ankle Athletic Socks', 'Comfortable athletic socks with stay-up technology, moisture-wicking fabric, and honeycomb arch support system.', 12.99, 'shoes', 'in_stock', 456),
('CEP Progressive+ Run Socks 2.0', 'Compression running socks with graduated compression, moisture management, and performance enhancement technology.', 39.99, 'shoes', 'in_stock', 167),
('Feetures Elite Light Cushion', 'Targeted compression running socks with anatomical design, seamless toe, and advanced moisture-wicking fibers.', 17.99, 'shoes', 'in_stock', 298),

-- Laces  
('Lock Laces Elastic Shoelaces', 'No-tie elastic laces with locking system, one-size-fits-all design, and easy slip-on shoe conversion.', 9.99, 'shoes', 'in_stock', 567),
('Nathan Run Laces Reflective', 'Reflective elastic laces for night safety, secure lock system, and easy adjustment for running shoes.', 12.99, 'shoes', 'in_stock', 423),
('Yankz Sure Lace System', 'Adjustable elastic laces with secure locking mechanism, customizable fit, and no-tie convenience for athletes.', 14.99, 'shoes', 'in_stock', 356),
('Hickies Elastic Lacing System', 'One-size-fits-all elastic laces with individual adjustment zones and modern no-tie shoe customization.', 19.99, 'shoes', 'in_stock', 234),
('Xtenex True Adaptive Laces', 'Individual elastic laces with knot-free design, custom tension adjustment, and comfortable all-day wear.', 24.99, 'shoes', 'in_stock', 189),

-- Shoe accessories
('Dr. Scholl\'s Sport Insoles', 'Performance insoles with gel cushioning, arch support, and moisture-wicking technology for athletic activities.', 19.99, 'shoes', 'in_stock', 278),
('Superfeet Green Heritage Insoles', 'Professional-grade insoles with biomechanical design, deep heel cup, and structured support for foot health.', 54.99, 'shoes', 'in_stock', 145),
('Powerstep Pinnacle Maxx Insoles', 'Maximum support insoles with dual-layer cushioning, antimicrobial treatment, and motion control technology.', 49.99, 'shoes', 'in_stock', 167),
('Spenco Polysorb Cross Trainer', 'Athletic insoles with 4-way stretch fabric, shock absorption, and moisture management for active lifestyles.', 29.99, 'shoes', 'in_stock', 234),
('Currex RunPro Insoles', 'Dynamic insoles with flexible arch support, rebound foam, and sport-specific design for running performance.', 69.99, 'shoes', 'in_stock', 98),
('Jason Markk Premium Shoe Cleaner', 'Eco-friendly shoe cleaning solution safe for all materials, with premium brush and microfiber cloth included.', 24.99, 'shoes', 'in_stock', 189),
('Crep Protect Ultimate Kit', 'Complete shoe care system with stain-resistant spray, cleaning wipes, and premium brush for protection.', 39.99, 'shoes', 'in_stock', 156),
('Reshoven8r Laundry System', 'Professional shoe cleaning system with sneaker-safe detergent, cleaning brush, and protective wash bags.', 34.99, 'shoes', 'in_stock', 123),

-- Specialty footwear
('Oofos OOahh Recovery Sandal', 'Post-workout recovery sandal with OOfoam technology, arch support, and pressure relief for foot recovery.', 59.99, 'shoes', 'in_stock', 134),
('Adidas Adilette Comfort Slides', 'Comfortable recovery slides with Cloudfoam Plus cushioning, quick-dry design, and post-exercise relaxation.', 34.99, 'shoes', 'in_stock', 198),
('Nike Benassi JDI Slide', 'Classic recovery slide with textured footbed, lightweight design, and easy slip-on convenience for athletes.', 24.99, 'shoes', 'in_stock', 267),
('Crocs Classic Clog', 'Comfortable casual clog with Croslite foam construction, ventilation ports, and easy cleaning for daily wear.', 49.99, 'shoes', 'in_stock', 189),
('Birkenstock Arizona Soft Footbed', 'Iconic two-strap sandal with contoured cork footbed, adjustable straps, and legendary comfort and support.', 134.99, 'shoes', 'in_stock', 87);