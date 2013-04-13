from formencode import Schema, validators
from pyramid_simpleform import Form

class StorySchema(Schema):
    allow_extra_fields = True
    filter_extra_fields = True

    title = validators.UnicodeString(max=255)
