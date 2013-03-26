import json, httplib, urllib2, sys, re, datetime

band_colors = [ 
    '\033[31m', 
    '\033[31m', 
    '\033[31m', 
    '\033[31m',
    '\033[31m', 
    '\033[31m', 
    '\033[31m', 
    '\033[31m', 
    '\033[33m', 
    '\033[33m', 
    '\033[33m', 
    '\033[33m', 
    '\033[33m', 
    '\033[33m', 
    '\033[32m', 
    '\033[32m', 
    '\033[32m', 
    '\033[32m', 
    '\033[32m', 
    '\033[32m',
    '\033[30m',
    '\033[32m'
]

access_token = sys.argv[1]
if access_token == None:
    print('Access token was NULL')
    sys.exit(1)

root_url = 'https://api.nike.com/me/sport'
sport_url =  root_url + '?access_token=' + access_token
activity_url = root_url + '/activities?access_token=' + access_token + '&count=2'

current_streak = 0
total_fuel = 0
todays_fuel = 0
last_sync = 0
daily_goal = 0
total_dots = 19

req = urllib2.Request(sport_url)
req.add_header("appid", "fuelband")
req.add_header("Accept", "application/json")

#grab data
try:
    handle = urllib2.urlopen(req)
except IOError, e:
    # here we shouldn't fail if the username/password is right
    print "It looks like the oauth token was wrong"
    sys.exit(1)

data = json.load(handle)
summaries = data['summaries']
records = []

for summary in summaries:
    if summary['experienceType'] == 'FUELBAND':
        records = summary['records']

for record in records:
    if record['recordType'] == 'LIFETIMEFUEL':
        total_fuel = record['recordValue']

    if record['recordType'] == 'CURRENTSTREAK':
        current_streak = record['recordValue']

    if record['recordType'] == 'DAILYGOALTARGETVALUE':
        daily_goal = float(record['recordValue'])


req = urllib2.Request(activity_url)
req.add_header("appid", "fuelband")
req.add_header("Accept", "application/json")

#grab data
try:
    handle = urllib2.urlopen(req)
except IOError, e:
    print "It looks like the oauth token was wrong"
    sys.exit(1)

data = json.load(handle)

last_data = data['data'][0]
last_sync = datetime.datetime(*map(int, re.split('[^\d]', last_data['startTime'])[:-1]))
current_date = current_date = datetime.datetime.now()

if last_sync.date() >= current_date.date():
    todays_fuel = last_data['metricSummary']['fuel']

    #print('calories: ' + str(last_data['calories']))
    #print('distance: ' + str(last_data['distance']))

    goal_gap = int(((float(todays_fuel) / daily_goal) * 100) / 5)

    for index in range(total_dots):
        if index < goal_gap:
            sys.stdout.write(band_colors[index] + ".   ")
        else:
            sys.stdout.write("  ")

    sys.stdout.write(band_colors[21] + ".   ") #far right dot.  I tried to make it blink with the color '\033[32;5m' but GeekTools wasn't having it
else:
  print('no sync today')

if total_fuel > 1000000:
    total_fuel = str(round(float(total_fuel) / float(1000000), 2)) + 'M'
else:
    total_fuel = str(round(float(total_fuel) / float(1000), 2)) + 'K'

print('\033[37m' + '\n\nNIKEFUEL: ' + str(todays_fuel) + '\t\t   GOAL: ' + str(int(daily_goal)))
print ('\ntotal:' +  total_fuel + '\t\t\tstreak: ' + str(current_streak) + ' days')
