# services/resource/project/tests/utils.py


from project.utils.basemodel import db
from project.api.user.models import User
from project.api.blog.models import Category, Article


def add_user(username, email, password, admin=False):
    user = User(username, email, password, admin=admin)
    with db.auto_commit():
        db.session.add(user)
    return user


def add_admin(username, email, password):
    admin = add_user(username, email, password, admin=True)
    return admin


def get_token(client, admin=False):
    add_user('test', 'test@qq.com', 'test1234', admin=admin)
    response = client.post(
        '/auth/login',
        json={'email': 'test@qq.com', 'password': 'test1234'}
    )
    token = response.get_json().get('auth_token')
    return token


def add_category(name):
    category = Category(name=name)
    with db.auto_commit():
        db.session.add(category)
    return category


def add_article(title, body, category):
    """Add a new article.
    :param title(str): the article title
    :param body(str): the article body
    :param category(Category instance): the article category.
    :return Article (instance)
    """
    article = Article(title=title, body=body)
    article.category = category
    with db.auto_commit():
        db.session.add(article)
    return article
