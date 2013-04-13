from pyramid.response import Response
from pyramid.view import view_config
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError
from datetime import datetime

from .models import (
    DBSession,
    User,
    Story,
    Task,
    )
from .forms import StorySchema


@view_config(route_name='story_list', renderer='templates/story_list.jinja2')
def story_list(request):
    stories = DBSession.query(Story).order_by('created').limit(20).all()
    return {'stories': stories}


@view_config(route_name='add_story', renderer='templates/add_story.jinja2')
def add_story(request):
    form = Form(request, schema=StorySchema())
    if form.validate():
        obj = form.bind(Story())
        obj.created = datetime.now()
        DBSession.add(obj)
        DBSession.flush()
        return HTTPFound(location='/story/%s' % obj.id)
    return {
        'renderer': FormRenderer(form),
        'form': form,
    }


@view_config(route_name='view_story', renderer='templates/story.jinja2')
def view_story(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).filter(Story.id==story_id).first()
    tasks = DBSession.query(Task).filter(story_id==story_id).all()
    return {'story': story, 'story_id': story_id, 'tasks': tasks}


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
    }


@view_config(route_name='add_task', renderer='templates/message.pt')
def add_task(request):
    story_id = request.matchdict['story_id']
    return {'message': 'Creating new task for story %s' % story_id}


@view_config(route_name='view_task', renderer='templates/message.pt')
def view_task(request):
    story_id = request.matchdict['story_id']
    task_id = request.matchdict['task_id']
    return {'message': 'View task %s of story %s' % (task_id, story_id)}


@view_config(route_name='edit_task', renderer='templates/message.pt')
def edit_task(request):
    story_id = request.matchdict['story_id']
    task_id = request.matchdict['task_id']
    return {'message': 'Edit task %s of story %s' % (task_id, story_id)}


@view_config(route_name='stats', renderer='templates/message.pt')
def stats(request):
    return {'message': 'stats'}


@view_config(route_name='view_stats', renderer='templates/message.pt')
def view_stats(request):
    username = request.matchdict['username']
    return {'message': 'Viewing stats for user %s' % username}
