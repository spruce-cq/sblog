# services/resource/project/api/blog/__init__.py


from flask import Blueprint

from project.api.blog import category, article

blog_bp = Blueprint('blog', __name__)
category.category_paint.depict(blog_bp)
article.article_paint.depict(blog_bp)
