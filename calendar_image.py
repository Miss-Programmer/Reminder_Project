from calendar_view.calendar import Calendar
from calendar_view.core import data
from calendar_view.core.event import Event
import file
from datetime import datetime, timedelta


def week_calendar(username, period):
    config = data.CalendarConfig(
        lang='en',
        title=f"{username}'s Tasks",
        dates=period,
        show_year=True,
        mode='working_hours',
        legend=False,
    )
    events = []
    user_tasks = file.user_row('tasks.csv', user_name=username)
    for task in user_tasks:
        daytime = task['due_time'].split(" ")
        day = daytime[0]
        start = datetime.strftime(datetime.strptime(daytime[1], '%H:%M:%S'), '%H:%M')
        end = datetime.strftime(datetime.strptime(daytime[1], '%H:%M:%S') + timedelta(hours=1), '%H:%M')
        events.append(Event(task['title'], day=day, start=start, end=end))

    data.validate_config(config)
    data.validate_events(events, config)

    calendar = Calendar.build(config)
    calendar.add_events(events)
    calendar.save(f"{username}_tasks.png")

