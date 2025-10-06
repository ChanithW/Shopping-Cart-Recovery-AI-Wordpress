#!/usr/bin/env python3
"""
Check existing WooCommerce products for recommendations
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='cartdb'
        )

        cursor = conn.cursor()

        # Check WooCommerce products from wp_posts
        print('Checking WooCommerce products from wp_posts...')
        cursor.execute('SELECT ID, post_title FROM wp_posts WHERE post_type = "product" AND post_status = "publish" LIMIT 20')
        products = cursor.fetchall()
        print(f'\nWooCommerce products found: {len(products)}')
        for product in products[:10]:  # Show first 10
            print(f'  ID: {product[0]}, Title: {product[1]}')

        # Get product prices and categories from postmeta
        if products:
            print('\nGetting product details...')
            for product_id, title in products[:5]:  # Check first 5
                # Get price
                cursor.execute('SELECT meta_value FROM wp_postmeta WHERE post_id = %s AND meta_key = "_price"', (product_id,))
                price_result = cursor.fetchone()
                price = price_result[0] if price_result else 'N/A'

                # Get category
                cursor.execute('''
                    SELECT t.name FROM wp_terms t
                    JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id
                    JOIN wp_term_relationships tr ON tt.term_taxonomy_id = tr.term_taxonomy_id
                    WHERE tr.object_id = %s AND tt.taxonomy = "product_cat"
                    LIMIT 1
                ''', (product_id,))
                cat_result = cursor.fetchone()
                category = cat_result[0] if cat_result else 'N/A'

                print(f'  {title}: ${price} (Category: {category})')

        # Check wp_products table
        print('\nChecking wp_products table...')
        cursor.execute('DESCRIBE wp_products')
        columns = cursor.fetchall()
        print('wp_products table structure:')
        for col in columns:
            print(f'  {col[0]}: {col[1]}')

        cursor.execute('SELECT COUNT(*) FROM wp_products')
        count = cursor.fetchone()[0]
        print(f'\nwp_products has {count} records')

        if count > 0:
            cursor.execute('SELECT * FROM wp_products LIMIT 5')
            records = cursor.fetchall()
            print('\nFirst 5 records from wp_products:')
            for record in records:
                print(f'  {record}')

        cursor.close()
        conn.close()

    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()