# PetalCart 🌸

An e-commerce platform for buying and selling fresh flowers online where users can browse flower catalogs, create shops, manage inventory, place orders, and make secure payments with real-time tracking. 💐✨

## ✨ Features

### 👤 User Management
- 📝 User registration and authentication
- 🎯 User profiles with order history and activity
- 🔐 Login/Logout functionality
- 🏪 Shop owner and seller roles

### 🌸 Flower Catalog
- ➕ Add and manage flower products with images
- 🔍 Browse and search flowers by name, shop, or category
- 💰 View pricing and availability
- ⭐ Rating and review system
- 🏪 Shop-specific product listings
- 📦 Track inventory and stock levels

### 🛒 Shopping Cart & Orders
- 🛍️ Add flowers to shopping cart
- 💳 Secure checkout process
- 📋 Order history and tracking
- 🚚 Order status management
- 📦 Multiple items per order
- 🎯 Order confirmation and details

### 💰 Payment System
- 💳 Razorpay payment integration
- 🔒 Secure payment processing
- 📊 Payment verification and tracking
- 🧾 Invoice generation
- ✅ Multiple payment methods support

### 🏪 Shop Management
- 🏢 Shop registration and profiles
- 📝 Shop management dashboard
- 👥 View shop customers
- 📊 Monitor sales and revenue
- 🎨 Shop branding and description

### 💬 Reviews & Ratings
- ⭐ Rate flowers and sellers
- 💭 Leave detailed reviews and comments
- 📍 Display star ratings
- 👍 Helpful review indicators
- 🗣️ Customer feedback system

## 🛠️ Technologies Used

- **Backend:** Django 5.2.8 🐍
- **Database:** SQLite / PostgreSQL 💾
- **Frontend:** HTML, CSS, JavaScript 🎨
- **Authentication:** Django's built-in authentication system 🔒
- **Payments:** Razorpay Integration 💳
- **Media Management:** Django media files handling 📸

## 📦 Installation

### ✅ Prerequisites
- Python 3.8 or higher 🐍
- pip (Python package manager) 📦
- Razorpay account keys 💳

### 🚀 Setup Steps

1. **📥 Clone the repository**
   ```bash
   cd petalcart
   ```

2. **🔧 Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **⚡ Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **📚 Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
petalcart/
├── accounts/               # User authentication and profiles
│   ├── migrations/        # Database migrations
│   ├── admin.py          # Admin configuration
│   ├── models.py         # User models
│   ├── views.py          # Authentication views
│   ├── forms.py          # Registration forms
│   └── urls.py           # Auth URL routing
├── shop/                 # Shop management
│   ├── migrations/
│   ├── admin.py
│   ├── models.py         # Shop and product models
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── petalcart/            # Cart and orders
│   ├── migrations/
│   ├── admin.py
│   ├── models.py         # Cart, Order, Item models
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── adaptlearn/           # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main URL routing
│   ├── wsgi.py           # WSGI configuration
│   └── asgi.py           # ASGI configuration
├── templates/            # HTML templates
│   ├── base.html
│   ├── navbar.html
│   ├── payment.html
│   ├── form.html
│   ├── shop/
│   ├── petalcart/
│   └── accounts/
├── static/              # Static files
│   ├── css/
│   ├── js/
│   └── pics/
├── media/               # User uploaded files
│   └── pics/
├── requirements.txt     # Python dependencies
├── db.sqlite3          # SQLite database
└── manage.py           # Django management script
```

## 📖 Usage

### 👨‍🎓 For Buyers

1. **🔐 Register/Login**
   - Create an account or login with existing credentials
   - Navigate to `/register/` or `/login/`

2. **🔍 Browse Flowers**
   - View all available flower products on the home page
   - Use the search bar to filter by name, shop, or category
   - Check prices and ratings

3. **🛒 Add to Cart**
   - Click "Add to Cart" on flower listings
   - View cart with selected items
   - Update quantities as needed

4. **💳 Checkout & Payment**
   - Proceed to checkout
   - Enter delivery details
   - Complete payment via Razorpay
   - Receive order confirmation

5. **📦 Track Orders**
   - View order history in your profile
   - Monitor order status
   - Track delivery updates

6. **⭐ Leave Reviews**
   - Rate flowers and shops
   - Leave detailed reviews and comments
   - Help other buyers with feedback

### 🏪 For Shop Owners

1. **🏢 Register Shop**
   - Create a shop account
   - Set up shop profile and branding
   - Add shop description and contact info

2. **🌸 Manage Flowers**
   - Add new flower products with images
   - Set pricing and availability
   - Update stock levels
   - Edit product details

3. **📊 Monitor Sales**
   - View orders from your shop
   - Track revenue and sales metrics
   - Manage customer orders

4. **👥 Customer Management**
   - View customer feedback and reviews
   - Respond to customer inquiries
   - Build customer relationships

## 🗄️ Database Models

### 👤 User
- Username, email, password
- First name, last name
- Profile picture
- User type (buyer/shop owner)
- Registration date

### 🏪 Shop
- Shop owner (Foreign Key to User)
- Shop name
- Description
- Contact information
- Shop image/logo
- Created/Updated timestamps

### 🌸 Flower (Product)
- Shop (Foreign Key)
- Flower name
- Description
- Price
- Stock quantity
- Product images
- Created/Updated timestamps

### 🛒 Cart
- User (Foreign Key)
- Items (Through CartItem)
- Total quantity
- Total price

### 📦 Order
- User (Foreign Key)
- Order items (Through OrderItem)
- Status (Pending, Processing, Shipped, Delivered)
- Total price
- Delivery address
- Payment status
- Created/Updated timestamps

### 💬 Comment/Review
- User (Foreign Key)
- Flower (Foreign Key)
- Rating (1-5 stars)
- Text content
- Created/Updated timestamps

## 🛣️ URL Routes

- 🏠 `/` - Home page with flower listings
- 🛍️ `/shop/` - All shops browsing
- 🌸 `/shop/<id>/` - Individual shop view
- 🌸 `/flower/<id>/` - Flower detail page
- 🛒 `/cart/` - Shopping cart
- 💳 `/payment/<order_id>/` - Payment page
- 📦 `/orders/` - User orders history
- 👤 `/profile/` - User profile
- 🏪 `/my-shop/` - Shop owner dashboard
- ➕ `/add-flower/` - Add new flower (shop owner)
- ✏️ `/edit-flower/<id>/` - Edit flower
- 🗑️ `/delete-flower/<id>/` - Delete flower
- 🔐 `/login/` - User login
- 👋 `/logout/` - User logout
- 📝 `/register/` - User registration
- 💬 `/comment/<flower_id>/` - Add review/comment

## 🔒 Security Notes

⚠️ **Important:** This project contains development settings that should be changed for production:

- 🔑 Change the `SECRET_KEY` in `settings.py`
- 🐛 Set `DEBUG = False` in production
- 🌐 Configure `ALLOWED_HOSTS` appropriately
- 💾 Use a production-grade database (PostgreSQL recommended)
- 📂 Set up proper static file serving
- 🔒 Enable HTTPS
- 🛡️ Implement additional security measures (CSRF, XSS protection, etc.)
- 💳 Use real Razorpay production keys
- 🔐 Secure payment data handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 🎉

## 📄 License

This project is open source and available for educational purposes. 📖

## 📬 Contact

For questions or support, please open an issue in the repository. 💌

---

**Happy Shopping! 🌸💐🛍️**
