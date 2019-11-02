# services/resource/project/api/blog/category.py


from flask import jsonify

from project.api.blog.forms import CategoryForm
from project.api.blog.models import Category
from project.api.utils import authenticate
from project.exceptions import BadRequest
from project.utils import paint
from project.utils.basemodel import db
from project.utils.jsonenhancer import toDict


category_paint = paint.Paint()


@category_paint.route('/categories', methods=['POST'])
@authenticate
def add_category():
    """Add a new category."""
    form = CategoryForm()
    resp_msg = 'Invalid payload.'
    if not form.validate():
        return BadRequest(resp_msg)
    name = form.name.data
    category = Category.query.filter_by(name=name).first()
    if category:
        return BadRequest('The category already exists.')
    with db.auto_commit(resp_msg):
        category = Category(name=name)
        db.session.add(category)
    resp_pbj = {
        'status': 'success',
        'message': f'category: {name} was added.'
    }
    return jsonify(resp_pbj), 201


@category_paint.route('/categories', methods=['GET'])
def get_all_categories():
    """Get all categoryies."""
    resp_obj = {
        'status': 'success',
        'data': [toDict(category) for category in Category.query.all()]
    }
    return jsonify(resp_obj), 200


@category_paint.route('/categories/<cate_id>', methods=['GET'])
def get_single_category_by(cate_id):
    """Get Category by category's id."""
    resp_message = 'Invalid payload.'
    try:
        cate_id = int(cate_id)
    except ValueError:
        return BadRequest(resp_message)

    category = Category.query.get_or_404(cate_id, resp_message)
    resp_obj = {
        'status': 'success',
        'data': toDict(category)
    }
    return jsonify(resp_obj), 200


@category_paint.route('/categories/<cate_id>', methods=['DELETE'])
@authenticate
def delete_single_category(cate_id):
    """Delete category by id."""
    resp_message = 'Invalid payload.'
    try:
        cate_id = int(cate_id)
    except ValueError:
        return BadRequest(resp_message)
    category = Category.query.get_or_404(cate_id, resp_message)
    with db.auto_commit():
        db.session.delete(category)
    resp_obj = {
        'status': 'success',
        'message': f'{category.id}: {category.name} is already deleted.'
    }
    # we need return message, so not for 204
    # the http status maybe not properly
    return jsonify(resp_obj), 202
