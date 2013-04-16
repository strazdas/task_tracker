# coding: utf-8
import os
import sys
import transaction
import datetime

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from ..models import (
    DBSession,
    Base,
    User,
    Story,
    Task,
    TimeSpent,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        user = User(username="albertas", password="admin")
        DBSession.add(user)
        user = User(username="aurimas", password="admin")
        DBSession.add(user)
        story = Story(title=u"'Task tracker' homework",
                description=u"""\
Any user can see list of ``stories`.
Authenticated users can create new `stories`.
Each `story` in the list has a link to its details.
Any user can see `story` detail page, where details, including
    list of `tasks` are displayed.
Authenticated users can update the details or add new `tasks`.
Each task in the `tasks` list has a link to its details.
Any user can see `tasks` details.
Authenticated users can update `task` description and log time spent.

Any user can review cumulative statistics of any registered user.
Cumulative statistcs consists of total estimated time and total time spent for
specified user.`""",
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
