# coding: utf-8
import unittest
import transaction
from os.path import split

from pyramid import testing

from .models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            MyModel,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = MyModel(name='one', value=55)
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'task_tracker')



class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from task_tracker import main
        directory, filename = split(__file__)
        app = main({}, **{
            'pyramid.includes': '\npyramid_jinja2',
            'sqlalchemy.url': 'sqlite:///%s.sqlite' % directory
        })
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_story_list(self):
        response = self.testapp.get('/', status=200)
        self.failUnless('Task tracker' in response.body)

    def test_add_story(self):
        response = self.testapp.get('/new/story', status=200)
        self.failUnless('Title' in response.body)

    def test_view_story(self):
        response = self.testapp.get('/story/1', status=200)
        self.failUnless('Any user can see list of' in response.body)

    def test_edit_story(self):
        response = self.testapp.get('/story/1/edit', status=200)
        self.failUnless('Any user can see list of' in response.body)

    def test_view_task(self):
        response = self.testapp.get('/story/1/task/1', status=200)
        self.failUnless('Should read Pyramid standard library' in response.body)

    def test_edit_task(self):
        response = self.testapp.get('/story/1/task/1', status=200)
        self.failUnless('Should read Pyramid standard library' in response.body)

    def test_stats(self):
        response = self.testapp.get('/stats', status=200)
        self.failUnless('View stats' in response.body)

    def test_login(self):
        response = self.testapp.get('/login', status=200)
        self.failUnless('Username' in response.body)

    def test_logout(self):
        response = self.testapp.get('/logout', status=302)
