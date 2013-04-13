from pyramid.response import Response
from pyramid.view import view_config
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    MyModel,
    User,
    Story,
    )
from .forms import StorySchema


@view_config(route_name='story_list', renderer='templates/story_list.pt')
def story_list(request):
    stories = [4,6,3]   # Story list STUB
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        one = None
    return {'one': one, 'stories': stories}



@view_config(route_name='add_story', renderer='templates/add_story.jinja2')
def add_story(request):
    form = Form(request, schema=StorySchema())

    if form.validate():
        obj = form.bind(Story())
        DBSession.add(obj)
        DBSession.flush()
        return HTTPFound(location='/story/%s' % obj.id)
    return {
        'renderer': FormRenderer(form),
        'request': request,
        'form': form,
        'erorrs': form.errors
    }


@view_config(route_name='view_story', renderer='templates/story.jinja2')
def view_story(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).filter(Story.id==story_id).first()
    return {'story': story, 'story_id': story_id }


@view_config(route_name='edit_story', renderer='templates/message.pt')
def edit_story(request):
    story_id = request.matchdict['story_id']
    story = DBSession.query(Story).filter(Story.id==story_id).first()
    form = Form(request, schema=StorySchema, obj=item)
    return {'message': 'Editing story %s' % story_id}


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
