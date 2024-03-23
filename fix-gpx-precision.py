import re

def check_lat_lon_precision(gpx_file_path):
    lat_lon_pattern = re.compile(r'lat="(-?\d+\.\d+)"\s+lon="(-?\d+\.\d+)"')
    line_number = 0

    with open(gpx_file_path, "r") as file:
        for line in file:
            line_number += 1
            match = lat_lon_pattern.search(line)

            if match:
                lat, lon = match.groups()

                if len(lat.split(".")[1]) != 7 or len(lon.split(".")[1]) != 7:
                    print(f"Incorrect precision at line {line_number}: {line.strip()}")

if __name__ == "__main__":
    gpx_file_path = "/Users/dwalter/Documents/projects/bm2023.gpx"
    check_lat_lon_precision(gpx_file_path)
