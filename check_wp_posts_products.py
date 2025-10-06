#!/usr/bin/env python3
"""
Check WooCommerce products from wp_posts table
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
        cursor.execute('SELECT ID, post_title FROM wp_posts WHERE post_type = "product" AND post_status = "publish"')
        products = cursor.fetchall()
        print(f'\nFound {len(products)} products in wp_posts')

        # Get product details with prices
        print('\nProduct details from wp_posts:')
        for product_id, title in products[:15]:  # Show first 15
            # Get price from postmeta
            cursor.execute('SELECT meta_value FROM wp_postmeta WHERE post_id = %s AND meta_key = "_price"', (product_id,))
            price_result = cursor.fetchone()
            price = price_result[0] if price_result else 'N/A'

            # Get regular price
            cursor.execute('SELECT meta_value FROM wp_postmeta WHERE post_id = %s AND meta_key = "_regular_price"', (product_id,))
            reg_price_result = cursor.fetchone()
            reg_price = reg_price_result[0] if reg_price_result else price

            # Get description
            cursor.execute('SELECT post_content FROM wp_posts WHERE ID = %s', (product_id,))
            desc_result = cursor.fetchone()
            description = desc_result[0][:150] + '...' if desc_result and desc_result[0] else 'N/A'

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

            print(f'  ID: {product_id}')
            print(f'  Title: {title}')
            print(f'  Price: ${price} (Regular: ${reg_price})')
            print(f'  Category: {category}')
            print(f'  Description: {description}')
            print('-' * 50)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()