**Streamoid Product Catalog – Django Backend
**
This project is a simple Django REST API that lets online sellers upload their product catalog in CSV format, validate it, and store valid products in the database. It ensures all required fields are present and checks that price ≤ MRP and quantity ≥ 0. Invalid rows are returned in the API response for review. The system also allows searching and filtering of products by brand, color, or price range.

To run the project, first clone the repository and navigate into the folder. Create a virtual environment using python3 -m venv venv and activate it. Install the required dependencies using pip install django djangorestframework pandas. Then, run python manage.py makemigrations and python manage.py migrate to create the database. Finally, start the server with python manage.py runserver and visit http://127.0.0.1:8000 to access the API.

The main endpoints are simple and RESTful:

POST /api/upload/ — Upload a CSV file using multipart form-data (file=@product_catalog.csv). Valid rows are saved in the database, and invalid ones are returned for correction.

GET /api/products/search/ — Filter products using query parameters such as brand, color, minPrice, and maxPrice.
Example: /api/products/search/?brand=StreamThreads&minPrice=500&maxPrice=1500

A lightweight backend built with Django REST Framework and Pandas to make product validation and management quick and reliable before sellers upload their listings to marketplaces.
