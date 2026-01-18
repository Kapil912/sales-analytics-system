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

