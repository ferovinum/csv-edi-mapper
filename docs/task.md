Task go from the CSV file to the Order XML.

The CSV file defines the order and we want to map it as an XML file by editing and appending to the base file.

Base XML file is provided to you as baseEDI.XML
The input file to use will be called order.csv

The CSV file is split up into two sections, heading and line items. There can only be one heading and multiple line items.

Column A will store markers for where header and lines start and end. 
###ORD-HEADER shows where the header starts 
###ORD-HEADER-END shows where the header ends 
###ORD-LINES shows where the line items start 
###ORD-LINES-END shows where the line items end

Mapping. Apply the following logic for the columns and values defined. 

First, the header.

CUST-ORDER. The value of this should replace the value of OrderHeader/CustOrder in the XML.
CUST-ADDR-CODE. Map to Document/DocHeader/CustAddr/Code
CUST-ADDR-NAME. Map to Document/DocHeader/CustAddr/Name
CUST-ADDR-ADDRESS1, CUST-ADDR-ADDRESS2, and CUST-ADDR-ADDRESS1. Map to Document/DocHeader/CustAddr/Address1, Document/DocHeader/CustAddr/Address2, and Document/DocHeader/CustAddr/Address3 appropriately. If those tags don't exist, create them.
DELIVERY-DUE-DATE. Map to Document/DocHeader/OrderHeader/Delivery/ReqDel/Date.
DELIVERY-TO-CODE. Map to Document/DocHeader/OrderHeader/Delivery/DeliverTo/Code.
DELIVERY-TO-NAME. Map to Document/DocHeader/OrderHeader/Delivery/DeliverTo/Name.
DELIVERY-TO-ADDRESS1. Map to Document/DocHeader/OrderHeader/Delivery/DeliverTo/Address1.
INVOICE-TO-CODE. Map to Document/DocHeader/OrderHeader/Locations/InvoiceTo/Code
INVOICE-TO-NAME. Map to Document/DocHeader/OrderHeader/Locations/InvoiceTo/NAME
INVOICE-TO-ADDRESS1. Map to Document/DocHeader/OrderHeader/Locations/InvoiceTo/Address1
TOTAL-ORDER-UNITS. Map to Document/DocHeader/OrderHeader/TotalOrderUnits
TOTAL-ORDER-VALUE. Map to Document/DocHeader/OrderHeader/TotalOrderVal

Second, the line items.
Underneath ###ORD-LINES there will be many lines which should be mapped to many OrderLine items in the XML.
The base XML has one order line. I want create additional OrderLine items for each line item.

For mapping use this,
LINE-NO. Map to OrderLine/LineNo (appropriate to the line item)
LINE-CODE. Map to OrderLine/Item/CustItem/Code
LINE-DESC. Map to OrderLine/Item/Desc1
LINE-QUANT. Map to OrderLine/OrderQty/Unit
LINE-PRICE. Map to OrderLine/OrderQty/CostPrice
LINE-TOTAL-AMOUNT. Map to Map to OrderLine/OrderQty/LineAmount.

Additionally, 
Map Document/DocTrailer/TotalLines value to the total amount of ord-lines in the CSV.


The rest of the line can be copied from the base order line. 

At the end, produce a file with the name in the following format "WAITROSE_{CUST-ORDER}.XML". Put the file in the new directory called outputs. If you encounter a file with that name, replace it. 

This time produce very concise documentation, only focusing on how to run the script, the required CSV and the location of the output file.