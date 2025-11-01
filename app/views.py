from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from app.models import Product, Brand, Cart, Wishlist, User, Order, OrderItem, ProductSize, db
from sqlalchemy import func, or_, desc
import random

views = Blueprint('views', __name__)

# ============= HOMEPAGE =============
@views.route('/')
def homepage():
    """Enhanced homepage with featured content"""
    brands_list = Brand.query.all()
    
    # Get trending products (most ordered)
    trending_products = db.session.query(Product)\
        .join(OrderItem)\
        .group_by(Product.id)\
        .order_by(func.count(OrderItem.id).desc())\
        .limit(20).all()
    
    # Fallback to all products if no orders yet
    if not trending_products:
        trending_products = Product.query.order_by(func.random()).limit(20).all()
    
    return render_template('home.html', 
                         brands=brands_list, 
                         products=trending_products)


# ============= BRAND PAGES =============
@views.route('/brand/<int:brand_id>')
def brand_info(brand_id):
    """Brand detail page with all products"""
    brand_data = Brand.query.get_or_404(brand_id)
    brand_items = Product.query.filter_by(brand_id=brand_id)\
        .order_by(Product.rating.desc()).all()
    
    return render_template('brand_details.html', 
                         brand=brand_data, 
                         products=brand_items)


# ============= CATEGORY PAGES =============
@views.route('/category/<string:category_name>')
def products_by_category(category_name):
    """Category page with sorting and filtering"""
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort', 'popularity')
    per_page = 24
    
    # Base query
    query = Product.query.filter_by(category=category_name)
    
    # Apply sorting
    if sort_by == 'price_low':
        query = query.order_by(Product.current_price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.current_price.desc())
    elif sort_by == 'rating':
        query = query.order_by(Product.rating.desc())
    elif sort_by == 'newest':
        query = query.order_by(Product.id.desc())
    else:  # popularity
        query = query.order_by(Product.count.desc())
    
    # Paginate
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('category.html', 
                         products=paginated.items,
                         pagination=paginated,
                         category=category_name,
                         sort_by=sort_by)


# ============= PRODUCT DETAIL =============
@views.route('/product/<int:product_id>')
def product_info(product_id):
    """Enhanced product detail page with recommendations"""
    product = Product.query.get_or_404(product_id)
    
    # Get product sizes
    sizes = ProductSize.query.filter_by(product_id=product.id).all()
    
    # Get similar products (same category and brand)
    similar_products = Product.query\
        .filter(Product.id != product.id)\
        .filter(Product.category == product.category)\
        .filter(Product.brand_id == product.brand_id)\
        .order_by(func.random())\
        .limit(4).all()
    
    # If not enough, add from same category
    if len(similar_products) < 4:
        additional = Product.query\
            .filter(Product.id != product.id)\
            .filter(Product.category == product.category)\
            .filter(Product.id.notin_([p.id for p in similar_products]))\
            .order_by(func.random())\
            .limit(4 - len(similar_products)).all()
        similar_products.extend(additional)
    
    # Check if user has this in wishlist
    in_wishlist = False
    if 'user_id' in session:
        in_wishlist = Wishlist.query.filter_by(
            user_id=session['user_id'], 
            product_id=product_id
        ).first() is not None
    
    return render_template('product_details.html', 
                         product=product, 
                         sizes=sizes, 
                         suggested_products=similar_products,
                         in_wishlist=in_wishlist)


