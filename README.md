# Vendor Management System with Performance Metrics

## Core Features

- **Vendor Profile Management**
- **Purchase Order Tracking**
- **Vendor Performance Evaluation**

  ## Various Data Models
### 1. Vendor Model
This model stores essential information about each vendor and their performance metrics.

### 2. Purchase Order (PO) Model
This model captures the details of each purchase order and is used to calculate various
performance metrics.

### 3. Historical Performance Model
This model optionally stores historical data on vendor performance, enabling trend analysis.

## API Endpoints

Vendor Profile Management:

● POST /api/vendors/: This endpoint will create a new vendor.

● GET /api/vendors/: Endpoint used to list all vendors.

● GET /api/vendors/{vendor_id}/: This endpoint will retrieve a specific vendor's details.

● PUT /api/vendors/{vendor_id}/: Update a vendor's details.

● DELETE /api/vendors/{vendor_id}/: Delete a vendor.


Purchase Order Tracking:

● POST /api/purchase_orders/: Create a purchase order with specific vendor.

● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.

● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.

● PUT /api/purchase_orders/{po_id}/: Update a purchase order.

● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.


Vendor Performance Evaluation:

● GET /api/vendors/{vendor_id}/performance: Retrieves the calculated performance metrics for a specific vendor.


Update Acknowledgment Endpoint:

● POST /api/purchase_orders/{po_id}/acknowledge


## Set-up process

1- Install all the dependencies using the requirements.txt file and open the project directory in the terminal.

2- To recover database items use the command in the terminal "python manage.py makemigrations" and after that run the command "python manage.py migrate".

3- Now run the server using the command "python manage.py runserver".

4 - After that, the server can serve various endpoint requests, you can check using various tools like Postman (Use a specific URL with localhost).

## To run Test Suite

1- Just install dependencies and recover database items(like in above set-up process step-2).

2- To initiate the test use the command "python manage.py test" in the terminal.

If the terminal shows "Ok" then all the endpoint tests are successful.



**Thank you!**
