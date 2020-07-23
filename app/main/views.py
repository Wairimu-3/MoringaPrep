from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from ..models import Comment, User, Tutorial
from . import main
from .forms import UpdateProfile, TutorialForm, CommentForm
from .. import db, photos
import markdown2

#Views
@main.route('/')
def index():
    '''
    Function to load the index page
    '''
    tutorial_list = tutorial.query.all()

       
    return render_template('index.html', tutorial_list=tutorial_list)


@main.route('/tutorial/comment/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
       #Updated comment instance
       new_comment = Comment(tutorial_id=id, details=form.details.data, user_id = current_user.id)
       #save comment method
       db.session.add(new_comment)
       db.session.commit()
       return redirect(url_for('main.index'))
        
    title = 'New Comment'
    return render_template('new_comment.html', title= title, comment_form = form)
        

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))
    
    return render_template('profile/update.html', form=form)

@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname = uname))

@main.route('/comment/<int:id>')
def single_comment(id):
    comment = Comment.query.get(id)
    if comment is None:
        abort(404)
    
    format_comment = markdown2.markdown(comment.details, extras=['code-friendly', 'fenced-code-blocks'])
    return render_template('comment.html', comment=comment, format_comment=format_comment)

@main.route('/tutorial/new/', methods=['GET', 'POST'])
def new_tutorial():
    '''
    Function to allow a user add a new tutorial post
    '''
    form = tutorialForm()
    if form.validate_on_submit():
        new_tutorial = tutorial(heading=form.tutorial_heading.data, content=form.tutorial_content.data, author=form.tutorial_author.data)
        db.session.add(new_tutorial)
        db.session.commit()
        return redirect(url_for('main.index'))

    title = 'New tutorial'
    return render_template('new_tutorial.html', title = title, tutorial_form = form)

@main.route('/tutorial/<int:id>')
def single_tutorial(id):
    tutorial = tutorial.query.get(id)
    comments = Comment.query.filter_by(tutorial_id = id).all()
    if tutorial is None:
        abort(404)

    format_tutorial = markdown2.markdown(tutorial.content, extras=["code-friendly", "fenced-code-blocks"])
    return render_template('tutorial_r.html', tutorial = tutorial, comments = comments, format_tutorial = format_tutorial)
    
