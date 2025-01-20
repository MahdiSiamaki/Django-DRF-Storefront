# django-storefront

## Project Overview
Django Storefront is a sample e-commerce application built with Django and Django REST Framework. It provides a backend API for managing products, collections, customers, orders, and more. The project is designed to demonstrate best practices for building a RESTful API with Django.

## Features
- Product management (CRUD operations)
- Collection management (CRUD operations)
- Customer management (CRUD operations)
- Order management (CRUD operations)
- Cart management
- Review management
- JWT authentication with Djoser
- Filtering, searching, and ordering of products
- Pagination

## Installation
Follow these steps to set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/MahdiSiamaki/Django-DRF-Storefront.git
   cd Django-DRF-Storefront
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database settings in `storefront/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'storefront2',
           'HOST': 'localhost',
           'USER': 'root',
           'PASSWORD': 'your_password'
       }
   }
   ```

5. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
Once the development server is running, you can use the API endpoints to interact with the application. Here are some of the available endpoints:

- `GET /store/products/` - List all products
- `POST /store/products/` - Create a new product
- `GET /store/products/{id}/` - Retrieve a specific product
- `PUT /store/products/{id}/` - Update a specific product
- `DELETE /store/products/{id}/` - Delete a specific product

- `GET /store/collections/` - List all collections
- `POST /store/collections/` - Create a new collection
- `GET /store/collections/{id}/` - Retrieve a specific collection
- `PUT /store/collections/{id}/` - Update a specific collection
- `DELETE /store/collections/{id}/` - Delete a specific collection

- `GET /store/customers/` - List all customers
- `POST /store/customers/` - Create a new customer
- `GET /store/customers/{id}/` - Retrieve a specific customer
- `PUT /store/customers/{id}/` - Update a specific customer
- `DELETE /store/customers/{id}/` - Delete a specific customer

- `GET /store/orders/` - List all orders
- `POST /store/orders/` - Create a new order
- `GET /store/orders/{id}/` - Retrieve a specific order
- `PUT /store/orders/{id}/` - Update a specific order
- `DELETE /store/orders/{id}/` - Delete a specific order

- `GET /store/carts/` - List all carts
- `POST /store/carts/` - Create a new cart
- `GET /store/carts/{id}/` - Retrieve a specific cart
- `PUT /store/carts/{id}/` - Update a specific cart
- `DELETE /store/carts/{id}/` - Delete a specific cart

- `GET /store/reviews/` - List all reviews
- `POST /store/reviews/` - Create a new review
- `GET /store/reviews/{id}/` - Retrieve a specific review
- `PUT /store/reviews/{id}/` - Update a specific review
- `DELETE /store/reviews/{id}/` - Delete a specific review

## Contributing
Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your forked repository.
5. Create a pull request to the main repository.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact
If you have any questions or suggestions, feel free to contact me at [your_email@example.com].
