# services/resource/manager.py


import unittest
import coverage
import click

from flask.cli import FlaskGroup

from project import db, create_app
from project.api.user.models import User


app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.Coverage(
    branch=True,
    include='project/*',
    omit=['project/test/*', 'project/config.py']
)

COV.start()

@cli.command()
def recreate_db():
    """ recreate db. """
    print('recreate db')
    db.drop_all()
    db.create_all()


@cli.command()
def seed_db_user():
    print("seed db")
    db.session.add(User('jianxin', 'jianxin@qq.com', 'password1234'))
    db.session.add(User('changqing', 'changqing@qq.com', 'password1234', admin=True))
    db.session.commit()


@cli.command()
@click.option('--category', default=3, help='Quantity of categories, default is 3.')
@click.option('--article', default=15, help='Quantity of posts, default is 15.')
def forge(category, article):
    """Generates the fake categories, posts, and comments."""
    from faker_data import fake_admin, fake_category, fake_article
    db.drop_all()
    db.create_all()
    click.echo('Generating the administrator...')
    fake_admin()
    click.echo('Generating %d categories...' % category)
    fake_category(category)
    click.echo('Generating %d posts...' % article)
    fake_article(article)
    click.echo('Done.')


@cli.command()
def test():
    test_suite = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    test_suite = unittest.TestLoader().discover('project/tests',pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    cli()