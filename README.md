# Sales Analytics System

**Student Name:** Kapil Goyla  
**Student ID:** 25071901  
**Email:** kapilgoyla83@gmail.com  
**Date:** 18/01/2026 

---

## Overview
This project provides an end-to-end Sales Analytics solution that includes:

- Reading and preprocessing raw sales data  
- Validating and optionally filtering transactions  
- Performing multiple analytical computations  
- Integrating with the DummyJSON API for product enrichment  
- Generating a formatted final sales report  
- Running all steps through a single main application workflow  

The entire pipeline follows the assignment specification and produces all required output files.

---

## Folder Structure
```
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py
```

---

## How to Run the Project

### 1. Install Dependencies
Only one external dependency (`requests`) is required:

```
pip install -r requirements.txt
```

### 2. Run the Main Program
```
python main.py
```

This executes the workflow.

---

## Sample Console Output
Below is an example of the expected program execution:

```
========================================
        SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 80 raw lines

[2/10] Parsing and cleaning data...
✓ Parsed 80 records

[3/10] Filter Options Available:
Regions: East, North, South, West
Amount Range: ₹257 - ₹818,960

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 70 | Invalid: 10

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
Fetched 100 products from API (bulk mode)
✓ Fetched 100 products

[7/10] Enriching sales data...
✓ Enriched 70/70 transactions (100.0%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
========================================
```

## Sample Output 
```
========================================
        SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 80 raw lines

[2/10] Parsing and cleaning data...
✓ Parsed 80 records

[3/10] Filter Options Available:
Regions: , East, North, South, West
Amount Range: ₹-8,982 - ₹818,960

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 70 | Invalid: 10

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
Fetched 100 products from API (bulk mode).
✓ Fetched 100 products

[7/10] Enriching sales data...
✓ Enriched 70/70 transactions (100.0%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
Sales report saved to: output/sales_report.txt
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
========================================
```