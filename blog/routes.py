from flask import render_template, url_for, flash, redirect, request
from blog.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from blog.models import User, Post, Comment
from blog import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
import requests

@app.route('/')
@app.route('/home')
def home():
    url = "http://quotes.stormconsultancy.co.uk/random.json"
    quotes = requests.get(url).json()
    posts = Post.query.all()
    return render_template('home.html', posts=posts, quotes=quotes,  title="Home")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, please check your email!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Wrong login credentials", 'danger')

    return render_template('login.html', title="Login", form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(post=form.post.data,
                    author=current_user)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title="New Post", form=form)


@app.route('/comment/<int:post_id>', methods=['GET', 'POST'])
def new_comment(post_id):
    comments = Comment.query.filter_by(post_id=post_id)
    form = CommentForm()
    if form.validate_on_submit():

        comment = Comment(comment=form.comment.data, post_id=post_id)

        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added', 'success')
        return redirect(url_for('home'))
    return render_template('new_comment.html', title="New Comment", form=form, comments=comments)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile')
@login_required
def profile():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', title="profile", posts=posts)
