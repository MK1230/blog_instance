#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app import create_app, db
from app.models import Role, User, Post, Follow, Permission, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 系统中不存在 FLASK_CONFIG 环境变量时，try 语句返回 create_app('default')
# 当存在 FLASK_CONFIG 环境变量，且值不属于 config 的键时，报 KeyError 错，此时通过 except 语句返回 create_app('default')
try:
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
except KeyError:
    app = create_app('default')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User, Post=Post, Follow=Follow, Permission=Permission, Comment=Comment)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://{}/index.html'.format(covdir))
        COV.erase()


@manager.command
def profile(length=10, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[
                                      length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.models import Role, User

    upgrade()

    Role.insert_roles()
    User.add_self_follows()


if __name__ == '__main__':
    manager.run()
