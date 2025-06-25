#!/usr/bin/env python

import sys
import csv
from allocation_data import STAFF_ID, STAFF_FIRST_NAME, STAFF_LAST_NAME, STAFF_GENDER, STAFF_GROUP_CHIEF, STAFF_FIRST_CHOICE, STAFF_SECOND_CHOICE, STAFF_THIRD_CHOICE, STAFF_CAMP_EXPERIENCE
from allocation_data import load_staff_data, load_camp_data, save_allocation_data
from allocator import StaffMember, Camp
from allocator import NO_PREFERENCE, ANY_FIRST_FORTNIGHT, ANY_SECOND_FORTNIGHT, ANY_EITHER_FORTNIGHT
from allocator import analyse_allocations

STAFF_ALLOCATED_CAMP = 45


def _load_camp_preference(preference: str) -> int:
    if preference == '':
        return NO_PREFERENCE
    if preference == "Any either fortnight":
        return ANY_EITHER_FORTNIGHT
    if preference == "Any 1st fortnight":
        return ANY_FIRST_FORTNIGHT
    if preference == "Any 2nd fortnight":
        return ANY_SECOND_FORTNIGHT
    return int(preference)


def main() -> None:
    applications_filepath = "data/All Applications for All Staff for Summer - First Fortnight.csv"
    camps_filepath = "data/Camp_Requirements First Fortnight.csv"
    staff = load_staff_data(applications_filepath)
    camps = load_camp_data(camps_filepath)

    with open(applications_filepath, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        next(csv_reader)
        for row in csv_reader:
            camp_id = row[STAFF_ALLOCATED_CAMP]
            if camp_id:
                camp_id = int(camp_id)
            else:
                continue
            staff_id = int(row[STAFF_ID])

            c = next((c for c in camps if c.id == camp_id), None)
            s = next((s for s in staff if s.id == staff_id), None)
            if c and s:
                c.staff.append(s)

    analyse_allocations(camps, staff)
    save_allocation_data(camps, "2025 Actual Allocations.txt")


if __name__ == '__main__':
    main()


# ./test_current.py
