import sys
from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data,
    generate_sales_report
)
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def main():
    print("========================================")
    print("        SALES ANALYTICS SYSTEM")
    print("========================================\n")

    try:
        # -----------------------------------------------------------
        # [1/10] READ SALES DATA
        # -----------------------------------------------------------
        print("[1/10] Reading sales data...")
        raw_data = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_data)} raw lines\n")

        # -----------------------------------------------------------
        # [2/10] PARSE DATA
        # -----------------------------------------------------------
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_data)
        print(f"✓ Parsed {len(transactions)} records\n")

        # -----------------------------------------------------------
        # [3/10] FILTER OPTIONS
        # -----------------------------------------------------------
        print("[3/10] Filter Options Available:")

        regions = sorted({t["Region"] for t in transactions})
        print("Regions:", ", ".join(regions))

        amounts = [t["Quantity"] * t["UnitPrice"] for t in transactions]
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        # Ask user
        region_filter = None
        min_amt = None
        max_amt = None

        if input("Do you want to filter data? (y/n): ").lower() == "y":
            print("\n--- APPLY FILTERS ---")

            r = input("Enter region to filter (or press Enter to skip): ").strip()
            if r in regions:
                region_filter = r

            try:
                m1 = input("Minimum amount (or press Enter to skip): ").strip()
                min_amt = float(m1) if m1 else None

                m2 = input("Maximum amount (or press Enter to skip): ").strip()
                max_amt = float(m2) if m2 else None
            except:
                print("Invalid amount entered. Filters ignored.")
                min_amt = max_amt = None

        print()

        # -----------------------------------------------------------
        # [4/10] VALIDATE + APPLY FILTERS
        # -----------------------------------------------------------
        print("[4/10] Validating transactions...")

        valid_tx, invalid_count, summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amt,
            max_amount=max_amt
        )

        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}\n")

        # -----------------------------------------------------------
        # [5/10] ANALYZE SALES DATA
        # -----------------------------------------------------------
        print("[5/10] Analyzing sales data...")

        # These calls ensure preprocessing is done
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)
        daily_sales_trend(valid_tx)
        find_peak_sales_day(valid_tx)
        low_performing_products(valid_tx)

        print("✓ Analysis complete\n")

        # -----------------------------------------------------------
        # [6/10] FETCH API PRODUCTS
        # -----------------------------------------------------------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # -----------------------------------------------------------
        # [7/10] ENRICH SALES DATA
        # -----------------------------------------------------------
        print("[7/10] Enriching sales data...")

        product_map = create_product_mapping(api_products)
        enriched = enrich_sales_data(valid_tx, product_map)

        match_count = sum(tx["API_Match"] for tx in enriched)
        total = len(enriched)
        pct = (match_count / total * 100) if total else 0

        print(f"✓ Enriched {match_count}/{total} transactions ({pct:.1f}%)\n")

        # -----------------------------------------------------------
        # [8/10] SAVE ENRICHED DATA
        # -----------------------------------------------------------
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # -----------------------------------------------------------
        # [9/10] GENERATE REPORT
        # -----------------------------------------------------------
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched)
        print("✓ Report saved to: output/sales_report.txt\n")

        # -----------------------------------------------------------
        # [10/10] COMPLETE
        # -----------------------------------------------------------
        print("[10/10] Process Complete!")
        print("========================================")

    except Exception as e:
        print("\nAn error occurred:")
        print(str(e))
        print("The program was unable to complete the process.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
