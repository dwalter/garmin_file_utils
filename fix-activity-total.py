"""
### Convert .fit to .csv
[link](https://developer.garmin.com/fit/fitcsvtool/osx/)
```bash
java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar ~/Downloads/activity.fit
```

### Convert .csv (from .fit) to .fit
[link](https://developer.garmin.com/fit/fitcsvtool/editing-files/)
```bash
java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar -c ./activity.csv ./activity.fit
```
"""
import os
import csv

# TODO FIXME
# https://www.strava.com/activities/1392061412/overview

PREFIX = "mar22_2024"
TOTAL_MILES = 4.0 # miles

fit2csv_command = f"java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar {PREFIX}.fit"
os.system(fit2csv_command)

EPSILON = 1e-6
METERS_PER_MILE = 1611.0 # increased to account for the strava tax
set_lap_dist = METERS_PER_MILE
ROOT_DIR = "." # "~/Downloads"
CSV_FILENAME = f"{PREFIX}.csv"
FIXED_PREFIX = f"fixed-{PREFIX}"
AFTER_CSV_FILENAME = f"{FIXED_PREFIX}.csv"
AFTER_FIT_FILENAME = f"{FIXED_PREFIX}.fit"


rows = []
laps = [0]
last_dist = 0
with open(f"{ROOT_DIR}/{CSV_FILENAME}", newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[6] == "distance" and row[8] == "m":
            last_dist = row[7]

        if row[0] == "Data" and row[2] == "lap":
            laps.append(last_dist)

        rows.append(row)

print(f"laps: {laps}")

multiplier = TOTAL_MILES * METERS_PER_MILE / float(last_dist)

prev_dist_proc = 0
total_prev_laps_proc = 0
for ir, row in enumerate(rows):
    if row[6] == "distance" and row[8] == "m":

        dist = float(row[7])
        dist_proc = dist * multiplier
        prev_dist_proc = dist_proc

        rows[ir][7] = str(dist_proc)
        print(f"before: {dist}, after: {dist_proc}")

    if row[0] == "Data" and row[2] == "lap":
        lap_dist_proc = total_prev_laps_proc - prev_dist_proc
        rows[ir][16] = lap_dist_proc
        total_prev_laps_proc = prev_dist_proc

    if row[0] == "Data" and row[2] == "session" and row[15] == "total_distance":
        rows[ir][16] = TOTAL_MILES * METERS_PER_MILE


with open(f"{ROOT_DIR}/{AFTER_CSV_FILENAME}", mode="w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)


csv_fit_command = f"java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar -c ./{AFTER_CSV_FILENAME} ./{AFTER_FIT_FILENAME}"
os.system(csv_fit_command)
