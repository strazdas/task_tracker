from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    session_factory = UnencryptedCookieSessionFactoryConfig('lphfwnviqzivz')
    Base.metadata.bind = engine
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('story_list', '/')
    config.add_route('add_story', '/new/story')
    config.add_route('view_story', '/story/{story_id}')
    config.add_route('edit_story', '/story/{story_id}/edit')
    config.add_route('view_task', '/story/{story_id}/task/{task_id}')
    config.add_route('edit_task', '/story/{story_id}/task/{task_id}/edit')
    config.add_route('stats', '/stats')
    config.add_route('view_stats', '/stats/{username}')
    config.scan()
    return config.make_wsgi_app()