# ============= SEARCH FUNCTIONALITY =============
@views.route('/search', methods=['GET'])
def search():
    """Enhanced search with multiple filters"""
    query = request.args.get('query', '').strip()
    category = request.args.get('category', '')
    brand = request.args.get('brand', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    color = request.args.get('color', '')
    sort_by = request.args.get('sort', 'relevance')
    page = request.args.get('page', 1, type=int)
    per_page = 24
    
    # Start with base query
    search_query = Product.query
    
    # Text search
    if query:
        search_query = search_query.filter(
            or_(
                Product.product_name.ilike(f'%{query}%'),
                Product.description.ilike(f'%{query}%')
            )
        )
    
    # Apply filters
    if category:
        search_query = search_query.filter(Product.category == category)
    
    if brand:
        search_query = search_query.join(Brand).filter(Brand.name == brand)
    
    if color:
        search_query = search_query.filter(Product.color.ilike(f'%{color}%'))
    
    if min_price is not None:
        search_query = search_query.filter(Product.current_price >= min_price)
    
    if max_price is not None:
        search_query = search_query.filter(Product.current_price <= max_price)
    
    # Apply sorting
    if sort_by == 'price_low':
        search_query = search_query.order_by(Product.current_price.asc())
    elif sort_by == 'price_high':
        search_query = search_query.order_by(Product.current_price.desc())
    elif sort_by == 'rating':
        search_query = search_query.order_by(Product.rating.desc())
    elif sort_by == 'newest':
        search_query = search_query.order_by(Product.id.desc())
    else:  # relevance
        if query:
            # Simple relevance: products with query in name first
            search_query = search_query.order_by(
                Product.product_name.ilike(f'%{query}%').desc(),
                Product.rating.desc()
            )
    
    # Paginate results
    paginated = search_query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Get filter options
    categories = db.session.query(Product.category).distinct().all()
    brands = Brand.query.all()
    colors = db.session.query(Product.color).filter(Product.color.isnot(None)).distinct().all()
    
    # Get price range
    price_range = db.session.query(
        func.min(Product.current_price),
        func.max(Product.current_price)
    ).first()
    
    return render_template(
        'search_results.html',
        products=paginated.items,
        pagination=paginated,
        query=query,
        filters={
            'category': category,
            'brand': brand,
            'color': color,
            'min_price': min_price,
            'max_price': max_price,
            'sort_by': sort_by
        },
        filter_options={
            'categories': [c[0] for c in categories],
            'brands': brands,
            'colors': [c[0] for c in colors if c[0]],
            'price_range': price_range
        },
        total_results=paginated.total
    )


# ============= CART FUNCTIONALITY =============
@views.route('/cart')
def show_cart():
    """Enhanced cart view with recommendations"""
    if 'user_id' not in session:
        flash('Please login to view your cart', 'warning')
        return render_template('cart.html', cart_items={}, 
                             total_mrp=0, discount_mrp=0, total_amount=0)
    
    user_id = session['user_id']
    
    # Get cart items with product details
    cart_data = db.session.query(Cart, Product)\
        .join(Product, Cart.product_id == Product.id)\
        .filter(Cart.user_id == user_id).all()
    
    # Calculate totals
    cart_items = {}
    total_mrp = 0
    total_discount = 0
    
    for cart, product in cart_data:
        item_mrp = cart.quantity * product.previous_price
        item_discount = cart.quantity * (product.previous_price - product.current_price)
        
        cart_items[product.id] = {
            'product_name': product.product_name,
            'image': product.product_picture,
            'price': product.current_price,
            'original_price': product.previous_price,
            'quantity': cart.quantity,
            'subtotal': cart.quantity * product.current_price
        }
        
        total_mrp += item_mrp
        total_discount += item_discount
    
    total_amount = int(total_mrp - total_discount)
    
    # Get recommended products
    if cart_items:
        # Get categories of items in cart
        cart_categories = db.session.query(Product.category)\
            .join(Cart).filter(Cart.user_id == user_id)\
            .distinct().all()
        
        categories = [c[0] for c in cart_categories]
        
        # Recommend products from same categories
        recommendations = Product.query\
            .filter(Product.category.in_(categories))\
            .filter(Product.id.notin_(cart_items.keys()))\
            .order_by(func.random())\
            .limit(4).all()
    else:
        recommendations = []
    
    return render_template('cart.html', 
                         cart_items=cart_items,
                         total_mrp=total_mrp,
                         discount_mrp=total_discount,
                         total_amount=total_amount,
                         recommendations=recommendations)


@views.route('/add_to_cart/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    """Add product to cart"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    product = Product.query.get_or_404(product_id)
    user_id = session['user_id']
    quantity = request.form.get('quantity', 1, type=int)
    
    # Check if already in cart
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(new_cart_item)
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'message': 'Added to cart'})
    
    flash('Product added to cart!', 'success')
    return redirect(url_for('views.show_cart'))


