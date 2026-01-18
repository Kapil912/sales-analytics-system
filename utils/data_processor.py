def calculate_total_revenue(transactions):
    """
    Computes total revenue across all transactions.
    """
    return sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)



def region_wise_sales(transactions):
    """
    Builds region-level sales summary sorted by total sales (DESC).
    """

    region_stats = {}
    overall_total = 0.0

    # Aggregate
    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        overall_total += amount

        stats = region_stats.setdefault(region, {"total_sales": 0.0, "transaction_count": 0})
        stats["total_sales"] += amount
        stats["transaction_count"] += 1

    # Add percentages
    for region, stats in region_stats.items():
        stats["percentage"] = (stats["total_sales"] / overall_total * 100) if overall_total else 0.0

    # Sort by total sales
    return dict(sorted(region_stats.items(), key=lambda x: x[1]["total_sales"], reverse=True))



def top_selling_products(transactions, n=5):
    """
    Returns top n products by quantity sold.
    """

    product_stats = {}

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        stats = product_stats.setdefault(name, {"qty": 0, "rev": 0.0})
        stats["qty"] += qty
        stats["rev"] += revenue

    # Convert to list of tuples
    products = [(name, s["qty"], s["rev"]) for name, s in product_stats.items()]

    # Sort by qty DESC
    products.sort(key=lambda x: x[1], reverse=True)

    return products[:n]



def customer_analysis(transactions):
    """
    Returns spending patterns and behavior for each customer.
    """

    customers = {}

    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        stats = customers.setdefault(cid, {"spent": 0.0, "count": 0, "products": set()})
        stats["spent"] += amount
        stats["count"] += 1
        stats["products"].add(product)

    # Final formatting
    final = {}
    for cid, s in customers.items():
        avg = s["spent"] / s["count"] if s["count"] else 0
        final[cid] = {
            "total_spent": s["spent"],
            "purchase_count": s["count"],
            "avg_order_value": avg,
            "products_bought": list(s["products"])
        }

    # Sort DESC by spending
    return dict(sorted(final.items(), key=lambda x: x[1]["total_spent"], reverse=True))



