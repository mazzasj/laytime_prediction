# %%
import csv
from datetime import datetime, timedelta

# Constants
RATE = 4.5  # doughs per hour
current_time = datetime(2023, 8, 16, 21, 5) # datetime.now() yyyy:mm:dd hh:mm


# %%

# Read the times from the CSV file https://carypi.us.kellogg.com/PIVision/#/Displays/324/Mixer-Complete
doughsage = []

with open('dough_times.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        timestamp = datetime.strptime(row[0], '%m/%d/%y %H:%M') #lowercase 'y' for 2 digit year
        age = (current_time - timestamp).total_seconds() / 3600
        # Consider all data entries in the csv as relevant (please filter ranges in the CSV file itself)
        doughsage.append(age)
    
LT = round(doughsage[0],2)
print(f"Current laytime is {LT} hours")         


# %%
print(f"{len(doughsage)} tubs") # number of tubs

# %%
mins_tub = 60 / RATE # minutes per tub

# Compute dump time of each tub based on consumption rate
laytime_predictions = []
laytime = []
LT_calc = []
LT_time = []
for i in range(len(doughsage)):
    tub_time = current_time + (timedelta(minutes = mins_tub) * i) # time when it will dump

    dump_time = tub_time - current_time # in how many minutes it will dump
    laytime.append(dump_time.total_seconds() + (doughsage[i]* 60 * 60)) # divide by 60 seconds twice to get laytime
    laytime_predictions.append(laytime[i] / 60 / 60)
    LT_calc.append(round(laytime_predictions.pop(0),2))
    LT_time.append(timedelta(minutes=mins_tub * i) + current_time)
    #if LT_calc[-1] < 23 or LT_calc[-1] > 27:
        #print(LT_calc[-1],LT_time[-1])
    

# %%
# Print the laytime predictions
eoh = current_time #end of hour
eoh += timedelta(hours=1)
eoh = datetime(eoh.year, eoh.month, eoh.day, eoh.hour, 0)
for i in range(len(LT_time)):
    if LT_time[i].hour == eoh.hour:
        tub0_from_eoh = eoh - LT_time[i-1]
        tub1_from_eoh = LT_time[i] - eoh
        total_distance_eoh = tub0_from_eoh + tub1_from_eoh
        LT_this_hour = (tub0_from_eoh / total_distance_eoh) * LT_calc[i]
        LT_this_hour += (1 - (tub0_from_eoh / total_distance_eoh)) * LT_calc[i-1]
        LT_this_hour = round(LT_this_hour,2)
        print(f"At {eoh.hour}:00, expected laytime will be {LT_this_hour} hours")
        eoh = datetime(eoh.year, eoh.month, eoh.day, eoh.hour, 0) + timedelta(hours=1)



