from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('story_details', '/story/{story_id:\d+}')
    config.add_route('task_details', '/story/{story_id:\d+}/task/{task_id:\d+}')
    config.add_route('stats', '/stats')
    config.scan()
    return config.make_wsgi_app()
