from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy.exc import DBAPIError
from datetime import datetime

from .models import (
    DBSession,
    User,
    Story,
    Task,
    TimeSpent,
    )
from .forms import StorySchema, TaskSchema, TimeSpentSchema, UserSchema
from .utils import sum_time_spent


def get_user(request):
    user_id = authenticated_userid(request)
    user = None
    if user_id:
        user = DBSession.query(User).get(user_id)
    return user


@view_config(route_name='story_list', renderer='templates/story_list.jinja2')
def story_list(request):
    stories = DBSession.query(Story).order_by('created').limit(20).all()
    return {
        'stories': stories,
        'user': get_user(request),
    }


@view_config(route_name='add_story', renderer='templates/add_story.jinja2')
def add_story(request):
    form = Form(request, schema=StorySchema())
    user = get_user(request)
    if form.validate():
        obj = form.bind(Story())
        obj.created = datetime.now()
        obj.created_by_id = user.id
        obj.created_by = user
        DBSession.add(obj)
        DBSession.flush()
        return HTTPFound(location='/story/%s' % obj.id)
    return {
        'renderer': FormRenderer(form),
        'form': form,
        'user': user,
    }


@view_config(route_name='view_story', renderer='templates/story.jinja2')
def view_story(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).filter(Story.id==story_id).first()
    tasks = DBSession.query(Task).filter(Task.story_id==story_id).all()
    task_form = Form(request, schema=TaskSchema())
    users = DBSession.query(User).all()
    user_options = [(user.id, user.username) for user in users]
    if request.method == 'POST' and task_form.validate():
        task = task_form.bind(Task())
        task.story = story
        task.story_id = story_id
        task.created = datetime.now()
        DBSession.add(task)
        return HTTPFound(location='/story/%s' % story_id)
    return {
        'story': story,
        'story_id': story_id,
        'tasks': tasks,
        'renderer': FormRenderer(task_form),
        'form': task_form,
        'user': get_user(request),
        'users': user_options,
    }


@view_config(route_name='edit_story', renderer='templates/edit_story.jinja2')
def edit_story(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).get(story_id)
    form = Form(request, schema=StorySchema(), obj=story)
    if request.method == 'POST' and form.validate():
        story = form.bind(story)
        return HTTPFound(location='/story/%s' % story.id)
    return {
        'renderer': FormRenderer(form),
        'form': form,
        'user': get_user(request),
    }


@view_config(route_name='view_task', renderer='templates/task.jinja2')
def view_task(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).get(story_id)
    task_id = request.matchdict['task_id']
    task = DBSession.query(Task).get(task_id)
    times_spent = DBSession.query(TimeSpent).filter(
                                        TimeSpent.task_id==task_id).all()
    form = Form(request, schema=TimeSpentSchema())

    if request.method == 'POST' and form.validate():
        time_spent = form.bind(TimeSpent())
        time_spent.task_id = task_id
        time_spent.task = task
        DBSession.add(time_spent)
        DBSession.flush()
        return HTTPFound(location='/story/%s/task/%s' % (story_id, task_id))
    return {
        'story': story,
        'story_id': story_id,
        'task': task,
        'task_id': task_id,
        'times_spent': times_spent,
        'renderer': FormRenderer(form),
        'form': form,
        'total_time_spent': str(sum_time_spent(times_spent)),
        'user': get_user(request),
    }


@view_config(route_name='edit_task', renderer='templates/edit_task.jinja2')
def edit_task(request):
    story_id = request.matchdict['story_id']
    task_id = request.matchdict['task_id']
    task = DBSession.query(Task).get(task_id)
    form = Form(request, schema=TaskSchema(), obj=task)
    if request.method == 'POST' and form.validate():
        task = form.bind(task)
        return HTTPFound(location='/story/%s/task/%s' % (story_id, task_id))
    return {
        'story_id': story_id,
        'task_id': task_id,
        'renderer': FormRenderer(form),
        'form': form,
        'user': get_user(request),
    }


@view_config(route_name='stats', renderer='templates/message.pt')
def stats(request):
    return {
        'message': 'stats',
        'user': get_user(request),
    }


@view_config(route_name='view_stats', renderer='templates/message.pt')
def view_stats(request):
    username = request.matchdict['username']
    return {
        'message': 'Viewing stats for user %s' % username,
        'user': get_user(request),
    }

@view_config(route_name='login', renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    message = None
    form = Form(request, schema=UserSchema())
    if request.method == 'POST' and form.validate():
        username = request.params['username']
        password = request.params['password']
        password_again = request.params['password_again']

        if bool(password_again):
            if password == password_again:
                user = form.bind(User())
                DBSession.add(user)
                DBSession.flush()
                user_id = user.id
                headers = remember(request, user.id)
                return HTTPFound(location='/', headers=headers)
            else:
                message = 'Passwords do not match.'
        else:
            user = DBSession.query(User).filter(User.username==username).first()
            if user and user.password == password:
                headers = remember(request, user.id)
                return HTTPFound(location='/', headers=headers)
            else:
                message = 'Username or password is incorrect.'
    return {
        'message': message,
        'form': form,
        'renderer': FormRenderer(form),
        'user': get_user(request),
    }

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)