@views.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def cart_remove(product_id):
    """Remove product from cart"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Product removed from cart!', 'success')
    
    return redirect(url_for('views.show_cart'))


@views.route('/update_cart_quantity/<int:product_id>', methods=['POST'])
def update_cart_quantity(product_id):
    """Update cart item quantity"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    new_quantity = request.form.get('quantity', 1, type=int)
    
    if new_quantity < 1:
        return jsonify({'error': 'Invalid quantity'}), 400
    
    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
        
        # Recalculate totals
        cart_data = db.session.query(Cart, Product)\
            .join(Product).filter(Cart.user_id == user_id).all()
        
        total_mrp = sum(c.quantity * p.previous_price for c, p in cart_data)
        total_discount = sum(c.quantity * (p.previous_price - p.current_price) for c, p in cart_data)
        total_amount = int(total_mrp - total_discount)
        
        return jsonify({
            'success': True,
            'total_mrp': total_mrp,
            'discount_mrp': total_discount,
            'total_amount': total_amount
        })
    
    return jsonify({'error': 'Item not found'}), 404


# ============= WISHLIST FUNCTIONALITY =============
@views.route('/wishlist')
def show_wishlist():
    """Enhanced wishlist view"""
    if 'user_id' not in session:
        flash('Please login to view your wishlist', 'warning')
        return render_template('wishlist.html', wishlist_items=[])
    
    wishlist_data = db.session.query(Wishlist)\
        .filter(Wishlist.user_id == session['user_id']).all()
    
    return render_template('wishlist.html', wishlist_items=wishlist_data)


@views.route('/add_to_wishlist/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    """Add product to wishlist"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    user_id = session['user_id']
    
    # Check if already in wishlist
    existing_item = Wishlist.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first()
    
    if not existing_item:
        new_wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(new_wishlist_item)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'success': True, 'message': 'Added to wishlist'})
        
        flash('Added to wishlist!', 'success')
    else:
        if request.is_json:
            return jsonify({'info': 'Already in wishlist'})
        flash('Already in wishlist', 'info')
    
    return redirect(request.referrer or url_for('views.show_wishlist'))


@views.route('/remove_from_wishlist/<int:product_id>', methods=['POST'])
def remove_from_wishlist(product_id):
    """Remove product from wishlist"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    wishlist_item = Wishlist.query.filter_by(
        user_id=session['user_id'], 
        product_id=product_id
    ).first()
    
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Removed from wishlist!', 'success')
    
    return redirect(url_for('views.show_wishlist'))


@views.route('/move_to_cart/<int:product_id>', methods=['POST'])
def move_to_cart(product_id):
    """Move item from wishlist to cart"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    
    # Remove from wishlist
    wishlist_item = Wishlist.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first()
    
    if wishlist_item:
        # Add to cart
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
            db.session.add(new_cart_item)
        
        # Remove from wishlist
        db.session.delete(wishlist_item)
        db.session.commit()
        
        flash('Moved to cart!', 'success')
    
    return redirect(url_for('views.show_cart'))


# ============= CHECKOUT & ORDERS =============
@views.route('/checkout')
def checkout():
    """Checkout page"""
    if 'user_id' not in session:
        flash('Please login to checkout', 'warning')
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Get cart items
    cart_data = db.session.query(Cart, Product)\
        .join(Product).filter(Cart.user_id == user_id).all()
    
    if not cart_data:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('views.show_cart'))
    
    # Calculate totals
    subtotal = sum(c.quantity * p.current_price for c, p in cart_data)
    shipping = 0 if subtotal > 999 else 50
    tax = round(subtotal * 0.05, 2)
    total = subtotal + shipping + tax
    
    cart_items = [{
        'name': p.product_name,
        'price': p.current_price,
        'quantity': c.quantity,
        'product_id': p.id
    } for c, p in cart_data]
    
    return render_template('checkout.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         shipping=shipping,
                         tax=tax,
                         total=total,
                         current_user=user)


