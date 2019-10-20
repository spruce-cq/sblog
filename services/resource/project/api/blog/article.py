# service/resource/project/api/blog/article.py


from flask import jsonify

from project.api.utils import authenticate, convert_to_int_for
from project.api.blog.forms import ArticleForm
from project.api.blog.models import Article
from project.exceptions import BadRequest
from project.utils import paint
from project.utils.basemodel import db
from project.utils.jsonenhancer import toJSON


article_paint = paint.Paint()


@article_paint.route('/articles', methods=['POST'])
@authenticate
def add_article():
    """Add a new article."""
    form = ArticleForm()
    resp_msg = 'Invalid payload.'
    if not form.validate():
        return BadRequest(resp_msg)
    title = form.title.data
    body = form.body.data
    category = form.category.data
    article = Article.query.filter_by(title=title).count()
    if article > 0:
        return BadRequest('The article already exists')
    article = Article(title=title, body=body, category_id=category)
    with db.auto_commit(resp_msg):
        db.session.add(article)
    resp_obj = {
        'status': 'success',
        'message': f'article: {title} was added.'
    }
    return jsonify(resp_obj), 201


@article_paint.route('/articles', methods=['GET'])
def get_all_articles():
    """Get all articles."""
    resp_obj = {
        'status': 'success',
        'data': [toJSON(article) for article in Article.query.all()]
    }
    return jsonify(resp_obj), 200


@article_paint.route('/articles/<art_id>', methods=['GET'])
def get_single_article(art_id):
    """Get single article by `art_id`."""
    art_id = convert_to_int_for(art_id, description='Invalid path params.')
    article = Article.query.get_or_404(
        art_id, description='Invalid path params.')
    resp_obj = {
        'status': 'success',
        'data': toJSON(article)
    }
    return jsonify(resp_obj), 200


@article_paint.route('/articles/<art_id>', methods=['DELETE'])
@authenticate
def delete_single_article(art_id):
    """Delete single article by `art_id`."""
    art_id = convert_to_int_for(art_id)
    article = Article.query.get_or_404(
        art_id, description='Invalid path params.')
    with db.auto_commit('Delete fail'):
        db.session.delete(article)
    resp_obj = {
        'status': 'success',
        'message': f'{article.id}: {article.title} is already deleted.'
    }
    return jsonify(resp_obj), 202


@article_paint.route('/articles', methods=['PUT'])
@authenticate
def update_single_article():
    """Update singel article by `form.aid.data`."""
    form = ArticleForm()
    resp_msg = 'Invalid payload.'
    if not form.validate():
        return BadRequest(resp_msg)
    aid = form.aid.data
    title = form.title.data
    body = form.body.data
    category = form.category.data
    article = Article.query.get_or_404(aid, description=resp_msg)
    with db.auto_commit(resp_msg):
        article.title = title
        article.body = body
        article.category_id = category
    resp_obj = {
        'status': 'success',
        'message': f'{aid}: article is already updated.'
    }
    return jsonify(resp_obj), 200
