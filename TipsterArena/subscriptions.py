# subscriptions.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from TipsterArena.models.user import SubscriptionPlan
from TipsterArena.extensions import db
from datetime import datetime, timedelta
from flask import request
from flask_login import current_user

subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/subscription-plans', methods=['GET'])
def view_subscription_plans():
    plans = SubscriptionPlan.query.all()
    return render_template('subscription_plans.html', plans=plans)


@subscriptions_bp.route('/create-subscription-plan', methods=['GET', 'POST'])
def create_subscription_plan():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        duration = request.form['duration']

        new_plan = SubscriptionPlan(name=name, price=price, duration=duration)
        db.session.add(new_plan)
        db.session.commit()

        flash('Subscription plan created successfully!', 'success')
        return redirect(url_for('view_subscription_plans'))

    return render_template('create_subscription_plan.html')

@subscriptions_bp.route('/subscribe/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def subscribe(plan_id):
    from models.user import SubscriptionPlan, UserSubscription
    plan = SubscriptionPlan.query.get_or_404(plan_id)

    if request.method == 'POST':
        end_date = datetime.utcnow() + timedelta(days=plan.duration)

        subscription = UserSubscription(
            user_id=current_user.user_id,
            plan_id=plan.plan_id,
            end_date=end_date
        )
        db.session.add(subscription)
        db.session.commit()

        flash('Subscribed successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('subscribe.html', plan=plan)
