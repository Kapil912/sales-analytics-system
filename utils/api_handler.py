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



