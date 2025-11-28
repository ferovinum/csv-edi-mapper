#!/usr/bin/env python3
"""
CSV to EDI Utility Script

Simple utility to process CSV files with the EDI mapper framework.
Automatically detects the base XML file and processes CSV input.
"""

import os
import sys
import glob
from csv_to_edi_mapper import CSVToEDIMapper


def main():
    """Main utility function."""
    print("CSV to EDI Mapper Utility")
    print("=" * 40)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Use default files or accept command line arguments
    if len(sys.argv) == 1:
        # Use default files from inputs folder
        csv_file = os.path.join(current_dir, "inputs", "order.csv")
        base_xml = os.path.join(current_dir, "inputs", "baseEDI.XML")
        print("Using default files:")
    elif len(sys.argv) == 2:
        # Custom CSV file with default base XML from inputs folder
        csv_file = sys.argv[1]
        base_xml = os.path.join(current_dir, "inputs", "baseEDI.XML")
        print("Using custom CSV with default base XML:")
    elif len(sys.argv) == 3:
        # Both custom files
        csv_file = sys.argv[1]
        base_xml = sys.argv[2]
        print("Using custom files:")
    else:
        print("Usage: python process_order.py [csv_file] [base_xml_file]")
        print("Examples:")
        print("  python process_order.py                    # Use inputs/order.csv and inputs/baseEDI.XML")
        print("  python process_order.py my_order.csv       # Use my_order.csv and inputs/baseEDI.XML")
        print("  python process_order.py order.csv base.xml # Use custom files")
        sys.exit(1)
    
    # Validate files
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    if not os.path.exists(base_xml):
        print(f"Error: Base XML file not found: {base_xml}")
        sys.exit(1)
    
    print(f"Input CSV: {os.path.basename(csv_file)}")
    print(f"Base XML: {os.path.basename(base_xml)}")
    print()
    
    # Process the file
    mapper = CSVToEDIMapper(base_xml)
    success = mapper.process(csv_file)
    
    if success:
        print("\n" + "=" * 40)
        print("✅ Processing completed successfully!")
        print("=" * 40)
        
        # Show summary
        cust_order = mapper.header_data.get('CUST-ORDER', 'UNKNOWN')
        output_file = f"WAITROSE_{cust_order}.XML"
        
        print(f"📄 Output file: outputs/{output_file}")
        print(f"📋 Header fields: {len(mapper.header_data)}")
        print(f"📦 Line items: {len(mapper.line_items)}")
        
        if mapper.header_data:
            print("\n📊 Order Summary:")
            for key, value in mapper.header_data.items():
                if value:  # Only show non-empty values
                    print(f"   {key}: {value}")
    else:
        print("\n❌ Processing failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()