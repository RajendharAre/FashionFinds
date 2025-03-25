#admin.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import User, db
from flask_login import current_user, login_required
admin = Blueprint('admin', __name__)

@admin.route('/role_approval')
def role_approval():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        return redirect(url_for('auth.home'))
    users = User.query.filter_by(role='delivery_agent', approved=False).all()
    return render_template('role_approval.html', users=users)

@admin.route('/approve_user/<int:user_id>', methods=['POST'])
def approve_user(user_id):
    user = User.query.get(user_id)
    print(user)
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('admin.role_approval'))
    user.approved = True
    db.session.commit()


@admin.route('/admin_dashboard')
# @login_required
def admin_dashboard():
    # if not current_user.is_authenticated or current_user.role != 'admin':
    #     flash('Unauthorized access', 'danger')
    #     return redirect(url_for('auth.home'))
    if 'user_id' not in session:
        flash('Unauthorized access', 'danger')
        print('user_id not in session')
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        print(user.role, "not admin")
        return redirect(url_for('auth.home'))
    
    # Add your dashboard statistics here
    total_users = User.query.count()
    pending_approvals = User.query.filter_by(approved=False).count()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         pending_approvals=pending_approvals)

@admin.route('/add_products')
# @login_required
def add_products():
    # if not current_user.is_authenticated or current_user.role != 'admin':
    #     flash('Unauthorized access', 'danger')
    #     print(not current_user.is_authenticated, current_user.role, "unauthorized")
    #     return redirect(url_for('auth.home'))
    if 'user_id' not in session:
        flash('Unauthorized access', 'danger')
        print('user_id not in session')
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if user.role != 'admin':
        print(user.role, "not admin")
        return redirect(url_for('auth.home'))
    
    return render_template('add_products.html')
