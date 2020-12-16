from calendar import HTMLCalendar, day_name
from .models import Event
from itertools import chain

class EventCalendar(HTMLCalendar):
    def __init__(self, events=None):
        super(EventCalendar, self).__init__()
        self.events = events

    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(EventCalendar, self).__init__()

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        weekday_name = day_name[int(weekday)]
        events_from_day = events.filter(event_date__day=day)
        events_from_weekday = events.filter(days__choice=weekday_name).exclude(event_date__day=day)
        all_events = list(chain(events_from_day, events_from_weekday))
        events_html = "<ul>"
        for event in all_events:
            events_html += "<li><a href= " + str(event.get_detail_url()) + ">" + "<b>" + event.event_name + "</b><br>" + self.formattime(event.event_start_time) + " - " + self.formattime(event.event_end_time) + "</a></li>"
        events_html += "</ul>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td><span class="%s">%d%s</span></td>' % (self.cssclasses[weekday], day, events_html)

    def formattime(self, time):
        time = str(time)[0: 5]
        if time[0] == '0':
            time = time[1: 5] + " AM"
        elif time[0] == '2':
            time = str(int(time[0: 2]) - 12) + time[2: 5] + " PM"
        else:
            if int(time[1]) < 2:
                time += " AM"
            elif int(time[1]) == 2:
                time += " PM"
            else:
                time = str(int(time[0:2]) - 12) + time[2:5] + " PM"
        return time

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, user, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(event_date__month=themonth
                                      ).filter(event_date__year=theyear
                                    ).filter(user=user)

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="calendar">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)