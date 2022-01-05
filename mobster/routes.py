import os
import random
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from mobster import app, db, bcrypt
from mobster.forms import InviteForm, RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm, BankDepositForm, BankWithdrawForm, EquipmentBuyForm, HospitalForm, TurfBuyForm, DoMissionForm, AttackForm, HitListForm, InviteForm
from mobster.models import User, Post, Item, User_Stats, Turf, Missions
from mobster.utils import save_user_img, send_reset_email, pay_users
from flask_login import login_user, logout_user, current_user, login_required

# Scheduled Tasks
@app.cli.command()
def schedule():
    print("Paying Users...")
    pay_users()
    db.session.commit()
    print("Users successfully paid!")

# Convert data to JSON
@app.route("/user_json")
def data_json():
    user = [
        {
            "id": current_user.id,
            "username": current_user.username,
            "current_health": current_user.stats.user_current_health,
            "max_health": current_user.stats.user_max_health,
            "current_energy": current_user.stats.user_current_energy,
            "max_energy": current_user.stats.user_max_energy,
            "mission_current_stage": current_user.stats.user_current_mission_stage
        }
    ]
    return jsonify(user)

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    user = data_json()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    # Create Posts
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'danger')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('index.html', matches=user.json, posts=posts, form=form, title='Home', legend='Create Post')

