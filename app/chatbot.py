# app/chatbot.py
from flask import Blueprint, request, jsonify
import openai  # or use any other AI API

chatbot_bp = Blueprint('chatbot', __name__)

class FAQBot:
    FAQ_DATA = {
        "shipping": {
            "question": "What is your shipping policy?",
            "answer": "We offer free shipping on orders above ₹999. Standard delivery takes 3-5 business days."
        },
        "returns": {
            "question": "What is your return policy?",
            "answer": "We accept returns within 30 days of purchase. Items must be unused with original tags."
        },
        "payment": {
            "question": "What payment methods do you accept?",
            "answer": "We accept Credit/Debit cards, UPI, Net Banking, and Cash on Delivery."
        },
        "tracking": {
            "question": "How do I track my order?",
            "answer": "You can track your order from 'My Orders' section in your account."
        }
    }
    
    @staticmethod
    def get_response(user_message):
        """Simple FAQ matching - can be enhanced with ML"""
        user_message = user_message.lower()
        
        # Check for keyword matches
        if any(word in user_message for word in ['ship', 'delivery', 'dispatch']):
            return FAQBot.FAQ_DATA['shipping']['answer']
        elif any(word in user_message for word in ['return', 'refund', 'exchange']):
            return FAQBot.FAQ_DATA['returns']['answer']
        elif any(word in user_message for word in ['payment', 'pay', 'cod']):
            return FAQBot.FAQ_DATA['payment']['answer']
        elif any(word in user_message for word in ['track', 'order status', 'where']):
            return FAQBot.FAQ_DATA['tracking']['answer']
        else:
            return "I'm here to help! Could you please be more specific about your query?"

@chatbot_bp.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = FAQBot.get_response(user_message)
    
    return jsonify({
        'message': response,
        'suggestions': [
            'Shipping information',
            'Return policy',
            'Payment methods',
            'Track order'
        ]
    })

# Register blueprint in __init__.py
# app.register_blueprint(chatbot_bp, url_prefix='/chatbot')