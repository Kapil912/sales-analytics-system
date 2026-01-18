import requests



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

