from formencode import Schema, validators, FancyValidator, Invalid
from pyramid_simpleform import Form
from datetime import datetime as dt, timedelta


class DurationValidator(FancyValidator):
    error_message = 'Use one of the formats: "%Days %H:%M", "%H", "%H:%M";'
    time_formats = ['%H', '%H:%M', '%H:%M:%S']
    no_time = dt(1900, 1, 1)

    def _to_python(self, value, state):
        days = time = None
        value = value.strip()
        if len(value.split()) > 1:
            days, value = value.split()

        for format_ in self.time_formats:
            try:
                time = dt.strptime(value, format_) - self.no_time
                break
            except ValueError:
                continue
        if not time:
            return None

        hours = time.seconds / 3600
        minutes = time.seconds % 3600 / 60
        if days:
            return '%d %d:%02u' % (days, hours, minutes)
        return '%d:%02u' % (hours, minutes)

    def validate_python(self, value, state):
        if not value:
            raise Invalid(self.error_message, value, state)

        value = value.strip()

        if len(value.split()) > 1:
            days, value = value.split()
            try:
                int(days)
            except ValueError:
                raise Invalid(self.error_message, value, state)

        parsed_time = None
        for format_ in self.time_formats:
            try:
                parsed_time = str(dt.strptime(value, format_) - self.no_time)
                break
            except ValueError:
                continue
        if not parsed_time:
            raise Invalid(self.error_message, value, state)



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