@app.route("/register", methods=['GET', 'POST'])
def register():
    # If logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Hash user password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create user object
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # Add user to Db
        db.session.add(user)
        # Commit changes to Db
        db.session.commit()
        # Give user stats
        stats = User_Stats(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!', 'danger')
        return redirect(url_for('login'))    
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    # If logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # Validate login
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash('You have been logged in', 'danger')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful, please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.user_img.data:
            img_file = save_user_img(form.user_img.data)
            current_user.image_file = img_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account info has been updated!', 'danger')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'images/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'danger')
        return redirect(url_for('index'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    # Fetch Post(if no post return 404 error)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post updated!', 'danger')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':    
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted!', 'danger')
    return redirect(url_for('index'))

@app.route("/user/<string:username>")
def user_pages(username):
    # Display posts by user
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('user_pages.html', posts=posts, title=username, user=user)

@app.route("/reset_password", methods=['GET', 'POST'])
def request_password_reset():
    if current_user.is_authenticated:
        flash('You must be logged out to request a password reset!', 'danger')
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password, if you do not see an email check your spam folder!', 'danger')
        return redirect(url_for('login'))
    return render_template('request_password_reset.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('You must be logged out to request a password reset!', 'danger')
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is either invalid or expired!', 'danger')
        return redirect(url_for('request_password_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has successfully been updated!', 'danger')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# Main game routes
@app.route("/attack")
def attack():
    return render_template('game_templates/attack.html', title='Attack')

@app.route("/bank", methods=['GET', 'POST'])
@login_required
def bank():
    # Bank Functionality
    # Deposits
    user = User.query.filter_by(username=current_user.username).first()
    deposit_form = BankDepositForm()
    if deposit_form.validate_on_submit():
        if deposit_form.deposit.data > user.cash_on_hand:
            flash(f"You don't have {deposit_form.deposit.data} on hand to deposit!", 'danger')
            return redirect(url_for('bank'))
        else:
            user.cash_in_bank += deposit_form.deposit.data
            user.cash_on_hand -= deposit_form.deposit.data
            db.session.commit()
            flash(f'You have deposited {deposit_form.deposit.data}!', 'danger')
            return redirect(url_for('bank'))
    # Withdraws
    withdraw_form = BankWithdrawForm()
    if withdraw_form.validate_on_submit():
        if withdraw_form.withdraw.data > user.cash_in_bank:
            flash(f"You don't have {withdraw_form.withdraw.data} in the bank to withdraw!", 'danger')
            return redirect(url_for('bank'))
        else:
            user.cash_in_bank -= withdraw_form.withdraw.data
            user.cash_on_hand += withdraw_form.withdraw.data
            db.session.commit()
            flash(f'You have withdrawn {withdraw_form.withdraw.data}!', 'danger')
            return redirect(url_for('bank'))
    return render_template('game_templates/bank.html', title='Bank', deposit_form=deposit_form, withdraw_form=withdraw_form)

@app.route("/equipment", methods=['GET', 'POST'])
@login_required
def equipment():
    user = User.query.get(current_user.id)
    page = request.args.get('page', 1, type=int)
    items = Item.query.order_by(Item.level_required).where(Item.level_required <= user.stats.user_level).paginate(page=page, per_page=10)
    form = EquipmentBuyForm()
    return render_template('game_templates/equipment.html', title='Equipment', items=items, form=form, user=user)

@app.route("/equipment/sale/<int:id>", methods=['POST'])
@login_required
def buy_sell_equipment(id):
    form = EquipmentBuyForm()
    qty = form.quantity.data
    if form.validate_on_submit():
        if form.buy_submit.data and qty > 0:
            return redirect(f"/equipment/buy/{id}/{qty}")
        if form.sell_submit.data and qty > 0:
            return redirect(f"/equipment/sell/{id}/{qty}")
    else:
        flash('Something went bad!', 'danger')
        return redirect(url_for('equipment'))
        
    
@app.route("/equipment/buy/<int:id>/<int:quantity>", methods=['GET', 'POST'])
@login_required
def buy_equipment_qty(id, quantity):
    user = User.query.get_or_404(current_user.id)
    item = Item.query.get_or_404(id)
    qty = quantity
    total_cost = item.item_cost * qty
    total_xp = (5 * qty)
    if user.cash_on_hand >= total_cost:
        user.add_item(item, qty)
        user.cash_on_hand -= total_cost
        user.give_xp(total_xp)
        db.session.commit()
        flash(f'You bought {qty}x {item.item_name}(s) for ${total_cost} and gained {total_xp}xp!', 'danger')
        return redirect(url_for('equipment'))
    else:
        flash(f"You need ${'{:,}'.format(total_cost)} to buy {qty}x {item.item_name}(s)!", 'danger')
        return redirect(url_for('equipment'))

    
@app.route("/equipment/sell/<int:id>/<int:quantity>", methods=['GET', 'POST'])
@login_required
def sell_equipment_qty(id, quantity):
    user = User.query.get_or_404(current_user.id)
    item = Item.query.get_or_404(id)
    qty = quantity
    total_sale = item.item_sell * qty
    if user.sell_item(item, quantity):
        user.cash_on_hand += total_sale
        db.session.commit()
        flash(f'You sold {qty}x {item.item_name}(s) for ${total_sale}!', 'danger')
        return redirect(url_for('equipment'))
    else:
        flash(f"You don't have {qty}x {item.item_name}(s) to sell!", 'danger')
        return redirect(url_for('equipment'))
    
    
@app.route("/godfather")
def godfather():
    return render_template('game_templates/godfather.html', title='Godfather')
    
@app.route("/hitlist")
def hitlist():
    form = HospitalForm()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).where(User_Stats.user_on_hitlist == True).outerjoin(User_Stats).paginate(page=page, per_page=10)
    return render_template('game_templates/hitlist.html', title='Hitlist', form=form, users=users)

@app.route("/hitlist/add/<user_id>", methods=['POST'])
def add_to_hitlist(user_id):
    form = HitListForm()
    if request.method == 'POST' and form.validate_on_submit:
        user = User.query.get(user_id)
        if form.bounty.data >= user.stats.user_total_income * 10:
            if current_user.cash_on_hand < form.bounty.data:
                flash(f'You don\'t have {form.bounty.data} to add {user.username} to the hitlist!', 'danger')
                return redirect(url_for('my_mobster', id=user.id))
            else:
                if user.stats.user_on_hitlist:
                    flash(f'{user.username} is already on the hitlist!', 'danger')
                    return redirect(url_for('my_mobster', id=user.id))
                else:
                    current_user.cash_on_hand -= form.bounty.data
                    user.stats.user_on_hitlist = True
                    user.stats.user_current_bounty = form.bounty.data
                    post = Post(user_id=current_user.id, title=f"New Target!", content=f"{current_user.username} just put a bounty of {form.bounty.data} on {user.username}'s head!")
                    db.session.add(post)
                    db.session.commit()
                    flash(f"You just put a bounty of {form.bounty.data} on {user.username}'s head!", 'danger')
                    return redirect(url_for('hitlist'))
    return redirect('my_mobster/', id=current_user.id)

@app.route("/missions", methods=['GET', 'POST'])
@login_required
def missions():
    page = request.args.get('page', 1, type=int)
    missions = Missions.query.order_by(Missions.id).where(Missions.id == current_user.stats.user_current_mission_id).paginate(page=page, per_page=5)
    form = DoMissionForm()
    if form.validate_on_submit():
        current_mission_id = current_user.stats.user_current_mission_id
        current_mission = Missions.query.get(current_mission_id)
        if current_user.stats.user_current_energy >= current_mission.mission_required_energy:
            mastery_complete = False
            current_user.stats.user_current_energy -= current_mission.mission_required_energy
            current_user.stats.user_current_mission_stage += 1
            current_user.stats.user_total_missions_complete += 1
            cash_reward = random.randint(current_mission.mission_reward_min_cash, current_mission.mission_reward_max_cash)
            xp_reward = random.randint(current_mission.mission_reward_min_xp, current_mission.mission_reward_max_xp)
            current_user.cash_on_hand += cash_reward
            current_user.give_xp(xp_reward)
            complete_message = f"Congrats! You completed {current_mission.mission_name}! You earned ${cash_reward} and {xp_reward}xp but used {current_mission.mission_required_energy} energy!"
            db.session.commit()
            if current_user.stats.user_current_mission_stage > current_mission.mission_required_mastery:
                mastery_complete = True
                current_user.stats.user_current_mission_id += 1
                current_user.stats.user_current_mission_stage = 1
                mastery_cash_reward = random.randint(current_mission.mission_mastery_reward_min_cash, current_mission.mission_mastery_reward_max_cash)
                mastery_xp_reward = random.randint(current_mission.mission_mastery_reward_min_xp, current_mission.mission_mastery_reward_max_xp)
                current_user.cash_on_hand += mastery_cash_reward
                current_user.give_xp(mastery_xp_reward)
                mastery_message = f"Congrats! You mastered {current_mission.mission_name}! You earned ${mastery_cash_reward} and {mastery_xp_reward}xp!  A new mission is now available!"
                db.session.commit()
            if mastery_complete:
                flash(complete_message, 'danger')
                flash(mastery_message, 'danger')
            else:
                flash(complete_message, 'danger')
            return redirect(url_for('missions'))
        if current_user.stats.user_current_energy < current_mission.mission_required_energy:
            flash(f"You don't have enough energy! You need {current_mission.mission_required_energy} energy to {current_mission.mission_name}!", 'danger')
            return redirect(url_for('missions'))
    return render_template('game_templates/missions.html', title='Missions', missions=missions, form=form)
    
@app.route("/turf")
def turf():
    user = User.query.get(current_user.id)
    page = request.args.get('page', 1, type=int)
    turfs = Turf.query.order_by(Turf.level_required).where(Turf.level_required <= user.stats.user_level).paginate(page=page, per_page=5)
    form = TurfBuyForm()
    return render_template('game_templates/turf.html', title='Turf', turfs=turfs, form=form, user=user)
    
@app.route("/turf/sale/<int:id>", methods=['POST'])
@login_required
def buy_sell_turf(id):
    form = TurfBuyForm()
    qty = form.quantity.data
    if form.validate_on_submit():
        if form.buy_submit.data and qty > 0:
            return redirect(f"/turf/buy/{id}/{qty}")
        if form.sell_submit.data and qty > 0:
            return redirect(f"/turf/sell/{id}/{qty}")
    else:
        flash('Something went bad!', 'danger')
        return redirect(url_for('turf'))
    
@app.route("/turf/buy/<int:id>/<int:quantity>", methods=['GET', 'POST'])
@login_required
def buy_turf_qty(id, quantity):
    user = User.query.get_or_404(current_user.id)
    turf = Turf.query.get_or_404(id)
    qty = quantity
    total_cost = turf.turf_cost * qty
    total_xp = (5 * qty)
    if user.cash_on_hand >= total_cost:
        user.add_turf(turf, qty)
        user.cash_on_hand -= total_cost
        user.give_xp(total_xp)
        user.stats.user_total_income += (turf.turf_income * qty)
        db.session.commit()
        flash(f'You bought {qty}x {turf.turf_name}(s) for ${total_cost} and gained {total_xp}xp!', 'danger')
        return redirect(url_for('turf'))
    else:
        flash(f"You need ${'{:,}'.format(total_cost)} to buy {qty}x {turf.turf_name}(s)!", 'danger')
        return redirect(url_for('turf'))

    
@app.route("/turf/sell/<int:id>/<int:quantity>", methods=['GET', 'POST'])
@login_required
def sell_turf_qty(id, quantity):
    user = User.query.get_or_404(current_user.id)
    turf = Turf.query.get_or_404(id)
    qty = quantity
    total_sale = turf.turf_sell * qty
    if user.sell_turf(turf, quantity):
        user.cash_on_hand += total_sale
        user.stats.user_total_income -= turf.turf_income
        if user.stats.user_total_income < 0:
            user.stats.user_total_income = 0
        db.session.commit()
        flash(f'You sold {qty}x {turf.turf_name}(s) for ${total_sale}!', 'danger')
        return redirect(url_for('turf'))
    else:
        flash(f"You don't have {qty}x {turf.turf_name}(s) to sell!", 'danger')
        return redirect(url_for('turf'))    

    
@app.route("/mods")
def mods():
    return render_template('game_templates/mods.html', title='Mods')
    
@app.route("/tos")
def tos():
    return render_template('game_templates/tos.html', title='TOS')
    
@app.route("/hospital", methods=['GET', 'POST'])
def hospital():
    user = User.query.get_or_404(current_user.id)
    form = HospitalForm()
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).where(User_Stats.user_in_icu == True).outerjoin(User_Stats).paginate(page=page, per_page=10)
    if user.cash_on_hand >= 500 and form.validate_on_submit():
        if form.heal_submit.data:
            if user.stats.user_current_health == user.stats.user_max_health:
                flash('Your health is already full!', 'danger')
            else:
                user.heal_user()
                user.cash_on_hand -= 500        
                db.session.commit()
        
        
    return render_template('game_templates/hospital.html', title='ICU', form=form, users=users)
    
@app.route("/hospital/punch/<int:id>", methods=['POST'])
def hospital_punch(id):
    user = User.query.get(id)
    form = HospitalForm()
    if form.punch_submit.data and user.get_punched():
        post = Post(user_id=current_user.id, title=f"{current_user.username} just punched {user.username}!", content=f"{user.username} just got rocked for 10hp!")
        db.session.add(post)
        db.session.commit()
        flash(f'You just rocked {user.username} for 10hp!', 'danger')
        if user.stats.user_on_hitlist and user.stats.user_current_health == 0:
            bounty = '{:,}'.format(user.stats.user_current_bounty)
            bounty_int = user.stats.user_current_bounty
            flash(f'You have killed {user.username} and have collected a bounty of $ {bounty}', 'danger')
            current_user.cash_on_hand += user.stats.user_current_bounty
            post = Post(user_id=current_user.id, title=f"Target Eliminated", content=f"{current_user.username} ended {user.username} and collected their bounty of ${bounty}!")
            user.stats.user_on_hitlist = False
            current_user.stats.user_total_bounty_collected += bounty_int
            user.stats.user_current_bounty = 0
            db.session.add(post)
            db.session.commit()
    else:
        flash('Chill man  he\'s dead already!', 'danger')
        db.session.commit()
    return redirect(url_for('my_mobster', id=id))
    
    
@app.route("/made_men")
def made_men():
    page = request.args.get('page', 1, type=int)
    highest_level = User.query.order_by(User_Stats.user_level.desc()).outerjoin(User_Stats).paginate(page=page, per_page=100)
    highest_bounty = User.query.order_by(User_Stats.user_total_income.desc()).outerjoin(User_Stats).paginate(page=page, per_page=100)
    most_missions = User.query.order_by(User_Stats.user_total_missions_complete.desc()).outerjoin(User_Stats).paginate(page=page, per_page=100)
    fights_won = User.query.order_by(User.id).paginate(page=page, per_page=100)
    fights_lost = User.query.order_by(User.id).paginate(page=page, per_page=100)
    most_deaths = User.query.order_by(User.id).paginate(page=page, per_page=100)
    most_kills = User.query.order_by(User.id).paginate(page=page, per_page=100)
    bounties_collected = User.query.order_by(User_Stats.user_total_bounty_collected.desc()).outerjoin(User_Stats).paginate(page=page, per_page=100)
    
    return render_template('game_templates/made_men.html', title='Made Men', highest_level=highest_level, highest_bounty=highest_bounty, most_missions=most_missions, fights_won=fights_won, fights_lost=fights_lost, most_deaths=most_deaths, most_kills=most_kills,bounties_collected=bounties_collected)

@app.route("/my_mob")
def my_mob():
    return render_template('game_templates/my_mob.html', title='My Mob')
    
@app.route("/my_mobster/<id>")
def my_mobster(id):
    user = User.query.filter_by(id=id).first_or_404()
    min_bounty = user.stats.user_total_income * 10
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=10)
    form = HospitalForm()
    hitlist_form = HitListForm()
    attack_form = AttackForm()
    invite_form = InviteForm()
    return render_template('game_templates/my_mobster.html', title='My Mobster', form=form, hitlist_form=hitlist_form, attack_form=attack_form, invite_form=invite_form, user=user, min_bounty=min_bounty, posts=posts)
