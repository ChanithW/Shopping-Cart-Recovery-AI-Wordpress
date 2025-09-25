#!/usr/bin/env python3
"""
Populate WordPress Cart Analytics Database
Creates sample abandoned cart data for testing the analytics dashboard
"""

import mysql.connector
import json
import time
import random
from datetime import datetime, timedelta

def populate_cart_data():
    print("🛒 WORDPRESS CART ANALYTICS - DATABASE POPULATION")
    print("="*60)
    
    # Database connection settings (adjust these for your WordPress setup)
    db_config = {
        'host': 'localhost',
        'database': 'cartdb',  # Your WordPress database name
        'user': 'root',
        'password': '',
        'charset': 'utf8mb4'
    }
    
    try:
        # Connect to database
        print("📡 Connecting to database...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # WordPress table prefix (usually wp_)
        table_prefix = 'wp_'
        table_name = f'{table_prefix}cart_logs'
        
        print(f"📊 Working with table: {table_name}")
        
        # Create table if it doesn't exist
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
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
        )
        """
        
        cursor.execute(create_table_sql)
        print("✅ Table created/verified successfully")
        
        # Sample cart data
        sample_carts = [
            {
                'user_id': 'customer_001',
                'email': 'john.doe@example.com',
                'items': [
                    {'product_id': 1001, 'name': 'Wireless Headphones', 'price': 99.99, 'quantity': 1},
                    {'product_id': 1002, 'name': 'Phone Case', 'price': 24.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 1, 'clicked': 0, 'converted': 0
            },
            {
                'user_id': 'customer_002',
                'email': 'jane.smith@example.com',
                'items': [
                    {'product_id': 2001, 'name': 'Gaming Mouse', 'price': 79.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 1, 'clicked': 1, 'converted': 1
            },
            {
                'user_id': 'customer_003',
                'email': 'mike.wilson@example.com',
                'items': [
                    {'product_id': 3001, 'name': 'MacBook Pro', 'price': 1299.99, 'quantity': 1},
                    {'product_id': 3002, 'name': 'Laptop Bag', 'price': 49.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 0, 'clicked': 0, 'converted': 0
            },
            {
                'user_id': 'guest_004',
                'email': 'guest.customer@example.com',
                'items': [
                    {'product_id': 4001, 'name': 'Bluetooth Speaker', 'price': 59.99, 'quantity': 2}
                ],
                'abandoned': 1, 'email_sent': 0, 'opened': 0, 'clicked': 0, 'converted': 0
            },
            {
                'user_id': 'customer_005',
                'email': 'sarah.johnson@example.com',
                'items': [
                    {'product_id': 5001, 'name': 'Smartwatch', 'price': 299.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 1, 'clicked': 1, 'converted': 0
            },
            {
                'user_id': 'customer_006',
                'email': 'alex.brown@example.com',
                'items': [
                    {'product_id': 6001, 'name': 'Wireless Charger', 'price': 39.99, 'quantity': 1},
                    {'product_id': 6002, 'name': 'Cable', 'price': 19.99, 'quantity': 2}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 1, 'clicked': 0, 'converted': 0
            },
            {
                'user_id': 'customer_007',
                'email': 'lisa.davis@example.com',
                'items': [
                    {'product_id': 7001, 'name': 'Gaming Keyboard', 'price': 129.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 1, 'opened': 1, 'clicked': 1, 'converted': 1
            },
            {
                'user_id': 'guest_008',
                'email': 'anonymous.shopper@example.com',
                'items': [
                    {'product_id': 8001, 'name': 'Fitness Tracker', 'price': 199.99, 'quantity': 1}
                ],
                'abandoned': 1, 'email_sent': 0, 'opened': 0, 'clicked': 0, 'converted': 0
            }
        ]
        
        # Insert sample data
        insert_sql = f"""
        INSERT INTO {table_name} 
        (user_id, email, items, timestamp, abandoned, email_sent, opened, clicked, converted) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        inserted_count = 0
        print("\n📝 Inserting sample cart data...")
        
        for i, cart in enumerate(sample_carts, 1):
            # Generate realistic timestamps from last 7 days
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            items_json = json.dumps(cart['items'])
            
            cursor.execute(insert_sql, (
                cart['user_id'],
                cart['email'],
                items_json,
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                cart['abandoned'],
                cart['email_sent'],
                cart['opened'],
                cart['clicked'],
                cart['converted']
            ))
            
            inserted_count += 1
            cart_value = sum(item['price'] * item['quantity'] for item in cart['items'])
            print(f"   {i}. {cart['email']} - ${cart_value:.2f} ({'Converted' if cart['converted'] else 'Abandoned'})")
        
        conn.commit()
        print(f"\n✅ Successfully inserted {inserted_count} cart records")
        
        # Show analytics stats
        print("\n📊 CURRENT ANALYTICS DASHBOARD STATS")
        print("-" * 40)
        
        stats_sql = f"""
        SELECT 
            COUNT(*) as total_abandoned,
            SUM(email_sent) as emails_sent,
            SUM(opened) as opened,
            SUM(clicked) as clicked,
            SUM(converted) as converted
        FROM {table_name} 
        WHERE abandoned = 1
        """
        
        cursor.execute(stats_sql)
        stats = cursor.fetchone()
        
        total_abandoned, emails_sent, opened, clicked, converted = stats
        
        print(f"📈 Total Abandoned Carts: {total_abandoned}")
        print(f"📧 Emails Sent: {emails_sent}")
        print(f"👀 Emails Opened: {opened}")
        print(f"🔗 Links Clicked: {clicked}")
        print(f"💰 Conversions: {converted}")
        
        if emails_sent > 0:
            open_rate = round((opened / emails_sent) * 100, 2)
            click_rate = round((clicked / emails_sent) * 100, 2)
            conversion_rate = round((converted / emails_sent) * 100, 2)
            
            print(f"\n📊 Performance Rates:")
            print(f"   Open Rate: {open_rate}%")
            print(f"   Click Rate: {click_rate}%")
            print(f"   Conversion Rate: {conversion_rate}%")
        
        # Show recent carts
        print(f"\n🕐 Recent Abandoned Carts:")
        recent_sql = f"""
        SELECT user_id, email, timestamp, abandoned, email_sent, converted
        FROM {table_name} 
        ORDER BY timestamp DESC 
        LIMIT 5
        """
        
        cursor.execute(recent_sql)
        recent_carts = cursor.fetchall()
        
        for cart in recent_carts:
            user_id, email, timestamp, abandoned, email_sent, converted = cart
            status = "✅ Converted" if converted else ("📧 Email Sent" if email_sent else "❌ No Email")
            print(f"   {timestamp} - {email} - {status}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("🎉 DATABASE POPULATED SUCCESSFULLY!")
        print("\n🌐 Now check your WordPress analytics at:")
        print("http://localhost/wordpress/wp-admin/admin.php?page=scr-analytics")
        print("\nOr if using different URL, navigate to:")
        print("WordPress Admin → Cart Recovery → Analytics")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure MySQL is running")
        print("2. Check database connection settings:")
        print(f"   - Host: {db_config['host']}")
        print(f"   - Database: {db_config['database']}")
        print(f"   - User: {db_config['user']}")
        print("3. Ensure the database exists and is accessible")
        print("4. Make sure WordPress is installed with this database")
        
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = populate_cart_data()
    
    if success:
        print("\n✨ The WordPress analytics page should now show cart data!")
    else:
        print("\n⚠️  Please fix the database connection and try again.")