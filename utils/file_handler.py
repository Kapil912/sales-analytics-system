def read_sales_data(filename):
    """
    Reads sales data from a text file.
    Tries multiple encodings and returns cleaned lines (excluding header).
    """

    encodings = ["utf-8", "latin-1", "cp1252"]

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = f.read().splitlines()
            break
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except UnicodeDecodeError:
            continue
    else:
        print(f"Error: Could not decode '{filename}' using available encodings.")
        return []

    # Strip header and blank lines
    return [line for line in lines[1:] if line.strip()]



def parse_transactions(raw_lines):
    """
    Converts raw pipe-delimited lines into structured transaction dictionaries.
    """

    cleaned = []

    for line in raw_lines:
        parts = line.split("|")

        # Should have exactly 8 fields
        if len(parts) != 8:
            continue

        (
            tid,
            date,
            pid,
            pname,
            qty,
            price,
            cid,
            region
        ) = parts

        # Clean product name and numeric fields
        pname = pname.replace(",", " ")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            continue

        cleaned.append({
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        })

    return cleaned



def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates each transaction, then applies optional region and amount filters.
    """

    valid = []
    invalid = 0

    # ---------- VALIDATION ----------
    for tx in transactions:
        quantity = tx["Quantity"]
        price = tx["UnitPrice"]

        if (
            quantity <= 0 or
            price <= 0 or
            not tx["TransactionID"].startswith("T") or
            not tx["ProductID"].startswith("P") or
            not tx["CustomerID"].startswith("C") or
            not tx["Region"]
        ):
            invalid += 1
            continue

        valid.append(tx)

    # Counters for summary
    filtered_by_region = 0
    filtered_by_amount = 0

    # ---------- REGION FILTER ----------
    if region:
        filtered = []
        for tx in valid:
            if tx["Region"] == region:
                filtered.append(tx)
            else:
                filtered_by_region += 1
        valid = filtered

    # ---------- AMOUNT FILTER ----------
    if min_amount is not None or max_amount is not None:
        filtered = []

        for tx in valid:
            amount = tx["Quantity"] * tx["UnitPrice"]

            if min_amount is not None and amount < min_amount:
                filtered_by_amount += 1
                continue
            if max_amount is not None and amount > max_amount:
                filtered_by_amount += 1
                continue

            filtered.append(tx)

        valid = filtered

    # ---------- SUMMARY ----------
    summary = {
        "total_input": len(transactions),
        "invalid": invalid,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid),
    }

    return valid, invalid, summary
