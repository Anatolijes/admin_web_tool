from src import app, bcrypt
from flask import render_template, request, url_for, redirect, session, flash, abort
from src import db
from src.forms import LoginForm, PostForm, RegistrationForm
from src.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required


@app.before_first_request
def create_table():
    db.create_all()


@login_required
@app.route("/")
@app.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        post1 = Post(title="test", content="content")
        post2 = Post(title="test2", content="content content content content content content content content content")

        db.session.add(post1)
        db.session.add(post2)
        posts = Post.query.all()
        return render_template('home.html', the_title="Home", posts=posts)


@app.route("/post/<int:post_id>")
def post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        p = Post.query.get(post_id)
        return render_template('post.html', post=p)


@login_required
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        form = PostForm()
        if form.validate_on_submit():
            p = Post(title=form.title.data, content=form.content.data)
            db.session.add(p)
            return redirect(url_for('home'))
        return render_template('create_post.html', the_title='create post', form=form)


@login_required
@app.route('/delete_post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            p = Post.query.get(post_id)
            db.session.delete(p)
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('error.html', error='something went wrong')


@login_required
@app.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    else:
        p = Post.query.get(post_id)
        form = PostForm()
        if request.method == 'GET':
            form.title.data = p.title
            form.content.data = p.content
            return render_template('update_post.html', the_title='Update', form=form)
        elif form.validate_on_submit():
            p.title = form.title.data
            p.content = form.content.data
            db.session.commit()
            return redirect(url_for('post', post_id=p.id))
        return render_template('error.html', error="something went wrong")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))

    return render_template('login.html', the_title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        return redirect(url_for('login'))
    else:
        return render_template('registration.html', title='Registration', form=form)
