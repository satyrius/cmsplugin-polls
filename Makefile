export PYTHONPATH := $(CURDIR):$(CURDIR)/tests
export DJANGO_SETTINGS_MODULE := settings_17

south_migrations:
	DJANGO_SETTINGS_MODULE=settings_south \
	source .tox/django-1.6/bin/activate && \
	django-admin.py schemamigration cmsplugin_polls --auto || true

migrations:
	source .tox/django-1.7/bin/activate && \
	django-admin.py makemigrations cmsplugin_polls
