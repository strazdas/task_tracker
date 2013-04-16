import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'jinja2',
    'webtest',
    ]

setup(name='task_tracker',
      version='0.0',
      description='task_tracker',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid task time',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='task_tracker',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = task_tracker:main
      [console_scripts]
      initialize_task_tracker_db = task_tracker.scripts.initializedb:main
      """,
      )