@views.route('/place_order', methods=['POST'])
def place_order():
    """Place an order"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = session['user_id']
    
    # Get form data
    data = request.form
    customer_name = f"{data.get('firstname')} {data.get('lastname')}"
    address_line_1 = data.get('address_line_1')
    city = data.get('city')
    state = data.get('state')
    pincode = data.get('pincode')
    email = data.get('email')
    
    # Get cart items
    cart_data = db.session.query(Cart, Product)\
        .join(Product).filter(Cart.user_id == user_id).all()
    
    if not cart_data:
        return jsonify({'error': 'Cart is empty'}), 400
    
    # Calculate total
    total = sum(c.quantity * p.current_price for c, p in cart_data)
    
    # Create order
    new_order = Order(
        user_id=user_id,
        customer_name=customer_name,
        address_line_1=address_line_1,
        city=city,
        state=state,
        pincode=pincode,
        mail=email,
        total_price=total,
        status='Pending'
    )
    
    db.session.add(new_order)
    db.session.flush()  # Get order ID
    
    # Add order items
    for cart, product in cart_data:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=cart.quantity,
            unit_price=product.current_price,
            subtotal=cart.quantity * product.current_price
        )
        db.session.add(order_item)
        
        # Update product stock
        product.count -= cart.quantity
    
    # Clear cart
    Cart.query.filter_by(user_id=user_id).delete()
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'success': True, 'order_id': new_order.id})
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('views.my_orders'))


@views.route('/my_orders')
def my_orders():
    """View user's orders"""
    if 'user_id' not in session:
        flash('Please login to view orders', 'warning')
        return redirect(url_for('auth.login'))
    
    orders = Order.query.filter_by(user_id=session['user_id'])\
        .order_by(Order.order_date.desc()).all()
    
    return render_template('my_orders.html', orders=orders)


@views.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    order = Order.query.filter_by(
        id=order_id, 
        user_id=session['user_id']
    ).first_or_404()
    
    if order.status != 'Pending':
        flash('Order cannot be cancelled', 'error')
        return redirect(url_for('views.my_orders'))
    
    # Restore product stock
    for item in order.order_items:
        product = Product.query.get(item.product_id)
        if product:
            product.count += item.quantity
    
    order.status = 'Cancelled'
    db.session.commit()
    
    flash('Order cancelled successfully', 'success')
    return redirect(url_for('views.my_orders'))


# ============= API ENDPOINTS =============
@views.route('/api/products/trending')
def api_trending_products():
    """API endpoint for trending products"""
    limit = request.args.get('limit', 10, type=int)
    
    products = db.session.query(Product)\
        .join(OrderItem)\
        .group_by(Product.id)\
        .order_by(func.count(OrderItem.id).desc())\
        .limit(limit).all()
    
    return jsonify([{
        'id': p.id,
        'name': p.product_name,
        'price': p.current_price,
        'image': p.product_picture,
        'rating': p.rating
    } for p in products])


@views.route('/api/cart/count')
def api_cart_count():
    """Get cart item count"""
    if 'user_id' not in session:
        return jsonify({'count': 0})
    
    count = Cart.query.filter_by(user_id=session['user_id']).count()
    return jsonify({'count': count})


@views.route('/api/wishlist/count')
def api_wishlist_count():
    """Get wishlist item count"""
    if 'user_id' not in session:
        return jsonify({'count': 0})
    
    count = Wishlist.query.filter_by(user_id=session['user_id']).count()
    return jsonify({'count': count})