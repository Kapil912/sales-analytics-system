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


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Same output format, new internal implementation style.
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    report = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_tx = len(transactions)

    # HEADER
    report.append("==============================================")
    report.append("             SALES ANALYTICS REPORT           ")
    report.append("==============================================")
    report.append(f"Generated: {now}")
    report.append(f"Records Processed: {total_tx}")
    report.append("==============================================\n")

    # SUMMARY
    total_revenue = calculate_total_revenue(transactions)
    avg_order = total_revenue / total_tx if total_tx else 0

    dates = sorted(t["Date"] for t in transactions)
    report.append("OVERALL SUMMARY")
    report.append("----------------------------------------------")
    report.append(f"Total Revenue: ₹{total_revenue:,.2f}")
    report.append(f"Total Transactions: {total_tx}")
    report.append(f"Average Order Value: ₹{avg_order:,.2f}")
    report.append(f"Date Range: {dates[0]} to {dates[-1]}\n")

    # REGION PERFORMANCE
    region_stats = region_wise_sales(transactions)
    report.append("REGION-WISE PERFORMANCE")
    report.append("----------------------------------------------")
    report.append(f"{'Region':10} {'Sales':15} {'% of Total':15} {'Transactions'}")

    for region, stats in region_stats.items():
        report.append(
            f"{region:10} ₹{stats['total_sales']:,.0f}   {stats['percentage']:.2f}%        {stats['transaction_count']}"
        )
    report.append("")

    # TOP PRODUCTS
    top_products = top_selling_products(transactions)
    report.append("TOP 5 PRODUCTS")
    report.append("----------------------------------------------")
    report.append(f"{'Rank':5} {'Product':20} {'Qty Sold':10} {'Revenue'}")

    for i, (name, qty, rev) in enumerate(top_products, start=1):
        report.append(f"{i:<5} {name:20} {qty:<10} ₹{rev:,.0f}")
    report.append("")

    # CUSTOMERS
    customers = customer_analysis(transactions)
    report.append("TOP 5 CUSTOMERS")
    report.append("----------------------------------------------")
    report.append(f"{'Rank':5} {'Customer':10} {'Total Spent':15} {'Orders'}")

    cust_sorted = sorted(
        customers.items(),
        key=lambda x: x[1]["total_spent"],
        reverse=True
    )[:5]

    for i, (cid, stats) in enumerate(cust_sorted, start=1):
        report.append(
            f"{i:<5} {cid:10} ₹{stats['total_spent']:,.0f}       {stats['purchase_count']}"
        )

    report.append("")

    # DAILY TREND
    daily_stats = daily_sales_trend(transactions)
    report.append("DAILY SALES TREND")
    report.append("----------------------------------------------")
    report.append(f"{'Date':12} {'Revenue':12} {'Transactions':12} {'Unique Cust'}")

    for date, stats in daily_stats.items():
        report.append(
            f"{date:12} ₹{stats['revenue']:,.0f}      {stats['transaction_count']:10}     {stats['unique_customers']}"
        )
    report.append("")

    # PERFORMANCE
    peak_date, peak_rev, peak_cnt = find_peak_sales_day(transactions)
    report.append("PRODUCT PERFORMANCE ANALYSIS")
    report.append("----------------------------------------------")
    report.append(f"Best Sales Day: {peak_date} (₹{peak_rev:,.0f}, {peak_cnt} transactions)\n")

    low_items = low_performing_products(transactions)
    report.append("Low Performing Products (Qty < 10):")
    for name, qty, rev in low_items:
        report.append(f" - {name}: Qty {qty}, Revenue ₹{rev:,.0f}")
    report.append("")

    # ENRICHMENT SUMMARY
    total = len(enriched_transactions)
    success = sum(tx["API_Match"] for tx in enriched_transactions)
    percent = (success / total * 100) if total else 0

    report.append("API ENRICHMENT SUMMARY")
    report.append("----------------------------------------------")
    report.append(f"Total Products Enriched: {total}")
    report.append(f"Successful Matches: {success} ({percent:.2f}%)")

    failed = [tx for tx in enriched_transactions if not tx["API_Match"]]
    if failed:
        report.append("Products That Could Not Be Enriched:")
        for tx in failed:
            report.append(f" - {tx['ProductID']} ({tx['ProductName']})")
        report.append("")

    # SAVE REPORT
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Sales report saved to: {output_file}")
