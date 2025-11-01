# app/recommendations.py
from app.models import Product, User, Order, OrderItem, Cart, Wishlist
from app import db
from sqlalchemy import func, desc
import numpy as np
from collections import defaultdict

class RecommendationEngine:
    """Hybrid Recommendation System combining Collaborative and Content-Based filtering"""
    
    @staticmethod
    def get_user_recommendations(user_id, limit=10):
        """Get personalized recommendations for a user"""
        # Collaborative filtering
        collab_recs = RecommendationEngine._collaborative_filtering(user_id, limit//2)
        
        # Content-based filtering
        content_recs = RecommendationEngine._content_based_filtering(user_id, limit//2)
        
        # Merge and deduplicate
        all_recs = list(set(collab_recs + content_recs))
        
        # If not enough, add trending products
        if len(all_recs) < limit:
            trending = RecommendationEngine._get_trending_products(limit - len(all_recs))
            all_recs.extend(trending)
        
        return all_recs[:limit]
    
    @staticmethod
    def _collaborative_filtering(user_id, limit):
        """User-based collaborative filtering"""
        # Find similar users based on purchase history
        user_products = db.session.query(OrderItem.product_id)\
            .join(Order).filter(Order.user_id == user_id).all()
        user_product_ids = [p[0] for p in user_products]
        
        if not user_product_ids:
            return []
        
        # Find users who bought similar products
        similar_users = db.session.query(Order.user_id, func.count().label('common'))\
            .join(OrderItem)\
            .filter(OrderItem.product_id.in_(user_product_ids))\
            .filter(Order.user_id != user_id)\
            .group_by(Order.user_id)\
            .order_by(desc('common'))\
            .limit(10).all()
        
        similar_user_ids = [u[0] for u in similar_users]
        
        # Get products bought by similar users
        recommended_products = db.session.query(OrderItem.product_id, func.count().label('freq'))\
            .join(Order)\
            .filter(Order.user_id.in_(similar_user_ids))\
            .filter(OrderItem.product_id.notin_(user_product_ids))\
            .group_by(OrderItem.product_id)\
            .order_by(desc('freq'))\
            .limit(limit).all()
        
        return [p[0] for p in recommended_products]
    
    @staticmethod
    def _content_based_filtering(user_id, limit):
        """Content-based filtering using product attributes"""
        # Get user's favorite categories and brands
        user_prefs = db.session.query(
            Product.category, 
            Product.brand_id,
            func.count().label('count')
        ).join(OrderItem).join(Order)\
         .filter(Order.user_id == user_id)\
         .group_by(Product.category, Product.brand_id)\
         .order_by(desc('count'))\
         .first()
        
        if not user_prefs:
            return []
        
        # Get user's purchased products
        purchased = db.session.query(OrderItem.product_id)\
            .join(Order).filter(Order.user_id == user_id).all()
        purchased_ids = [p[0] for p in purchased]
        
        # Recommend similar products
        recommendations = Product.query\
            .filter(Product.category == user_prefs[0])\
            .filter(Product.brand_id == user_prefs[1])\
            .filter(Product.id.notin_(purchased_ids))\
            .order_by(desc(Product.rating))\
            .limit(limit).all()
        
        return [p.id for p in recommendations]
    
    @staticmethod
    def _get_trending_products(limit):
        """Get currently trending products"""
        trending = db.session.query(
            OrderItem.product_id,
            func.count().label('sales')
        ).group_by(OrderItem.product_id)\
         .order_by(desc('sales'))\
         .limit(limit).all()
        
        return [p[0] for p in trending]
    
    @staticmethod
    def get_similar_products(product_id, limit=4):
        """Get products similar to a given product"""
        product = Product.query.get(product_id)
        if not product:
            return []
        
        similar = Product.query\
            .filter(Product.id != product_id)\
            .filter(Product.category == product.category)\
            .filter(Product.brand_id == product.brand_id)\
            .order_by(desc(Product.rating))\
            .limit(limit).all()
        
        if len(similar) < limit:
            # Add products from same category
            additional = Product.query\
                .filter(Product.id != product_id)\
                .filter(Product.category == product.category)\
                .filter(Product.id.notin_([s.id for s in similar]))\
                .order_by(desc(Product.rating))\
                .limit(limit - len(similar)).all()
            similar.extend(additional)
        
        return similar


# Update views.py to use recommendations
from app.recommendations import RecommendationEngine

@views.route('/recommendations')
def show_recommendations():
    if 'user_id' not in session:
        # Show trending for guests
        product_ids = RecommendationEngine._get_trending_products(20)
    else:
        product_ids = RecommendationEngine.get_user_recommendations(session['user_id'], 20)
    
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    return render_template('recommendations.html', products=products)