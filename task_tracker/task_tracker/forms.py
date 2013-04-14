from formencode import Schema, validators, FancyValidator, Invalid
from pyramid_simpleform import Form

from .utils import DurationValidator


class StorySchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    title = validators.UnicodeString(max=255, min=1)
    description= validators.UnicodeString()
    estimated = DurationValidator()


class TaskSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    title = validators.UnicodeString(max=255, min=1)
    description= validators.UnicodeString()
    estimated = DurationValidator()


class TimeSpentSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = False

    duration = DurationValidator()


class UserSchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = False

    username = validators.UnicodeString(max=255, min=1)
    password = validators.UnicodeString(max=255, min=1)
    password_again = validators.UnicodeString(max=255, nullable=True)
