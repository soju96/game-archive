from flask import Blueprint, render_template, request, redirect, url_for, abort
#from app.models import Post, Comment
from app.forms import CommentForm, PostForm

bp = Blueprint('main', __name__, url_prefix='/ssm')

# 인기 게시글 목록 보기
@bp.route('/')
def popular_posts():
    popular_posts = Post.query.order_by(Post.views.desc()).limit(3).all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=10)
    
    return render_template('common/main.html', popular_posts=popular_posts, posts=posts)

# 게시글 상세 보기
@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    post.views += 1  # 조회수 증가
    post.save()
    comments = post.comments.all()
    
    form = CommentForm()
    if request.method == 'POST' and form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post)
        comment.save()
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    return render_template('post_detail.html', post=post, comments=comments, form=form)

# 게시글 작성
@bp.route('/post/new', methods=['GET', 'POST'])
def post_create():
    form = PostForm()
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data)
        post.save()
        return redirect(url_for('main.popular_posts'))
    
    return render_template('post_form.html', form=form)

# 댓글 작성
@bp.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post)
        comment.save()
        return redirect(url_for('main.post_detail', post_id=post.id))
    
    return render_template('add_comment.html', form=form, post=post)
