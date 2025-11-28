#!/usr/bin/env python3
"""
CSV Format Validator

Validates that CSV files follow the expected format for the EDI mapper.
"""

import csv
import sys
import os


def validate_csv_format(csv_path):
    """
    Validate that the CSV file has the correct format.
    
    Args:
        csv_path: Path to the CSV file to validate
        
    Returns:
        tuple: (is_valid, errors)
    """
    errors = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
    except Exception as e:
        return False, [f"Failed to read CSV file: {e}"]
    
    if not rows:
        return False, ["CSV file is empty"]
    
    # Check for required markers
    markers_found = set()
    required_markers = {
        "###ORD-HEADER",
        "###ORD-HEADER-END", 
        "###ORD-LINES",
        "###ORD-LINES-END"
    }
    
    for i, row in enumerate(rows):
        if row and len(row) > 0:
            marker = row[0].strip()
            if marker in required_markers:
                markers_found.add(marker)
    
    missing_markers = required_markers - markers_found
    if missing_markers:
        errors.append(f"Missing required markers: {', '.join(missing_markers)}")
    
    # Check section structure
    header_start = None
    header_end = None
    lines_start = None
    lines_end = None
    
    for i, row in enumerate(rows):
        if not row:
            continue
        marker = row[0].strip()
        
        if marker == "###ORD-HEADER":
            header_start = i
        elif marker == "###ORD-HEADER-END":
            header_end = i
        elif marker == "###ORD-LINES":
            lines_start = i
        elif marker == "###ORD-LINES-END":
            lines_end = i
    
    # Validate header section
    if header_start is not None and header_end is not None:
        if header_end <= header_start:
            errors.append("Header end marker must come after header start marker")
        else:
            header_rows = rows[header_start + 1:header_end]
            if not header_rows:
                errors.append("Header section is empty")
            else:
                # Check for CUST-ORDER field
                has_cust_order = False
                for row in header_rows:
                    if len(row) >= 2 and row[0].strip() == "CUST-ORDER":
                        has_cust_order = True
                        if not row[1].strip():
                            errors.append("CUST-ORDER field is required but empty")
                        break
                
                if not has_cust_order:
                    errors.append("CUST-ORDER field is required in header section")
    
    # Validate lines section
    if lines_start is not None and lines_end is not None:
        if lines_end <= lines_start:
            errors.append("Lines end marker must come after lines start marker")
        else:
            lines_rows = rows[lines_start + 1:lines_end]
            if not lines_rows:
                errors.append("Lines section is empty")
    
    return len(errors) == 0, errors


def main():
    """Main validation function."""
    if len(sys.argv) != 2:
        print("Usage: python validate_csv.py <csv_file>")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    
    print(f"Validating CSV file: {csv_file}")
    print("=" * 50)
    
    is_valid, errors = validate_csv_format(csv_file)
    
    if is_valid:
        print("✅ CSV file format is VALID")
        print("The file can be processed by the EDI mapper")
    else:
        print("❌ CSV file format is INVALID")
        print("\nErrors found:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    print("=" * 50)


if __name__ == "__main__":
    main()