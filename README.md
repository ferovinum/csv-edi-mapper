# CSV to EDI Mapper

Converts CSV order data to TrueCommerce XML format for Waitrose orders.

## How to Run

```bash
# Process inputs/order.csv with inputs/baseEDI.XML
python process_order.py

# Or run the main script directly  
python csv_to_edi_mapper.py
```

## Required CSV Format

The input file `inputs/order.csv` must contain:

```csv
###ORD-HEADER,,,,,,,,,,,,,,
CUST-ORDER,CUST-ADDR-CODE,CUST-ADDR-NAME,CUST-ADDR-ADDRESS1,CUST-ADDR-ADDRESS2,CUST-ADDR-ADDRESS3,DELIVERY-DUE-DATE,DELIVERY-TO-CODE,DELIVERY-TO-NAME,DELIVERY-TO-ADDRESS1,INVOICE-TO-CODE,INVOICE-TO-NAME,INVOICE-TO-ADDRESS1,TOTAL-ORDER-UNITS,TOTAL-ORDER-VALUE
CUST-001,CA0,Waitrose Head Office,Address Line 1,Address Line 2,Address Line 3,2018-04-10,DC01,Depot Name,Depot Address,INV01,Invoice Name,Invoice Address,100,5000
###ORD-HEADER-END,,,,,,,,,,,,,,
###ORD-LINES,,,,,,,,,,,,,,
LINE-NO,LINE-CODE,LINE-DESC,LINE-QUANT,LINE-PRICE,LINE-TOTAL-AMOUNT
1,PROD001,Product Description,10,25.50,255.00
2,PROD002,Another Product,5,30.00,150.00
###ORD-LINES-END,,,,,,,,,,,,,,
```

## Output Location

Generated XML files are saved as: `outputs/WAITROSE_{CUST-ORDER}.XML`

## Test the Script

```bash
python test_mapper.py
```