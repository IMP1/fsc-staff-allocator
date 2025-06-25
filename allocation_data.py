import sys
import csv
from allocator import StaffMember, Camp
from allocator import NO_PREFERENCE, ANY_FIRST_FORTNIGHT, ANY_SECOND_FORTNIGHT, ANY_EITHER_FORTNIGHT
import random
import collections
from enum import Enum

# Application Spreadsheet Column Indicies
STAFF_ID = 47
STAFF_FIRST_NAME = 0
STAFF_LAST_NAME = 1
STAFF_GENDER = 2
STAFF_GROUP_CHIEF = 31
STAFF_FIRST_CHOICE = 40
STAFF_SECOND_CHOICE = 41
STAFF_THIRD_CHOICE = 42
STAFF_CAMP_EXPERIENCE = 33
# Camp Spreadsheet Column Indicies
CAMP_ID = 0
CAMP_NAME = 1
CAMP_MIN_INCLUSION_GROUP_CHIEFS = 2
CAMP_MIN_GROUP_CHIEFS = 3
CAMP_MIN_INCLUSION_STAFF = 4
CAMP_MIN_EXPERIENCED_STAFF = 5
CAMP_MIN_STAFF = 6
CAMP_MAX_STAFF = 7


log_filepath = "log.txt"
log_to_stdout = True
log_to_file = False
results_filepath = "results.txt"


def log(message: str) -> None:
    """"""
    if log_to_file:
        with open(log_filepath, "a") as log_file:
            log_file.write(message + "\n")
    if log_to_stdout:
        print(message)


def log_error(message: str) -> None:
    """"""
    print(message, file=sys.stderr)
    


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


def load_staff_data(filepath: str) -> list:
    staff = []
    try:
        with open(filepath, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(csv_reader)
            for row in csv_reader:
                staff_id = int(row[STAFF_ID])
                s = StaffMember(staff_id)
                s.name = row[STAFF_FIRST_NAME] + " " + row[STAFF_LAST_NAME]
                s.is_dominant_gender = (row[STAFF_GENDER] == "Female")
                s.preferences = []
                s.preferences.append(_load_camp_preference(row[STAFF_FIRST_CHOICE]))
                s.preferences.append(_load_camp_preference(row[STAFF_SECOND_CHOICE]))
                s.preferences.append(_load_camp_preference(row[STAFF_THIRD_CHOICE]))
                s.is_group_chief = row[STAFF_GROUP_CHIEF] == "Yes"
                s.has_inclusion_experience = False # TODO: This data seems to be missing from the spreadsheet
                s.is_experienced = int(row[STAFF_CAMP_EXPERIENCE]) >= 3
                s.must_camp_with = [] # TODO: Get from spreadsheet
                s.must_not_camp_with = [] # TODO: Get from spreadsheet
                staff.append(s)
    except FileNotFoundError as e:
        log_error(f"Could not find the file '{filepath}'. Make sure it exists.")
        exit(1)

    log("Application data:")
    log(f"  - {len(staff)} total applications")

    # Check for duplicates
    staff_ids = set()
    unique_staff = []
    duplicate_staff = []
    for s in staff:
        if s.id in staff_ids:
            duplicate_staff.append(s)
        else:
            unique_staff.append(s)
            staff_ids.add(s.id)

    if len(staff) > len(unique_staff):
        log(f"  - {len(staff) - len(unique_staff)} duplicate applications")
        staff = unique_staff

    # Apply inclusion experience assumptions
    if True:
        # NOTE: Currently inclusion experience is missing, so about 1/4 of the applicants are assumed to have inclusion experience, 
        # with 4/5 of those applying to Hodore (camp 20) assumed to have inclusion experience.
        random.shuffle(staff)
        hodore_inclusion_experience = int(len([s for s in staff if 20 in s.preferences]) * 4 / 5)
        general_inclusion_experience = int(len([s for s in staff if not 20 in s.preferences]) / 4)
        log(f"(TEMPORARY) Inclusion Experience:")
        log(f"  - Assuming {hodore_inclusion_experience} hodore applications have inclusion experience (4 in 5)")
        log(f"  - Assuming {general_inclusion_experience} general applications have inclusion experience (1 in 4)")
        for s in staff:
            if 20 in s.preferences and hodore_inclusion_experience > 0:
                s.has_inclusion_experience = True
                hodore_inclusion_experience -= 1
            elif 20 not in s.preferences and general_inclusion_experience > 0:
                s.has_inclusion_experience = True
                general_inclusion_experience -= 1
    # TODO: Remove the above once inclusion experience is part of the imported data set

    return staff


def load_camp_data(filepath: str) -> list:
    camps = []
    try:
        with open(filepath, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            next(csv_reader)
            for row in csv_reader:
                camp_id = int(row[CAMP_ID])
                c = Camp(camp_id)
                c.name = row[CAMP_NAME]
                c.min_inclusion_experience_group_chiefs = int(row[CAMP_MIN_INCLUSION_GROUP_CHIEFS])
                c.min_inclusion_experience_staff = int(row[CAMP_MIN_INCLUSION_STAFF])
                c.min_group_chiefs = int(row[CAMP_MIN_GROUP_CHIEFS])
                c.min_experienced_staff = int(row[CAMP_MIN_EXPERIENCED_STAFF])
                c.min_staff = int(row[CAMP_MIN_STAFF])
                c.max_staff = int(row[CAMP_MAX_STAFF])
                c.staff = []
                camps.append(c)
    except FileNotFoundError as e:
        log_error(f"Could not find the file '{filepath}'. Make sure it exists.")
        exit(1)
    return camps


def save_allocation_data(camps, filepath):
    with open(filepath, "w") as results:
        for c in camps:
            results.write(c.name + "\n")
            for s in c.staff:
                results.write("\t" + s.name + "\n")
            results.write("\n")
