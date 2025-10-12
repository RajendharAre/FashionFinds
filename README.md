# 👗 FashionFinds - Your Ultimate Fashion E-Commerce Platform

<div align="center">

![Fashion Finds](https://img.shields.io/badge/FashionFinds-E--Commerce-c4877a?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-green?style=for-the-badge&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A modern, feature-rich e-commerce platform for fashion enthusiasts**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Technologies](#-technologies-used) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [User Roles](#-user-roles)
- [Database Schema](#-database-schema)
- [API Endpoints](#-api-endpoints)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🌟 Overview

**FashionFinds** is a complete e-commerce web application designed specifically for the fashion industry. Built with Flask and modern web technologies, it provides a seamless shopping experience for customers while offering powerful management tools for administrators and delivery personnel.

Whether you're a customer looking for the latest fashion trends, an admin managing inventory, or a delivery agent tracking orders, FashionFinds has everything you need!

### 🎯 Why FashionFinds?

- **User-Friendly Interface**: Clean, modern design that's easy to navigate
- **Secure Authentication**: Email-based login with password reset functionality
- **Role-Based Access**: Different interfaces for customers, admins, and delivery agents
- **Smart Shopping**: Cart, wishlist, and personalized product recommendations
- **Advanced Search**: Filter products by category, brand, color, and price range
- **Order Management**: Complete order tracking from placement to delivery

---

## ✨ Key Features

### 🛍️ For Customers

- **User Registration & Authentication**
  - Secure email-based registration
  - Password reset via email
  - Profile management with address details

- **Product Discovery**
  - Browse products by categories (Men, Women, Kids, Accessories)
  - Filter by brand, price, color, and more
  - View detailed product information with images
  - See suggested similar products

- **Shopping Experience**
  - Add products to cart with quantity selection
  - Save favorites to wishlist
  - Move items between cart and wishlist
  - Real-time cart total calculation

- **Order Management**
  - Easy checkout process
  - View order history
  - Track order status
  - Cancel orders when needed

### 👨‍💼 For Administrators

- **Dashboard Access**
  - View total users and pending approvals
  - Monitor system statistics
  
- **Product Management**
  - Add new products with images and descriptions
  - Manage product inventory and pricing
  - Set discounts and sales
  - Organize products by brands and categories

- **User Management**
  - Approve delivery agent registrations
  - Manage user roles and permissions

### 🚚 For Delivery Agents

- **Delivery Dashboard**
  - View assigned deliveries
  - Update delivery status
  - Manage delivery routes
  - Approval system for new agents

---

## 🛠️ Technologies Used

### Backend
- **Flask** - Lightweight and powerful Python web framework
- **Flask-SQLAlchemy** - SQL toolkit and ORM for database management
- **Flask-Login** - User session management
- **Flask-Mail** - Email functionality for password resets

### Database
- **SQLite** - Reliable embedded database (easily upgradable to PostgreSQL/MySQL)

### Frontend
- **HTML5 & CSS3** - Modern, responsive web design
- **Bootstrap** - UI components and responsive grid system
- **JavaScript** - Interactive user experience
- **Font Awesome** - Beautiful icons

### Security
- **itsdangerous** - Secure token generation for password resets
- Session-based authentication
- CSRF protection

---

## 📁 Project Structure

```
FashionFinds/
│
├── app/
│   ├── __init__.py          # Flask app initialization & configuration
│   ├── models.py            # Database models (User, Product, Order, etc.)
│   ├── auth.py              # Authentication routes (login, register, password reset)
│   ├── admin.py             # Admin routes (dashboard, product management)
│   ├── views.py             # Main routes (homepage, cart, wishlist, checkout)
│   │
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template with navigation
│   │   ├── home.html        # Homepage with product listings
│   │   ├── login.html       # User login page
│   │   ├── registration.html # User registration
│   │   ├── cart.html        # Shopping cart
│   │   ├── wishlist.html    # User wishlist
│   │   ├── product_details.html  # Product detail page
│   │   └── ...              # Other templates
│   │
│   └── static/              # Static files (CSS, JS, images)
│       ├── css/
│       ├── js/
│       └── images/
│
├── instance/
│   └── users.db             # SQLite database file
│
├── migrations/              # Database migration files
│
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

---

## 🚀 Installation Guide

Follow these simple steps to get FashionFinds running on your local machine!

### Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/RajendharAre/FashionFinds.git
cd FashionFinds
```

### Step 2: Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install flask flask-sqlalchemy flask-login flask-mail itsdangerous
```

### Step 4: Configure Environment Variables

Create a `.env` file or update `app/__init__.py` with your settings:

```python
# Email Configuration (for password reset)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'  # Use App Password, not regular password
```

> **Note**: For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833)

### Step 5: Initialize the Database

```bash
python run.py
```

The database will be automatically created on first run!

---

## ⚙️ Configuration

### Database Configuration

By default, FashionFinds uses SQLite. To use a different database:

```python
# In app/__init__.py
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost/fashionfinds"
# or
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://user:password@localhost/fashionfinds"
```

### Secret Key

**Important**: Change the secret key in production!

```python
app.secret_key = "your-secure-random-secret-key"
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

---

## 💻 Usage

### Running the Application

1. **Activate your virtual environment** (if not already activated)

2. **Start the Flask development server:**
   ```bash
   python run.py
   ```

3. **Open your browser and visit:**
   ```
   http://localhost:5000
   ```

### Creating Your First Admin Account

1. Register a new account through the website
2. Manually update the database to set the user as admin:
   ```python
   from app import create_app, db
   from app.models import User
   
   app = create_app()
   with app.app_context():
       user = User.query.filter_by(email='admin@example.com').first()
       user.role = 'admin'
       user.approved = True
       db.session.commit()
   ```

### Adding Products

1. Login as an admin
2. Navigate to "Add Products" from your account page
3. Fill in product details and submit

---

## 👥 User Roles

### 🛍️ Customer (Default)
- Browse and search products
- Manage cart and wishlist
- Place and track orders
- Update profile and password

### 👨‍💼 Admin
- All customer features
- Access to admin dashboard
- Add and manage products
- Approve delivery agents
- View system statistics

### 🚚 Delivery Agent
- View assigned deliveries
- Update delivery status
- Access to delivery dashboard
- Requires admin approval

---

## 🗄️ Database Schema

### Core Models

**User**
- Personal information (name, email, phone)
- Authentication (password, reset tokens)
- Address details
- Role and approval status

**Product**
- Product details (name, description, images)
- Pricing (current price, previous price, discount)
- Inventory (stock count, sizes)
- Categorization (category, brand, color)
- Ratings and reviews

**Order**
- Customer information
- Order items and quantities
- Pricing and totals
- Status tracking
- Delivery information

**Cart & Wishlist**
- User associations
- Product references
- Quantities

---

## 🔌 API Endpoints

### Authentication
- `GET/POST /auth/login` - User login
- `GET/POST /auth/register` - User registration
- `GET/POST /auth/forgot-password` - Request password reset
- `GET/POST /auth/reset-password/<token>` - Reset password with token
- `GET /auth/logout` - User logout

### Products
- `GET /` - Homepage with featured products
- `GET /product/<id>` - Product details
- `GET /category/<category>` - Products by category
- `GET /brand/<brand_id>` - Products by brand
- `GET /search` - Search with filters

### Shopping
- `GET /cart` - View shopping cart
- `POST /add_to_cart/<product_id>` - Add product to cart
- `POST /remove_from_cart/<product_id>` - Remove from cart
- `POST /update_cart_quantity/<product_id>` - Update quantity
- `GET /wishlist` - View wishlist
- `POST /add_to_wishlist/<product_id>` - Add to wishlist

### Orders
- `GET /checkout` - Checkout page
- `POST /place_order` - Place new order
- `GET /my_orders` - View order history
- `POST /cancel_order/<order_id>` - Cancel order

### Admin
- `GET /admin/admin_dashboard` - Admin dashboard
- `GET /admin/add_products` - Add products page
- `GET /admin/role_approval` - Approve delivery agents
- `POST /admin/approve_user/<user_id>` - Approve user

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)
*Browse through our extensive collection of fashion products with category filters*

### Product Details
![Product Details](screenshots/admin_page.png)
*Detailed product information with size selection and cart options*

### Admin Dashboard
![Admin Dashboard](screenshots/admin.png)
*Complete admin panel for managing products, users, and orders*

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add comments to complex code sections
- Update documentation for new features
- Test your changes thoroughly

---

## 🐛 Known Issues & Future Enhancements

### Current Limitations
- Payment gateway integration pending
- Product reviews and ratings not fully implemented
- Email notifications for order status updates

### Planned Features
- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Product reviews and ratings
- [ ] Email notifications for orders
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Social media integration

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

**Rajendhar Are**

- GitHub: [@RajendharAre](https://github.com/RajendharAre)
- Email: arerajendhar2903@gmail.com
- Project Link: [https://github.com/RajendharAre/FashionFinds](https://github.com/RajendharAre/FashionFinds)

---

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap for the UI framework
- Font Awesome for icons
- All contributors and supporters

---

<div align="center">

**Made with ❤️ by Rajendhar Are**

⭐ Star this repo if you find it helpful!

</div>




