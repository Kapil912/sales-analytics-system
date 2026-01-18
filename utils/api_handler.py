import requests
import datetime
import os
from utils.data_processor import *


def fetch_all_products():
    """
    Fetches first 100 products (limit=100).
    Bulk list is NOT used for enrichment anymore,
    but required by assignment to demonstrate a GET list call.
    """

    url = "https://dummyjson.com/products?limit=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])

        print(f"Fetched {len(products)} products from API (bulk mode).")
        return products

    except Exception as e:
        print("Bulk API fetch failed:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """

    product_map = {}

    for product in api_products:
        pid = product.get("id")

        # Extract required fields only
        info = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
            "price": product.get("price")
        }

        product_map[pid] = info

    return product_map


def enrich_sales_data(transactions, product_mapping=None):
    """
    New approach:
      - Converts P101 → 101
      - Makes direct API call:
            https://dummyjson.com/products/101
    """

    enriched_list = []

    for tx in transactions:
        new_tx = tx.copy()

        # Extract numeric ID: 'P101' → 101
        pid_raw = tx.get("ProductID", "")
        try:
            num_id = int(pid_raw[1:])
        except:
            num_id = None

        if num_id is None:
            new_tx.update({
                "API_Category": None,
                "API_Brand": None,
                "API_Rating": None,
                "API_Match": False
            })
            enriched_list.append(new_tx)
            continue

        # Direct API product lookup
        api_url = f"https://dummyjson.com/products/{num_id}"
        try:
            res = requests.get(api_url, timeout=8)
            if res.status_code == 200:
                pdata = res.json()
            else:
                pdata = None
        except Exception:
            pdata = None

        if pdata:
            new_tx["API_Category"] = pdata.get("category")
            new_tx["API_Brand"] = pdata.get("brand")
            new_tx["API_Rating"] = pdata.get("rating")
            new_tx["API_Match"] = True
        else:
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False

        enriched_list.append(new_tx)

    return enriched_list


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched data in pipe-delimited format.
    """

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for tx in enriched_transactions:
            row = [str(tx.get(h, "None")) for h in headers]
            f.write("|".join(row) + "\n")



