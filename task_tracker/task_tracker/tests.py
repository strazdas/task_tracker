# coding: utf-8
import unittest
import transaction
from os.path import split
import datetime

from pyramid import testing
from sqlalchemy import create_engine

from .models import (
    DBSession,
    Base,
    User,
    Story,
    Task,
    TimeSpent,
    )


class TestViews(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        engine = create_engine('sqlite://')
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            user = User(username="albertas", password="admin")
            DBSession.add(user)
            user = User(username="aurimas", password="admin")
            DBSession.add(user)
            story = Story(title=u"'Task tracker' homework",
                    description=u"""Any user can see list of ``stories`.""",
            estimated = '10 0:00',
            created = datetime.datetime(2013, 4, 14, 11, 24, 30, 354409),
            created_by_id = 1,
                    )
            DBSession.add(story)
            task = Task(title=u"Read documentation and get to know framework",
                    description="""Should read Pyramid standard library, write some \
    'hello worlds'.""",
                    estimated = "3 0:00",
                    created = datetime.datetime(2013, 4, 14, 11, 30, 20, 834472),
                    assigned_id = 1,
                    story_id = 1,
                    )
            DBSession.add(task)
            task = Task(title=u"Implement 'Task tracker' requirements",
                    description="""Full 'Task tracker' feature implementation.""",
                    estimated = "7 0:00",
                    created = datetime.datetime(2013, 4, 14, 11, 30, 40, 834472),
                    assigned_id = 1,
                    story_id = 1,
                    )
            DBSession.add(TimeSpent(duration=u"12:00", task_id=1))
            DBSession.add(TimeSpent(duration=u"14:00", task_id=1))
            DBSession.add(TimeSpent(duration=u"5:00", task_id=2))
            DBSession.add(TimeSpent(duration=u"8:00", task_id=2))

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_story_list_view(self):
        from .views import story_list
        request = testing.DummyRequest()
        info = story_list(request)
        self.failUnless(len(info['stories']) == 1)

    def test_add_story_view_post(self):
        from .views import add_story
        from pyramid.security import remember
        # TODO: Unable to login user..
        # headers = remember(testing.DummyRequest(), 1)
        request = testing.DummyRequest(post={
            'title': 'Test story',
            'estimated': '1 11:30',
            'description': 'Description for test story'})
        # info = add_story(request)

    def test_stats_post(self):
        from .views import stats
        request = testing.DummyRequest(post={
            'user_id': 1,
        })
        info = stats(request)
        self.failUnless(info['total_time_estimated'] == '3 days, 0:00:00')
        self.failUnless(info['total_time_spent'] == '1 day, 2:00:00')


class FunctionalTests(unittest.TestCase):
    def setUp(self):
        from task_tracker import main
        app = main({}, **{
            'pyramid.includes': '\npyramid_jinja2',
            'sqlalchemy.url': 'sqlite:///%s.sqlite' % split(__file__)[0]
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

    def test_add_time_spent(self):
        response = self.testapp.post('/story/1/task/1', {'duration': '1 0:00'})
        self.failUnless(response.status_int == 302)

    def test_edit_task(self):
        response = self.testapp.get('/story/1/task/1', status=200)
        self.failUnless('Should read Pyramid standard library' in response.body)

    def test_stats(self):
        response = self.testapp.get('/stats', status=200)
        self.failUnless('Choose developer' in response.body)

    def test_stats_post(self):
        response = self.testapp.post('/stats', {'user_id': 1})
        self.failUnless('days' in response.body)

    def test_login(self):
        response = self.testapp.get('/login', status=200)
        self.failUnless('Username' in response.body)

    def test_logout(self):
        response = self.testapp.get('/logout', status=302)
