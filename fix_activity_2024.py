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

# https://www.strava.com/activities/1392061412/overview


class FixActivity:
    def __init__(self):
        self.PREFIX = "mar22_2024"
        # self.TOTAL_MILES = 8.0 # miles

        fit2csv_command = f"java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar {self.PREFIX}.fit"
        os.system(fit2csv_command)

        self.EPSILON = 1e-6
        self.METERS_PER_MILE = 1611.0
        self.set_lap_dist = self.METERS_PER_MILE
        self.ROOT_DIR = "." # "~/Downloads"
        self.CSV_FILENAME = f"{self.PREFIX}.csv"
        self.FIXED_PREFIX = f"fixed-{self.PREFIX}"
        self.AFTER_CSV_FILENAME = f"{self.FIXED_PREFIX}.csv"
        self.AFTER_FIT_FILENAME = f"{self.FIXED_PREFIX}.fit"

    def get_rows_laps_and_last_dist(self):
        rows = []
        laps = [0]
        total_dist = 0
        # final_dist = None
        with open(f"{self.ROOT_DIR}/{self.CSV_FILENAME}", newline='') as f:
            reader = csv.reader(f)
            for row in reader:

                rows.append(row)

                if "total_distance" not in row:
                    continue

                # get the index of the "total_distance"column:
                total_dist_i = row.index("total_distance")
                total_dist_data_i = total_dist_i + 1
                total_dist_data = row[total_dist_data_i]

                if float(total_dist_data) > 50 and float(total_dist_data) < 2000:
                    total_dist += float(total_dist_data)
                    laps.append(total_dist)

                # elif total_dist_data > 2000:
                #     final_dist = total_dist_data

        return rows, laps#, final_dist

    def get_rows_proc(self):
        # rows, laps, last_dist = self.get_rows_laps_and_last_dist()
        rows, laps = self.get_rows_laps_and_last_dist()

        print(f"laps: {laps}")

        i_lap = 1
        i_lap_counting = 1
        prev_dist = 0
        total_prev_laps = 0
        total_prev_laps_adj = 0

        total_session_row = None
        for ir, row in enumerate(rows):
            if row[6] == "distance" and row[8] == "m":

                lap_dist = float(laps[i_lap_counting])
                dist = float(row[7])

                # increment the lap
                if dist > lap_dist and lap_dist != laps[-1]:
                    i_lap_counting += 1
                    lap_dist = float(laps[i_lap_counting])
                    total_prev_laps = prev_dist
                    total_prev_laps_adj += self.set_lap_dist

                lap_net_dist = (lap_dist - total_prev_laps) + self.EPSILON
                prev_dist = dist
                net_dist = dist - total_prev_laps

                net_dist_adjusted = net_dist * self.set_lap_dist / lap_net_dist
                dist_adjusted = net_dist_adjusted + total_prev_laps_adj

                rows_ir = rows[ir]
                rows_ir[7] = str(dist_adjusted)
                print(f"before: {dist}, after: {dist_adjusted}")

            if row[0] == "Data" and row[2] == "lap":
                # total_dist = row[16]
                # total_prev_laps = prev_dist
                # total_prev_laps_adj += self.set_lap_dist
                row[16] = self.set_lap_dist
                i_lap += 1
                # if i_lap == 5:
                #     set_lap_dist = METERS_PER_MILE * 0.002
                # i_lap_act = i_lap - 1
                # set_lap_dist = laps_act[i_lap_act] * METERS_PER_MILE

            if row[0] == "Data" and row[2] == "session" and row[15] == "total_distance":
                total_session_row = rows[ir]

        total_prev_laps = prev_dist
        total_prev_laps_adj += self.set_lap_dist
        total_session_row[16] = total_prev_laps_adj

        return rows

    def output_file_proc(self, rows):
        with open(f"{self.ROOT_DIR}/{self.AFTER_CSV_FILENAME}", mode="w") as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

        csv_fit_command = f"java -jar ~/Documents/FitSDKRelease_21.94.00/java/FitCSVTool.jar -c ./{self.AFTER_CSV_FILENAME} ./{self.AFTER_FIT_FILENAME}"
        os.system(csv_fit_command)


fixer = FixActivity()
rows_proc = fixer.get_rows_proc()
fixer.output_file_proc(rows_proc)
