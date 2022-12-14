"""
Solutions for AOC 2018 Day 4 - "Repose Record".
"""

import re


def process_input_file(filepath="./input/day04.txt"):
    """
    Processes the AOC 2018 Day 4 input file into the format required by the
    solver functions. Returns dict recording the amount of time spent asleep
    during each minute of the midnight hour for each guard.
    """
    with open(filepath, encoding="utf-8") as file:
        sleep_recs = []
        regex_timestamp = re.compile(
            r"^\[(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)\]")
        regex_guard = re.compile(r"Guard #(\d+) begins shift")
        for line in file.readlines():
            if len(line := line.strip()) == 0:
                continue
            if match_timestamp := regex_timestamp.match(line):
                year = int(match_timestamp.group(1))
                month = int(match_timestamp.group(2))
                day = int(match_timestamp.group(3))
                hour = int(match_timestamp.group(4))
                minute = int(match_timestamp.group(5))
                sleep_recs.append((year, month, day, hour, minute, line))
        # Sort the repose records in order
        sleep_recs = sorted(sleep_recs,
                            key=lambda rec: (rec[0], rec[1], rec[2], rec[3], rec[4]))
        # Determine shift records
        cursor = 0
        guard_shifts = []
        while cursor < len(sleep_recs):
            if match_guard := regex_guard.search(sleep_recs[cursor][5]):
                guard_id = int(match_guard.group(1))
                sleep_periods = []
                cursor += 1
                while cursor < len(sleep_recs) and \
                        not regex_guard.search(sleep_recs[cursor][5]):
                    if "wakes up" in sleep_recs[cursor][5]:
                        left = sleep_recs[cursor - 1][4]
                        right = sleep_recs[cursor][4]
                        sleep_periods.append((left, right))
                    cursor += 1
                guard_shifts.append((guard_id, sleep_periods))
        return generate_guard_sleep_counts(guard_shifts)


def solve_part1(guard_sleep_counts):
    """
    Solves AOC 2018 Day 4 Part 1 // Finds the guard that spends the most minutes
    asleep, returning the ID of that guard multiplied by the minute that they
    spend the most time asleep.
    """
    # Find the guard that spends the most minutes asleep
    most_minutes_asleep = -1
    guard_id_sleepy = -1
    for (guard_id, sleep_hour_record) in guard_sleep_counts.items():
        time_asleep = sum(sleep_hour_record.values())
        if time_asleep > most_minutes_asleep:
            most_minutes_asleep = time_asleep
            guard_id_sleepy = guard_id
    # Find the sleepiest minute for the sleepiest guard
    sleepiest_minute = max(guard_sleep_counts[guard_id_sleepy],
                           key=guard_sleep_counts[guard_id_sleepy].get)
    return guard_id_sleepy * sleepiest_minute


def solve_part2(guard_sleep_counts):
    """
    Solves AOC 2018 Day 4 Part 2 // Finds the guard most frequently asleep on
    the same minute, returning the ID of that guard multiplied by the chosen
    minute.
    """
    # Find the guard that is most frequently asleep on the same minute
    most_time_asleep = -1
    guard_id_sleepy = -1
    chosen_minute = -1
    for (guard_id, minute_sleep_counts) in guard_sleep_counts.items():
        for (minute, sleep_count) in minute_sleep_counts.items():
            if sleep_count > most_time_asleep:
                most_time_asleep = sleep_count
                guard_id_sleepy = guard_id
                chosen_minute = minute
    return guard_id_sleepy * chosen_minute


def generate_guard_sleep_counts(guard_shifts):
    """
    Generates the guard sleep counts (the total amount of time spent asleep in
    each minute of the midnight hour by each guard) by processing the guard
    shifts.
    """
    guard_sleep_counts = {}
    for (guard_id, sleep_periods) in guard_shifts:
        if guard_id not in guard_sleep_counts:
            guard_sleep_counts[guard_id] = {i: 0 for i in range(60)}
        for (left, right) in sleep_periods:
            for minute in range(left, right + 1):
                guard_sleep_counts[guard_id][minute] += 1
    return guard_sleep_counts
