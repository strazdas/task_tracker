install:
	# ../bin is created by ``$ virtualenv --no-site-packages env``
	../bin/easy_install pyramid nose coverage
	../bin/python setup.py develop

run:
	../bin/pserve development.ini --reload

db:
	../bin/initialize_task_tracker_db development.ini

test:
	../bin/python setup.py test -q

coverage:
	../bin/nosetests --cover-package=task_tracker --cover-erase --with-coverage

