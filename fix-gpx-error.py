import xml.etree.ElementTree as ET
import sys

def check_gpx_file(gpx_file_path):
    try:
        tree = ET.parse(gpx_file_path)
        root = tree.getroot()

        if root.tag != '{http://www.topografix.com/GPX/1/1}gpx':
            print("Root element is not 'gpx'.")

        for elem in root.iter():
            if not isinstance(elem.tag, str):
                print(f"Element with incorrect tag type: {elem.tag}")

        print("GPX file check completed. No formatting errors found.")

    except ET.ParseError as e:
        print(f"Error while parsing the GPX file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    gpx_file_path = "/Users/dwalter/Documents/projects/bm2023.gpx"
    check_gpx_file(gpx_file_path)
