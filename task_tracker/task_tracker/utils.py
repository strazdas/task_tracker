from formencode import FancyValidator, Invalid
from datetime import datetime as dt, timedelta


def sum_time_spent(times_spent):
    def parse_time(time):
        days = 0
        if len(time.split()) > 1:
            days, time = time.split()
        time = dt.strptime(time, '%H:%M') - dt(1900, 1, 1)
        return timedelta(int(days)) + time

    total_time_spent = timedelta(0)
    for time_spent in times_spent:
        total_time_spent += parse_time(time_spent.duration)
    return total_time_spent


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
