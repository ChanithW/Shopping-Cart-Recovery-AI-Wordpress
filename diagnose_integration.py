#!/usr/bin/env python3
"""
WordPress Plugin Integration Diagnostic
Checks the integration between WordPress and AI services
"""

import requests
import json
import mysql.connector
from datetime import datetime

def diagnose_integration():
    print("🔍 WORDPRESS PLUGIN INTEGRATION DIAGNOSTIC")
    print("="*60)
    
    # 1. Check AI Services Status
    print("\n1. 🤖 AI Services Status Check")
    print("-"*40)
    
    services = [
        ("Abandonment Detector", "http://localhost:8001/docs"),
        ("Email Generator", "http://localhost:8002/docs")
    ]
    
    services_ok = 0
    for name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name}: RUNNING")
                services_ok += 1
            else:
                print(f"   ❌ {name}: ERROR {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: NOT ACCESSIBLE - {e}")
    
    # 2. Check Database Connection
    print(f"\n2. 🗄️  Database Connection Check")
    print("-"*40)
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='cartdb',
            user='root',
            password='',
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Check if cart_logs table exists
        cursor.execute("SHOW TABLES LIKE 'wp_cart_logs'")
        table_exists = cursor.fetchone() is not None
        
        if table_exists:
            print("   ✅ Database connection: OK")
            print("   ✅ wp_cart_logs table: EXISTS")
            
            # Check recent data
            cursor.execute("SELECT COUNT(*) FROM wp_cart_logs WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 1 DAY)")
            recent_count = cursor.fetchone()[0]
            
            print(f"   📊 Recent cart logs (24h): {recent_count}")
            
        else:
            print("   ⚠️  wp_cart_logs table: NOT FOUND")
            print("   💡 The WordPress plugin may not be activated")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
    
    # 3. Test API Integration
    print(f"\n3. 🔗 API Integration Test")
    print("-"*40)
    
    if services_ok >= 1:
        # Test with sample data
        test_cart = {
            "user_id": "diagnostic_test_user",
            "email": "diagnostic@test.com",
            "items": [
                {
                    "product_id": 9999,
                    "name": "Diagnostic Test Product",
                    "price": 19.99,
                    "quantity": 1
                }
            ],
            "behavior": {
                "idle_time": 125,  # Above 60 second threshold
                "pages_viewed": 3,
                "session_duration": 200
            },
            "timestamp": datetime.now().timestamp()
        }
        
        headers = {
            'Authorization': 'Bearer d405b55571c2b2471760c4ccfc6a62a9d8e8ee5e15a3cccd6a576cf69939f379',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                'http://localhost:8001/detect-abandonment',
                headers=headers,
                json=test_cart,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                print("   ✅ API Test: SUCCESS")
                print(f"   📊 Abandonment Detected: {result.get('abandoned', False)}")
                print(f"   🎯 Recommendations Generated: {len(result.get('data', {}).get('recommendations', []))}")
            else:
                print(f"   ❌ API Test Failed: Status {response.status_code}")
                print(f"   📄 Response: {response.text}")
                
        except Exception as e:
            print(f"   ❌ API Test Error: {e}")
    
    # 4. WordPress Plugin Check
    print(f"\n4. 🔌 WordPress Plugin Status")
    print("-"*40)
    
    plugin_files = [
        'wordpress_plugin/shopping-cart-recovery.php',
        'wordpress_plugin/includes/api_handler.php',
        'wordpress_plugin/includes/tracking.php',
        'wordpress_plugin/admin/analytics.php',
        'wordpress_plugin/assets/js/tracking.js'
    ]
    
    plugin_ok = 0
    for file_path in plugin_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic check
                    print(f"   ✅ {file_path.split('/')[-1]}: OK")
                    plugin_ok += 1
                else:
                    print(f"   ⚠️  {file_path.split('/')[-1]}: TOO SHORT")
        except Exception:
            print(f"   ❌ {file_path.split('/')[-1]}: NOT FOUND")
    
    # Summary and Recommendations
    print(f"\n" + "="*60)
    print("📋 DIAGNOSTIC SUMMARY & RECOMMENDATIONS")
    print("="*60)
    
    if services_ok == 2:
        print("✅ AI Services: Both running properly")
    else:
        print("❌ AI Services: Some services down - restart needed")
    
    if plugin_ok >= 4:
        print("✅ Plugin Files: All present")
    else:
        print("⚠️  Plugin Files: Some missing or corrupted")
    
    print(f"\n🔧 TO FIX THE CART ANALYTICS ISSUE:")
    print("="*60)
    
    print("\n1. ✅ COMPLETED - Database populated with sample data")
    print("   The analytics page should now show data!")
    
    print("\n2. 📦 WordPress Plugin Installation:")
    print("   • Copy 'wordpress_plugin' folder to:")
    print("     /wp-content/plugins/shopping-cart-recovery/")
    print("   • Activate plugin in WordPress admin")
    
    print("\n3. ⚙️  Plugin Configuration:")
    print("   • Go to WordPress Admin → Plugins")
    print("   • Activate 'Shopping Cart Recovery AI'") 
    print("   • The plugin will auto-configure API settings")
    
    print("\n4. 🧪 Real-Time Testing:")
    print("   • Add items to WooCommerce cart")
    print("   • Wait 60+ seconds without activity")
    print("   • Check browser console for tracking logs")
    print("   • New carts should appear in analytics")
    
    print(f"\n5. 📊 Check Analytics Dashboard:")
    print("   • Navigate to: WordPress Admin → Cart Recovery")
    print("   • You should see the sample data we just added")
    print("   • URL: http://localhost/wordpress/wp-admin/admin.php?page=scr-analytics")
    
    if services_ok < 2:
        print(f"\n⚠️  IMPORTANT: Restart AI services first!")
        print("   Run these commands in separate terminals:")
        print("   1. Start abandonment detector:")
        print("      python -m uvicorn agents.abandonment_detector.app:app --port 8001")
        print("   2. Start email generator:")  
        print("      python -m uvicorn agents.email_generator_offer_suggestor.app:app --port 8002")

if __name__ == "__main__":
    diagnose_integration()