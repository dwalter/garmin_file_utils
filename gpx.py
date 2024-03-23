SOURCE_FILE = "/Users/dwalter/Documents/projects/copy_from.gpx"
DESTINATION_FILE = "/Users/dwalter/Documents/projects/after-copy-from.gpx"

# <time>2023-01-28T21:39:31Z</time>
# 2023-03-15T22:16:52Z
T_START_MIN = 16
T_START_SEC = 55

# <time>2023-01-28T21:42:47Z</time>
# <time>2023-03-15T22:30:44Z</time>
T_END_MIN = 30
T_END_SEC = 39

TOTAL_SEC = (T_END_MIN * 60 - T_START_MIN * 60) + (T_END_SEC - T_START_SEC)

rows = []
with open(SOURCE_FILE, "r") as f:
    for r in f:
        rows.append(r)

# kw = "<time>2023-01-28T21:"
kw = "<time>2023-03-15T22:"

count = sum([kw in r for r in rows])
ic = 0

sec_per_r = TOTAL_SEC / float(count)
leftover = 0.0
prev_t = T_START_MIN * 60 + T_START_SEC

for i, _ in enumerate(rows):
    r = rows[i]
    # kw = "<time>2022-11-17T13:"
    if kw not in r:
        continue

    start, end = r.split(kw)
    # 2022-11-17T13:08:21Z

    start = start + kw
    # remove the xx:xx part
    end = end[5:]

    t = prev_t + sec_per_r + leftover
    t_int = int(t)
    leftover = t - t_int

    t = t_int
    prev_t = t

    t_min = int(t / 60)
    t_sec = int(t % 60.0)

    t_min_str = str(t_min)
    t_min_str = (2 - len(t_min_str)) * "0" + t_min_str

    t_sec_str = str(t_sec)
    t_sec_str = (2 - len(t_sec_str)) * "0" + t_sec_str

    middle = t_min_str + ":" + t_sec_str

    new_r = start + middle + end

    rows[i] = new_r



with open(DESTINATION_FILE, "w") as f:
    for r in rows:
        f.write(r)
