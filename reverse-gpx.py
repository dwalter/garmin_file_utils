SOURCE_FILE = "/Users/dwalter/Documents/projects/before-j28-2.gpx"
DESTINATION_FILE = "/Users/dwalter/Documents/projects/before-rev-j28-2.gpx"

chunks = []
chunk = []
with open(SOURCE_FILE, "r") as f:
    for r in f:
        chunk.append(r)
        if "</trkpt>" in r:
            chunks.append([x for x in chunk])
            chunk = []

chunks.reverse()

with open(DESTINATION_FILE, "w") as f:
    for rows in chunks:
        for r in rows:
            f.write(r)
