from random import shuffle

# Appliocation Preference Special Values
NO_PREFERENCE = 0
ANY_FIRST_FORTNIGHT = -1
ANY_SECOND_FORTNIGHT = -2
ANY_EITHER_FORTNIGHT = -3


class StaffMember:

    def __init__(self, id: int):
        self.id = id
        self.name = ""
        # The important factor here is whether the oversubscribed gender (women) is too highly represented on a camp.
        # It doesn't actually matter what gender they are beyond that.
        self.is_dominant_gender = False 
        self.preferences = []
        self.is_group_chief = False
        self.has_inclusion_experience = False
        self.is_experienced = False
        self.must_camp_with = []
        self.must_not_camp_with = []
    
    def __str__(self):
        return self.name


class Camp:

    def __init__(self, id: int):
        self.id = id
        self.name = ""
        self.min_inclusion_experience_group_chiefs = 0
        self.min_inclusion_experience_staff = 0
        self.min_group_chiefs = 0
        self.min_experienced_staff = 0
        self.min_staff = 0
        self.max_staff = 0
        self.staff = []

    def __str__(self):
        return self.name

    def get_allocated_inclusion_experience_group_chiefs(self) -> int:
        return len([s for s in self.staff if s.is_group_chief and s.has_inclusion_experience])

    def get_allocated_group_chiefs(self) -> int:
        return len([s for s in self.staff if s.is_group_chief])

    def get_allocated_inclusion_experience_staff(self) -> int:
        return len([s for s in self.staff if s.has_inclusion_experience])

    def get_allocated_experienced_staff(self) -> int:
        return len([s for s in self.staff if s.is_experienced])

    def get_allocated_gender_balance(self) -> int:
        return len([s for s in self.staff if s.is_dominant_gender]) / len(staff)

    def get_allocated_staff(self) -> int:
        return len(self.staff)


log_filepath = "log.txt"
log_to_file = True
log_to_stdout = False


def log(message: str) -> None:
    """Writes message to a file"""
    if log_to_file:
        with open(log_filepath, "a") as log_file:
            log_file.write(message + "\n")
    if log_to_stdout:
        print(message)


def __camp_loop(camps):
    """Custom iterator that loops through (non-full) camps until they're all full and then stops"""
    i = 0
    while True:
        if len(camps[i].staff) < camps[i].max_staff:
            yield camps[i]
        i += 1
        i %= len(camps)
        if all([len(c.staff) == c.max_staff for c in camps]):
            break


def __add_staff_to_camp(staff: StaffMember, camp: Camp, application_list: list, reason="") -> None:
    """Add a staff to a camp and remove them from the list of applications"""
    if reason:
        reason = "(" + reason + ")"
    log(f"\tAllocating {staff.name} to {camp.name} {reason}")
    camp.staff.append(staff)
    application_list.remove(staff)


def __allocate_from_pool(pool_name: str, camps: list, application_list: list, current_pool: list, camp_iterator, condition, consider_gender=False) -> None:
    """"""
    log(f"Allocating {pool_name}")
    shuffle(current_pool)

    while True:
        camp = next(camp_iterator)
        if not current_pool:
            log(f"No more {pool_name}")
            break

        if condition(camp):
            reason = ""
            staff = None

            # TODO: Question: Will this be run for both fortnights/all camps at once? 
            #       In which case, then camps will need to say whether they're first/second fortnight
            #       Or else, then somehow will need to know if a preference for first/second is relevant to this application for this camp

            if not staff:
                staff = next((s for s in current_pool if (s.preferences[0] == camp.id) or (s.preferences[0] < 0)), None) # First choice preferences
                reason = "First choice"
            if not staff:
                staff = next((s for s in current_pool if (s.preferences[1] == camp.id) or (s.preferences[1] < 0)), None) # Second choice preferences
                reason = "2nd choice"
            if not staff:
                staff = next((s for s in current_pool if (s.preferences[2] == camp.id) or (s.preferences[2] < 0)), None) # Third choice preferences
                reason = "3rd choice"
            if not staff:
                staff = current_pool[0]
                reason = f"Any staff from {pool_name}"
            
            # TODO: Take gender into account (sometimes)
            # TODO: Handle the case where the staff *mustn't* camp with someone who's already on this camp

            current_pool.remove(staff)
            __add_staff_to_camp(staff, camp, application_list, reason)
            if staff.must_camp_with:
                # TODO: If the staff has anyone in their must_camp_with, then also add them
                print("Adding tag alongs")

        if all([not condition(c) for c in camps]):
            break


def allocate(camps: list, applications: list) -> list:
    """"""
    camp_iterator = __camp_loop(camps)

    pool = [s for s in applications if s.is_group_chief and s.has_inclusion_experience]
    __allocate_from_pool("Group Chiefs with Inclusion Experience", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_inclusion_experience_group_chiefs() < c.min_inclusion_experience_group_chiefs)

    pool = [s for s in applications if s.has_inclusion_experience]
    __allocate_from_pool("Staff with Inclusion Experience", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_inclusion_experience_staff() < c.min_inclusion_experience_staff)

    pool = [s for s in applications if s.is_group_chief]
    __allocate_from_pool("Group Chiefs", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_group_chiefs() < c.min_group_chiefs)

    pool = [s for s in applications if s.is_experienced]
    __allocate_from_pool("Experienced Staff", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_experienced_staff() < c.min_experienced_staff, True)

    pool = [s for s in applications]
    __allocate_from_pool("Staff", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_staff() < c.min_staff, True)

    pool = [s for s in applications]
    __allocate_from_pool("Staff", camps, applications, pool, camp_iterator, 
        lambda c: c.get_allocated_staff() < c.max_staff, True)

    return camps


def analyse_allocations(camps: list, applications: list) -> None:
    staff_applied = len(applications)
    staff_placed = sum([c.get_allocated_staff() for c in camps])
    staff_on_first_choice  = sum([len([s for s in c.staff if s.preferences[0] == c.id]) for c in camps])
    staff_on_second_choice = sum([len([s for s in c.staff if s.preferences[1] == c.id]) for c in camps])
    staff_on_third_choice  = sum([len([s for s in c.staff if s.preferences[2] == c.id]) for c in camps])
    camp_applications = sorted(camps, key=lambda c: -len([a for a in applications if c.id in a.preferences]))

    print("")
    print("")
    print("--- Staff Allocations ---")
    print("")
    print(f"Total Applications:   {staff_applied}")
    print(f"Total Placed:         {staff_placed}")
    print(f"Placed on 1st Choice: {staff_on_first_choice}")
    print(f"Placed on 2nd Choice: {staff_on_second_choice}")
    print(f"Placed on 3rd Choice: {staff_on_third_choice}")
    print(f"Not Placed at all:    {staff_applied - staff_placed}")
    print(f"Camps by Popularity:")
    longest_camp_name = max([len(c.name) for c in camps])
    for c in camp_applications:
        applications_for_camp = [a for a in applications if c.id in a.preferences]
        name = ("(" + c.name + ")").ljust(longest_camp_name + 2, " ")
        camp_applications = str(len(applications_for_camp)).rjust(3, " ") + " applications"
        gender_balance = int(100 * len([s for s in c.staff if s.is_dominant_gender]) / len(c.staff))
        gender_balance = f"{gender_balance}% Women"
        print(f"  - Camp {c.id} {name} : {camp_applications}   {gender_balance}")
    print("Campers Not Placed:")
    not_placed = [s for s in applications if not any([s in c.staff for c in camps])]
    for s in not_placed:
        print(f"  - {s.name}: ({s.preferences[0]}, {s.preferences[1]}, {s.preferences[2]})")

