import datetime
import calendar
import matplotlib.pyplot as plt
import numpy as np

start = datetime.date(2019,1,1)
end   = datetime.date(2020,1,1)
def date_period(start, end):
    return [start+datetime.timedelta(days=dd) for dd in range((end-start).days)]

period = date_period(start, end)

def get_month_starts(period):
    return [d for d in period if d.day==1]

def get_week_starts(period):
    return [d for d in period if d.weekday()==0]

N = len(period)  # number of days in the circle (year)
R = 10  # radius of the circle
angle_increment = 2*np.pi/N  # angle increment for each day
fs = 10  # figure size
fig = plt.figure(figsize=(fs, fs))
plt.polar()
ax = plt.gca()
ax.set_theta_zero_location("N")
ax.set_theta_direction("clockwise")
ax.grid("off")
ax.axis("off")

font = {
    'size'   : 11,
    'family' : 'monospace',
    }
plt.rc('font', **font)

#%%
# colours
colours = ['#ffffff', '#f0f0f0', '#d9d9d9', '#bdbdbd', '#969696', '#737373',
           '#525252', '#252525', '#000000']

# formatting info
f_daylines = dict(lw=0.5, color=colours[-5], zorder=1)
f_weeklines = dict(lw=1, color=colours[-3], zorder=2)
f_monthlines = dict(lw=2, color=colours[-2], zorder=3)
f_startend = dict(lw=3, color=colours[-1], zorder=4)
f_title = dict(fontsize=30)
f_middle = dict(color="w", zorder=5)
f_event = dict(color=colours[-5], zorder=0)
f_event_text = dict(color=colours[-4], zorder=6)


# plot the year (or maximum increment)
title = 2019
plt.title(title, y=1.08, **f_title)

# plot the vertical start/end line
plt.plot([0, 0], [0, R], **f_startend)

# plot the day lines
for day in range(N):

    theta = day*angle_increment  # angle of the line at the start of this day
    plt.plot([theta, theta], [0, R], **f_daylines)
    # find the date of each day
    delta = datetime.timedelta(days=day)
    date = start+delta
    weekday = calendar.day_abbr[date.weekday()]
    text = date.isoformat()+" "+weekday
    """
    # diagnostics -- plot the full date of each day
    plt.text(theta+angle_increment/2, R+2, text,
             horizontalalignment="center",
             verticalalignment="center",
             rotation=-np.rad2deg(theta+angle_increment/2)+90,
             color="0.75",
             )
    #"""

# plot the month lines
for month in get_month_starts(period):
    month_name = calendar.month_abbr[month.month].upper()
    days = (month-start).days
    theta = days*angle_increment
    plt.plot([theta, theta], [0, R], **f_monthlines)
    plt.text(theta+angle_increment/2, R+1, str(month_name),
             rotation=-np.rad2deg(theta+angle_increment/2)+90,
             verticalalignment="center", horizontalalignment="center")

# plot the week lines
for week in get_week_starts(period):
    days = (week-start).days
    theta = days*angle_increment
    plt.plot([theta, theta], [0, R], **f_weeklines)

    # plot the day number
    plt.text(theta+angle_increment/2, R+.3, week.day,
             horizontalalignment="center",
             verticalalignment="center",
             rotation=-np.rad2deg(theta+angle_increment/2)+90,
             color="k",
             )

# plot any special dates
birthdays = {"Dad birthday": datetime.date(1,6,7),
             "Mum birthday": datetime.date(1,8,9),
             }

# these are in tuples so they can be unpacked, supporting multi-day events
fixed_public_holidays = {
                         "New year's day": (datetime.date(1,1,1),),
                         "Christmas & Boxing day": (datetime.date(1,12,25),
                                                     datetime.date(1,12,26)),
                         "Summer bank holiday": (datetime.date(2017,8,26),),
                         "Spring bank holiday": (datetime.date(2017,5,27),),
                         "Early may bank holiday": (datetime.date(2017,5,6),),
                         "Easter Monday": (datetime.date(2017,4,22),),
                         "Good Friday": (datetime.date(2017,4,19),),
                         }

def fill_event(event_s, event_e=None, name=None, recurring=False):

    print("\nconsidering event {}".format(name))
    # ignore the year attached to the recurring event. Update it to match start
    if recurring is True:
        print("recurring event. Ignoring the year.")
        event_s = event_s.replace(year=start.year)

    # check that the event occurs in our start/end bounds
    if event_e is not None:  # for multi-day events
        print("multi-day event.")
        if recurring is True:  # recurring event ignore year
            print("recurring event. Ignoring the year.")
            event_e = event_e.replace(year=start.year)

        print("start={}, end={}".format(event_s,event_e))
        if event_s > end or event_e < start:
            raise Exception("event_s > end or event_e < start, so the event "
                            "must lie outside of the period. It is not a "
                            "recurring event, so you must have made a mistake.")
        if event_s > event_e:
            raise Exception("event start after event end!")
        if event_s < start:  # if the event starts before the period
            print("event starts before period")
            event_s = start  # set the event start to period start
            print("so I've set event start = period start")
        if event_e > end:  # if the event ends after period
            print("event ends after period")
            event_e = end  # set the event end to period end

        # calculate end angle (after modifying end date if necessary)
        angle_end = ((event_e-start).days+1)*angle_increment
        n_pts = (event_e-event_s).days+1

    else:  # for single-day events
        if event_s >= start and event_s <= end:  # if event in period
            # calculate end angle as 1 increment after start angle
            angle_end = ((event_s-start).days+1)*angle_increment
            n_pts=2
            print("single-day event in range")
        else:  # if the event is out of range
            print("single-day event out of range:\n"
                  "event_s = {}; start = {}; end = {}".format(event_s,start,end))
            return None  # ignore this event and exit

    # always work out start angle
    angle_start = (event_s-start).days*angle_increment

    print("angle_start, angle_end = {}, {}".format(angle_start, angle_end))
    print("number of points = ", n_pts)

    # generate the shape of the event and plot it
    theta = list(np.linspace(angle_start, angle_end, n_pts))+[0]
    r = list(np.ones(n_pts)*(R-.5))+[0]
    ax.fill(theta,r,fill=True,**f_event)
    print("theta range = ", theta)
    print("r range = ", r)

    if name is not None:  # plot the name if one was passed
        # pad the string with spaces
        name = name.rjust(30, " ")
        plt.text(angle_start+angle_increment/2, R-5, name,
            horizontalalignment="center",
            verticalalignment="center",
            rotation=-np.rad2deg(angle_start+angle_increment/2)+90,
            **f_event_text)

for name, day in birthdays.items():
    fill_event(day, name=name, recurring=True)

for name, day in fixed_public_holidays.items():
    fill_event(*day, name=name, recurring=True)

# fill in the middle
theta = np.linspace(0, 2*np.pi, 100)
r = np.ones(100)*(R-1)
ax.fill(theta,r,fill=True,**f_middle)

plt.tight_layout()
fig.savefig("circular_calendar.pdf")
fig.savefig("circular_calendar.png")
