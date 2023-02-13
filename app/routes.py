from app import app, mail
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm, ContactForm, PostForm, CommentForm
from app.models import User, Post, Comment
from flask_mail import Mail, Message
#from app.api import RNA_dict, FRET_dict



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/julia')
def julia():
    return render_template('julia.html')

@app.route('/contact', methods=["GET","POST"])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(f"Name:{form.name.data}, E-mail:{form.email.data}, Subject:{form.subject.data}, Message:{form.message.data}")
            flash(f'Thank you, {form.name.data}. We will get back to you as soon as possible.','success') 
            msg = Message(form.subject.data, recipients=['zoefreeman13@gmail.com'])
            msg.body = f'From: {form.name.data}, {form.email.data}, {form.subject.data}, {form.message.data}'
            mail.send(msg)
            return redirect(url_for('index'))
        else:
            return render_template('contact.html', form=form)
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/news')
def news():
    posts = Post.query.all()
    return render_template('news.html', posts=posts)

@app.route('/papers')
def papers():
    return render_template('papers.html', RNA_dict=RNA_dict, FRET_dict=FRET_dict)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user:
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        print(username, password)
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

@app.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Get data from form
        title = form.title.data
        body = form.body.data
        # Create new post instance which will also add to db
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"{new_post.title} has been listed", "success")
        return redirect(url_for('news'))
        
    return render_template('create.html', form=form)

@app.route('/posts/<int:post_id>')
def get_post(post_id):
    # post = Post.query.get_or_404(post_id)
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    comments = Comment.query.all()
    return render_template('post.html', post=post, comments=comments)
    

@app.route('/posts/<post_id>/edit', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        title = form.title.data
        body = form.body.data
        # update the post using the .update method
        post.update(title=title, body=body)
        flash(f"{post.title} has been updated!", "success")
        return redirect(url_for('get_post', post_id=post.id))
    if request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('edit_post.html', post=post, form=form)

@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", "info")
    return redirect(url_for('index'))

@app.route('/posts/<post_id>/create-comment', methods=['GET', 'POST'])
def create_comment(post_id):
#def create_comment():
    post = Post.query.get_or_404(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('index'))
    form = CommentForm()
    if form.validate_on_submit():
        # Get data from form
        name = form.name.data
        email = form.email.data
        comment = form.comment.data
        new_comment = Comment(name=name, email=email, comment=comment, post_id=post_id)
        flash("Your comment has been added to the post", "success")
        return redirect(url_for("get_post", post_id=post.id))
        
    return render_template('create_comment.html', form=form)

# @app.route('/posts/<post_id>/<comment_id>/delete')
@app.route('/comments/<comment_id>/delete')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash(f"A comment with id {comment_id} does not exist", "danger")
        return redirect(url_for('index'))
    # Make sure the post author is the current user
    comment.delete()
    flash(f"Comment has been deleted", "info")
    return redirect(url_for('news'))

@app.route('/comments/<int:comment_id>')
def get_comment(comment_id):
    # post = Post.query.get_or_404(post_id)
    comment = Comment.query.get(comment_id)
    if not comment:
        flash(f"A comment with id {comment_id} does not exist", "danger")
        return redirect(url_for('index'))
    return render_template('comment.html', comment=comment)

# @app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
# def create_comment(post_id):
#     post = Post.query.get_or_404(post_id)
#     form = CommentForm()
#     if request.method == 'POST': # this only gets executed when the form is submitted and not when the page loads
#         if form.validate_on_submit():
#             name = form.name.data
#             email = form.email.data
#             comment = form.comment.data
#             new_comment = Comment(name=name, email=email, comment=comment)
#             db.session.add(new_comment)
#             db.session.commit()
#             flash("Your comment has been added to the post", "success")
#             return redirect(url_for("post", post_id=post.id))
#     return render_template("create_post.html", title="Add Comment", 
# form=form, post_id=post_id)