# CSV to EDI Mapping Configuration

This file defines the comprehensive mapping rules between CSV fields and XML elements for the Waitrose order processing system.

## Header Section Mappings

The CSV header section contains order-level information mapped to various XML locations:

### Customer Information

- `CUST-ORDER` → `OrderHeader/CustOrder`
- `CUST-ADDR-CODE` → `Document/DocHeader/CustAddr/Code`
- `CUST-ADDR-NAME` → `Document/DocHeader/CustAddr/Name`
- `CUST-ADDR-ADDRESS1` → `Document/DocHeader/CustAddr/Address1`
- `CUST-ADDR-ADDRESS2` → `Document/DocHeader/CustAddr/Address2` (created if missing)
- `CUST-ADDR-ADDRESS3` → `Document/DocHeader/CustAddr/Address3` (created if missing)

### Delivery Information

- `DELIVERY-DUE-DATE` → `OrderHeader/Delivery/ReqDel/Date`
- `DELIVERY-TO-CODE` → `OrderHeader/Delivery/DeliverTo/Code`
- `DELIVERY-TO-NAME` → `OrderHeader/Delivery/DeliverTo/Name`
- `DELIVERY-TO-ADDRESS1` → `OrderHeader/Delivery/DeliverTo/Address1`

### Invoice Information

- `INVOICE-TO-CODE` → `OrderHeader/Locations/InvoiceTo/Code`
- `INVOICE-TO-NAME` → `OrderHeader/Locations/InvoiceTo/Name`
- `INVOICE-TO-ADDRESS1` → `OrderHeader/Locations/InvoiceTo/Address1`

### Order Totals

- `TOTAL-ORDER-UNITS` → `OrderHeader/TotalOrderUnits`
- `TOTAL-ORDER-VALUE` → `OrderHeader/TotalOrderVal`

## Line Item Section Mappings

Line items contain product-specific information:

- `LINE-NO` → Line item number/sequence
- `LINE-CODE` → Product/item code
- `LINE-DESC` → Product description
- `LINE-QUANT` → Quantity ordered
- `LINE-PRICE` → Unit price
- `LINE-TOTAL-AMOUNT` → Line total amount

## File Structure Requirements

### Input Files

- **CSV Input**: `order.csv` - Contains order data in structured format
- **XML Template**: `baseEDI.XML` - TrueCommerce XML template

### Output Files

- **Generated XML**: `outputs/WAITROSE_{CUST-ORDER}.XML`
- **Directory**: Files are saved in the `outputs/` subdirectory

### CSV Section Markers

Required section delimiters:

- `###ORD-HEADER` - Start of header section
- `###ORD-HEADER-END` - End of header section  
- `###ORD-LINES` - Start of line items section
- `###ORD-LINES-END` - End of line items section

### Header Section Format

- **Row 1**: Field names (column headers)
- **Row 2**: Field values (actual data)

### Line Items Section Format

- **Row 1**: Column headers for line item fields
- **Subsequent rows**: Line item data (one product per row)

## XML Namespace Handling

The framework properly handles TrueCommerce XML namespaces:

- `tc`: `http://www.truecommerce.com/docs/order`

## Element Creation

The framework automatically creates missing XML elements when:

- Address2 and Address3 elements don't exist in CustAddr section
- Other elements are missing but required by the mapping

## Data Validation

- Empty CSV fields are ignored (no XML updates made)
- XML entities are properly encoded (e.g., `&` becomes `&amp;`)
- Date formats are preserved as provided in CSV