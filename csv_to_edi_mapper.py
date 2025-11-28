#!/usr/bin/env python3
"""
CSV to EDI Mapper Framework

This script maps CSV order data to TrueCommerce XML format.
The CSV file should contain order header and line item sections marked with specific delimiters.
"""

import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List, Optional, Any
import os
import sys


class CSVToEDIMapper:
    """Main class for mapping CSV order data to TrueCommerce XML format."""
    
    def __init__(self, base_xml_path: str):
        """
        Initialize the mapper with the base XML template.
        
        Args:
            base_xml_path: Path to the base XML template file
        """
        self.base_xml_path = base_xml_path
        self.tree = None
        self.root = None
        self.header_data = {}
        self.line_items = []
        self.namespaces = {'tc': 'http://www.truecommerce.com/docs/order'}
        
    def load_base_xml(self) -> bool:
        """
        Load the base XML template.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.tree = ET.parse(self.base_xml_path)
            self.root = self.tree.getroot()
            return True
        except Exception as e:
            print(f"Error loading base XML: {e}")
            return False
    
    def parse_csv(self, csv_path: str) -> bool:
        """
        Parse the CSV file and extract header and line item data.
        
        The CSV structure should have:
        - Column A: Markers (###ORD-HEADER, ###ORD-HEADER-END, ###ORD-LINES, ###ORD-LINES-END)
        - Other columns: Field names and values
        
        Args:
            csv_path: Path to the CSV file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
            return self._extract_sections(rows)
            
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            return False
    
    def _extract_sections(self, rows: List[List[str]]) -> bool:
        """
        Extract header and line items from CSV rows based on markers.
        
        Args:
            rows: List of CSV rows
            
        Returns:
            bool: True if successful, False otherwise
        """
        current_section = None
        header_start = None
        header_end = None
        lines_start = None
        lines_end = None
        
        # Find section boundaries
        for i, row in enumerate(rows):
            if not row or len(row) == 0:
                continue
                
            marker = row[0].strip()
            
            if marker == "###ORD-HEADER":
                current_section = "header"
                header_start = i + 1
            elif marker == "###ORD-HEADER-END":
                header_end = i
            elif marker == "###ORD-LINES":
                current_section = "lines"
                lines_start = i + 1
            elif marker == "###ORD-LINES-END":
                lines_end = i
        
        # Extract header data
        if header_start is not None and header_end is not None:
            self.header_data = self._extract_header_data(rows[header_start:header_end])
        
        # Extract line items
        if lines_start is not None and lines_end is not None:
            self.line_items = self._extract_line_items(rows[lines_start:lines_end])
        
        return True
    
    def _extract_header_data(self, header_rows: List[List[str]]) -> Dict[str, Any]:
        """
        Extract header data from CSV rows.
        The first row contains field names, the second row contains values.
        
        Args:
            header_rows: Rows containing header data
            
        Returns:
            Dict containing header field mappings
        """
        header_data = {}
        
        if len(header_rows) >= 2:
            # First row has field names, second row has values
            field_names = [col.strip() for col in header_rows[0] if col and col.strip()]
            field_values = header_rows[1] if len(header_rows) > 1 else []
            
            for i, field_name in enumerate(field_names):
                if i < len(field_values) and field_values[i] and field_values[i].strip():
                    header_data[field_name] = field_values[i].strip()
        
        return header_data
    
    def _extract_line_items(self, line_rows: List[List[str]]) -> List[Dict[str, Any]]:
        """
        Extract line item data from CSV rows.
        
        Args:
            line_rows: Rows containing line item data
            
        Returns:
            List of dictionaries containing line item data
        """
        line_items = []
        
        if not line_rows:
            return line_items
        
        # Assume first row contains headers
        headers = [col.strip() for col in line_rows[0] if col.strip()]
        
        # Process data rows
        for row in line_rows[1:]:
            if len(row) > 0 and any(cell.strip() for cell in row):
                line_item = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        line_item[header] = row[i].strip()
                line_items.append(line_item)
        
        return line_items
    
    def map_header_data(self) -> bool:
        """
        Map header data from CSV to XML structure.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Map CUST-ORDER to OrderHeader/CustOrder
            if 'CUST-ORDER' in self.header_data:
                elem = self.root.find('.//OrderHeader/CustOrder', self.namespaces)
                if elem is not None:
                    elem.text = self.header_data['CUST-ORDER']
                    print(f"Updated CustOrder: {self.header_data['CUST-ORDER']}")
            
            # Map customer address fields to Document/DocHeader/CustAddr
            cust_addr = self.root.find('.//Document/DocHeader/CustAddr', self.namespaces)
            if cust_addr is not None:
                self._update_or_create_element(cust_addr, 'Code', self.header_data.get('CUST-ADDR-CODE'))
                self._update_or_create_element(cust_addr, 'Name', self.header_data.get('CUST-ADDR-NAME'))
                self._update_or_create_element(cust_addr, 'Address1', self.header_data.get('CUST-ADDR-ADDRESS1'))
                self._update_or_create_element(cust_addr, 'Address2', self.header_data.get('CUST-ADDR-ADDRESS2'))
                self._update_or_create_element(cust_addr, 'Address3', self.header_data.get('CUST-ADDR-ADDRESS3'))
            
            # Map delivery due date to Document/OrderHeader/Delivery/ReqDel/Date (corrected path)
            req_del = self.root.find('.//Document/OrderHeader/Delivery/ReqDel', self.namespaces)
            if req_del is not None and 'DELIVERY-DUE-DATE' in self.header_data:
                date_elem = req_del.find('Date')
                if date_elem is not None:
                    date_elem.text = self.header_data['DELIVERY-DUE-DATE']
                    print(f"Updated Delivery Due Date: {self.header_data['DELIVERY-DUE-DATE']}")
            
            # Map delivery address fields to Document/OrderHeader/Delivery/DeliverTo (corrected path)
            deliver_to = self.root.find('.//Document/OrderHeader/Delivery/DeliverTo', self.namespaces)
            if deliver_to is not None:
                self._update_or_create_element(deliver_to, 'Code', self.header_data.get('DELIVERY-TO-CODE'))
                self._update_or_create_element(deliver_to, 'Name', self.header_data.get('DELIVERY-TO-NAME'))
                self._update_or_create_element(deliver_to, 'Address1', self.header_data.get('DELIVERY-TO-ADDRESS1'))
            
            # Map invoice address fields to Document/OrderHeader/Locations/InvoiceTo (corrected path)
            invoice_to = self.root.find('.//Document/OrderHeader/Locations/InvoiceTo', self.namespaces)
            if invoice_to is not None:
                self._update_or_create_element(invoice_to, 'Code', self.header_data.get('INVOICE-TO-CODE'))
                self._update_or_create_element(invoice_to, 'Name', self.header_data.get('INVOICE-TO-NAME'))
                self._update_or_create_element(invoice_to, 'Address1', self.header_data.get('INVOICE-TO-ADDRESS1'))
            
            # Map order totals to Document/OrderHeader (corrected path)
            order_header = self.root.find('.//Document/OrderHeader', self.namespaces)
            if order_header is not None:
                self._update_or_create_element(order_header, 'TotalOrderUnits', self.header_data.get('TOTAL-ORDER-UNITS'))
                self._update_or_create_element(order_header, 'TotalOrderVal', self.header_data.get('TOTAL-ORDER-VALUE'))
            
            return True
            
        except Exception as e:
            print(f"Error mapping header data: {e}")
            return False
    
    def _create_order_line_from_template(self, template, line_item):
        """
        Create a new OrderLine element from template with CSV line item data.
        
        Args:
            template: Base OrderLine element to copy
            line_item: Dictionary containing line item data
            
        Returns:
            New OrderLine element with mapped data
        """
        import copy
        
        # Create deep copy of template
        new_line = copy.deepcopy(template)
        
        # Map LINE-NO to OrderLine/LineNo
        line_no_elem = new_line.find('LineNo')
        if line_no_elem is not None and 'LINE-NO' in line_item:
            line_no_elem.text = line_item['LINE-NO']
        
        # Map LINE-CODE to OrderLine/Item/CustItem/Code
        cust_item_code = new_line.find('.//Item/CustItem/Code')
        if cust_item_code is not None and 'LINE-CODE' in line_item:
            cust_item_code.text = line_item['LINE-CODE']
        
        # Map LINE-DESC to OrderLine/Item/Desc1
        desc1_elem = new_line.find('.//Item/Desc1')
        if desc1_elem is not None and 'LINE-DESC' in line_item:
            desc1_elem.text = line_item['LINE-DESC']
        
        # Map LINE-QUANT to OrderLine/OrderQty/Unit
        order_qty_unit = new_line.find('.//OrderQty/Unit')
        if order_qty_unit is not None and 'LINE-QUANT' in line_item:
            order_qty_unit.text = line_item['LINE-QUANT']
        
        # Map LINE-PRICE to OrderLine/CostPrice
        cost_price_elem = new_line.find('CostPrice')
        if cost_price_elem is not None and 'LINE-PRICE' in line_item:
            cost_price_elem.text = line_item['LINE-PRICE']
        
        # Map LINE-TOTAL-AMOUNT to OrderLine/LineAmount
        line_amount_elem = new_line.find('LineAmount')
        if line_amount_elem is not None and 'LINE-TOTAL-AMOUNT' in line_item:
            line_amount_elem.text = line_item['LINE-TOTAL-AMOUNT']
        
        return new_line
    
    def _update_or_create_element(self, parent, tag_name: str, value: str):
        """
        Update an existing element or create a new one if it doesn't exist.
        
        Args:
            parent: Parent XML element
            tag_name: Name of the child element
            value: Value to set
        """
        if value is None:
            return
            
        elem = parent.find(tag_name)
        if elem is not None:
            elem.text = value
            print(f"Updated {tag_name}: {value}")
        else:
            # Create new element
            new_elem = ET.SubElement(parent, tag_name)
            new_elem.text = value
            print(f"Created {tag_name}: {value}")
    
    def map_line_items(self) -> bool:
        """
        Map line item data from CSV to XML structure.
        Creates multiple OrderLine elements based on CSV line items.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.line_items:
                print("No line items to process")
                return True
            
            # Find the Document element and existing OrderLine
            document = self.root.find('.//Document', self.namespaces)
            if document is None:
                print("Document element not found")
                return False
            
            # Find the base OrderLine to use as template
            base_order_line = document.find('OrderLine')
            if base_order_line is None:
                print("Base OrderLine not found")
                return False
            
            # Remove existing OrderLine first
            document.remove(base_order_line)
            
            # Create new OrderLine elements for each CSV line item
            for i, line_item in enumerate(self.line_items):
                # Create a copy of the base OrderLine
                new_order_line = self._create_order_line_from_template(base_order_line, line_item)
                
                # Insert before DocTrailer
                doc_trailer = document.find('DocTrailer')
                if doc_trailer is not None:
                    document.insert(list(document).index(doc_trailer), new_order_line)
                else:
                    document.append(new_order_line)
                
                print(f"Created OrderLine {i+1}: {line_item.get('LINE-CODE', 'Unknown')}")
            
            # Update DocTrailer/TotalLines
            doc_trailer = document.find('DocTrailer')
            if doc_trailer is not None:
                total_lines_elem = doc_trailer.find('TotalLines')
                if total_lines_elem is not None:
                    total_lines_elem.text = str(len(self.line_items))
                    print(f"Updated TotalLines: {len(self.line_items)}")
            
            return True
            
        except Exception as e:
            print(f"Error mapping line items: {e}")
            return False
    
    def generate_output_xml(self, output_dir: str = None) -> str:
        """
        Generate the output XML file with the correct naming convention.
        
        Args:
            output_dir: Directory to save the output file (default: outputs subdirectory)
            
        Returns:
            str: Path to the generated XML file
        """
        try:
            # Get CUST-ORDER value for filename
            cust_order = self.header_data.get('CUST-ORDER', 'UNKNOWN')
            filename = f"WAITROSE_{cust_order}.XML"
            
            if output_dir is None:
                # Create outputs directory in the project root, not relative to base XML location
                current_dir = os.path.dirname(os.path.abspath(__file__))
                output_dir = os.path.join(current_dir, 'outputs')
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, filename)
            
            # Write the modified XML
            self.tree.write(output_path, encoding='utf-8', xml_declaration=True)
            
            print(f"Generated output XML: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating output XML: {e}")
            return ""
    
    def process(self, csv_path: str, output_dir: str = None) -> bool:
        """
        Main processing method to convert CSV to EDI XML.
        
        Args:
            csv_path: Path to the input CSV file
            output_dir: Directory to save the output file
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("Starting CSV to EDI mapping process...")
        
        # Load base XML template
        if not self.load_base_xml():
            return False
        
        # Parse CSV data
        if not self.parse_csv(csv_path):
            return False
        
        print(f"Header data extracted: {len(self.header_data)} fields")
        print(f"Line items extracted: {len(self.line_items)} items")
        
        # Map header data
        if not self.map_header_data():
            return False
        
        # Map line items
        if not self.map_line_items():
            return False
        
        # Generate output
        output_path = self.generate_output_xml(output_dir)
        if output_path:
            print("CSV to EDI mapping completed successfully!")
            return True
        else:
            return False


def main():
    """Main entry point for the script."""
    # Use default files from inputs folder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, "inputs", "order.csv")
    base_xml_file = os.path.join(current_dir, "inputs", "baseEDI.XML")
    
    # Allow command line override
    if len(sys.argv) == 3:
        csv_file = sys.argv[1]
        base_xml_file = sys.argv[2]
    elif len(sys.argv) != 1:
        print("Usage: python csv_to_edi_mapper.py [csv_file] [base_xml_file]")
        print("       python csv_to_edi_mapper.py  (uses order.csv and baseEDI.XML)")
        sys.exit(1)
    
    # Validate input files
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)
    
    if not os.path.exists(base_xml_file):
        print(f"Error: Base XML file not found: {base_xml_file}")
        sys.exit(1)
    
    print(f"Processing: {os.path.basename(csv_file)} -> {os.path.basename(base_xml_file)}")
    
    # Create mapper and process
    mapper = CSVToEDIMapper(base_xml_file)
    success = mapper.process(csv_file)
    
    if not success:
        print("Failed to process CSV to EDI mapping")
        sys.exit(1)


if __name__ == "__main__":
    main()