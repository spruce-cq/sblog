import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from project.api.blog.models import Article, Category
from project.api.user.models import User
from project.utils.basemodel import db

fake = Faker()


def fake_admin():
    admin = User(
        email='666@qq.com',
        username='admin',
        admin=True,
        password = 'abcd1234'
    )
    db.session.add(admin)

    user = User(
        email='555@qq.com',
        username='changqing',
        admin=False,
        password = 'abcd1234'
    )
    db.session.add(user)
    db.session.commit()


def fake_category(count=4):
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_article(count=15):
    for i in range(count):
        article = Article(
            title=fake.sentence(5),
            body=fake.text(2000),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(article)
    db.session.commit()