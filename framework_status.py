#!/usr/bin/env python3
"""
Framework Status and Usage Guide

Shows the current status of the CSV to EDI mapper framework and provides usage examples.
"""

import os
import glob


def show_framework_status():
    """Display the current framework status."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 CSV to EDI Mapper Framework")
    print("=" * 50)
    
    # Check for required files
    required_files = {
        'csv_to_edi_mapper.py': 'Core mapping framework',
        'process_order.py': 'Utility script for processing orders',
        'validate_csv.py': 'CSV format validator',
        'test_mapper.py': 'Test script with examples',
        'README.md': 'Documentation',
        'MAPPING_CONFIG.md': 'Field mapping configuration'
    }
    
    print("📁 Framework Files Status:")
    for filename, description in required_files.items():
        filepath = os.path.join(current_dir, filename)
        if os.path.exists(filepath):
            print(f"   ✅ {filename} - {description}")
        else:
            print(f"   ❌ {filename} - {description} (MISSING)")
    
    # Check for base XML templates in inputs folder
    inputs_dir = os.path.join(current_dir, 'inputs')
    if os.path.exists(inputs_dir):
        xml_files = glob.glob(os.path.join(inputs_dir, "*.XML"))
        print(f"\n📄 Input XML Templates Found: {len(xml_files)}")
        for xml_file in xml_files:
            basename = os.path.basename(xml_file)
            if basename == "baseEDI.XML":
                print(f"   📋 inputs/{basename} (Base template)")
            else:
                print(f"   📄 inputs/{basename}")
    
    # Check for any remaining XML files in root
    root_xml_files = glob.glob(os.path.join(current_dir, "*.XML"))
    if root_xml_files:
        print(f"\n📄 Other XML Files: {len(root_xml_files)}")
        for xml_file in root_xml_files:
            basename = os.path.basename(xml_file)
            print(f"   📄 {basename}")
    
    # Check for CSV files in inputs folder
    inputs_dir = os.path.join(current_dir, 'inputs')
    if os.path.exists(inputs_dir):
        csv_files = glob.glob(os.path.join(inputs_dir, "*.csv"))
        print(f"\n📊 Input CSV Files Found: {len(csv_files)}")
        for csv_file in csv_files:
            basename = os.path.basename(csv_file)
            print(f"   📋 inputs/{basename}")
    else:
        csv_files = glob.glob(os.path.join(current_dir, "*.csv"))
        print(f"\n📊 CSV Files Found: {len(csv_files)}")
        for csv_file in csv_files:
            basename = os.path.basename(csv_file)
            print(f"   📋 {basename}")
    
    print("🔧 Usage Examples:")
    print("-" * 30)
    print("1. Process with default files:")
    print("   python process_order.py")
    print("\n2. Validate CSV format:")
    print("   python validate_csv.py inputs/order.csv")
    print("\n3. Run framework tests:")
    print("   python test_mapper.py")
    print("\n4. Direct processing:")
    print("   python csv_to_edi_mapper.py")
    print("\n5. Custom files:")
    print("   python process_order.py my_order.csv")
    
    print("\n📝 CSV Structure (inputs/order.csv):")
    print("-" * 40)
    print("   ###ORD-HEADER")
    print("   CUST-ORDER,CUST-ADDR-CODE,CUST-ADDR-NAME,...")
    print("   CUST-001,CA0,Waitrose & Partners Head Office,...")
    print("   ###ORD-HEADER-END")
    print("   ###ORD-LINES")
    print("   LINE-NO,LINE-CODE,LINE-DESC,LINE-QUANT,...")
    print("   1,32815,Product Name,500,...")
    print("   ###ORD-LINES-END")
    
    print("\n📊 Field Mappings:")
    print("-" * 20)
    print("   ✅ 15 header fields mapped to XML elements")
    print("   ✅ Customer address (Code, Name, Address1-3)")
    print("   ✅ Delivery information (Code, Name, Address)")
    print("   ✅ Invoice details (Code, Name, Address)")
    print("   ✅ Order totals (Units, Value)")
    print("   ✅ Automatic XML element creation")
    
    print(f"\n📤 Output Directory:")
    outputs_dir = os.path.join(current_dir, 'outputs')
    if os.path.exists(outputs_dir):
        output_files = [f for f in os.listdir(outputs_dir) if f.endswith('.XML')]
        print(f"   📁 {outputs_dir}")
        print(f"   📄 {len(output_files)} XML files generated")
        for xml_file in output_files[:3]:  # Show first 3 files
            print(f"      • {xml_file}")
        if len(output_files) > 3:
            print(f"      • ... and {len(output_files) - 3} more")
    else:
        print(f"   📁 {outputs_dir} (will be created on first run)")
    
    print(f"\n📂 Working Directory: {current_dir}")
    print("=" * 50)


if __name__ == "__main__":
    show_framework_status()