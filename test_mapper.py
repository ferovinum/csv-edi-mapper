#!/usr/bin/env python3
"""
Test script for the CSV to EDI Mapper framework.

This script tests the mapper with the actual order.csv and baseEDI.XML files.
"""

import os
from csv_to_edi_mapper import CSVToEDIMapper


def test_mapper():
    """Test the CSV to EDI mapper with the actual order data."""
    
    # Define file paths using the required files from inputs folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "inputs", "order.csv")
    base_xml_file = os.path.join(base_dir, "inputs", "baseEDI.XML")
    
    print("🧪 Testing CSV to EDI Mapper Framework")
    print("=" * 50)
    print(f"Input CSV: {os.path.basename(csv_file)}")
    print(f"Base XML: {os.path.basename(base_xml_file)}")
    print()
    
    # Create mapper instance
    mapper = CSVToEDIMapper(base_xml_file)
    
    # Process the CSV file
    success = mapper.process(csv_file)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
        # Display extracted header data
        print("\n📋 Extracted Header Data:")
        for key, value in mapper.header_data.items():
            print(f"   {key}: {value}")
        
        print(f"\n📦 Extracted Line Items: {len(mapper.line_items)}")
        for i, item in enumerate(mapper.line_items, 1):
            print(f"   Line {i}:")
            for field, value in item.items():
                if value:  # Only show non-empty fields
                    print(f"      {field}: {value}")
        
        # Show output information
        cust_order = mapper.header_data.get('CUST-ORDER', 'UNKNOWN')
        output_file = f"WAITROSE_{cust_order}.XML"
        print(f"\n📄 Generated Output: outputs/{output_file}")
        
    else:
        print("\n❌ TEST FAILED!")


if __name__ == "__main__":
    test_mapper()