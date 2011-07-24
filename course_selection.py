# Core logic for representing a set of course preferences and a schedule.
# Provided under the terms of the MIT License, as stated in LICENSE.txt.

import re, os

# Helper functions for tabulating conflicts:

# A library function not available in Python 2.6:
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def gencmp_conflict(schedule):
    def comparator(conflict1, conflict2):
        courses1, timeslot1 = conflict1
        courses2, timeslot2 = conflict2

        # First compare by # of simultaneous courses, largest first:
        lendelta = -cmp(len(courses1), len(courses2))
        if lendelta is not 0: return lendelta

        # Then compare by chronological order of slots:
        index1 = schedule.slotlist.index(timeslot1)
        index2 = schedule.slotlist.index(timeslot2)
        return cmp(index1, index2)
    return comparator

# Helper functions for reading data from files:

pat_course = re.compile(r"^\s*(\b.*\b)\s*(?:\((.*)\))?\s*$")

def read_preference_file(path):
    input_file = open(path, "r")
    
    # Obtain the person's name from the first line in the file:
    name = input_file.readline().strip()
    
    # Each following line gives a course choice, with possible comment:
    courses = []
    for line in input_file:
        if re.match(r"\s*#", line) is not None: # -- skip comment lines.
            continue
        course, comment = pat_course.search(line).groups()
        courses.append((course,comment,))

    return name, courses

def split_schedule_line(line):
    items = line.split("/")
    items = [elt.strip() for elt in items] # -- trim whitespace.
    return items[0], items[1:] # -- separate the first element from the rest.

# Data structures:

class Preferences:
    """Can represent students' course preferences, or teachers' offerings."""

    def __init__(self, path=None):
        # TODO: people uses sets rather than lists
        self.people = {} # -- could be either students or teachers.
        self.classes = {} # TODO: use this more widely, e.g. in checker
        if path is not None:
            self.read_from_datadir(path)

    def read_from_datadir(self, datadir):
        for path in os.listdir(datadir):
            path = os.path.join(datadir, path)
            if not path.endswith('.txt'): # -- skip DS_Store type junk
                continue
            name, courses = read_preference_file(path)

            # Allow incremental addition from many datadirs:
            if name in self.people:
                self.people[name].extend(courses)
            else:
                self.people[name] = courses

            # Also update the classlists to contain the person's name:
            for course, _comment in courses:
                if course not in self.classes:
                    self.classes[course] = set()
                self.classes[course].add(name)


class Schedule:
    def __init__(self, path=None):
        self.slotlist = []
        self.timeslots = {}
        self.bad_slots = {} ## EXPERIMENTAL
        self.courses = {}
        if path is not None:
            self.read_from_file(path)

    def add(self, teacher, course, timeslot):
        if timeslot in self.timeslots:
            self.timeslots[timeslot][teacher] = course
        else:
            self.timeslots[timeslot] = {teacher: course}
        self.courses[course] = timeslot

    ## EXPERIMENTAL
    def add_bad_slot(self, teacher, timeslot):
        if teacher in self.bad_slots:
            self.bad_slots[teacher].append(timeslot)
        else:
            self.bad_slots[teacher] = [timeslot]

    def read_from_file(self, path):
        input_file = open(path, "r")

        # Obtain a list of teachers from the first line in the file:
        line = input_file.readline()
        _dontcare, teachers = split_schedule_line(line)

        # Each following line gives the courses scheduled for one timeslot:
        for line in input_file:
            timeslot, courses = split_schedule_line(line)
            self.slotlist.append(timeslot) # -- note order of slots.
            for course, teacher in zip(courses, teachers):
                if course == "-": # -- indicates an empty timeslot.
                    continue

                ## EXPERIMENTAL (for 'teacher can't come in' marks)
                if course == "X":
                    if True:
                        self.add_bad_slot(teacher, timeslot)
                    continue

                self.add(teacher, course, timeslot)

    def problems_for_selection(self, course_list):
        timetable, conflicts, missing_courses = {}, [], []

        # First draw a timetable that shows where courses conflict:
        for course, _comment in course_list:
            if course not in self.courses: # -- course not offered
                missing_courses.append(course)
                continue
            timeslot = self.courses[course]
            if timeslot not in timetable: # -- no conflict for this course, yet.
                timetable[timeslot] = [course]
                continue
            timetable[timeslot].append(course)

        # Then go and read off the list of conflicts:
        for conflicting_courses in timetable.values():
            if len(conflicting_courses) < 2: # -- no conflict in this slot.
                continue
            timeslot = self.courses[conflicting_courses[0]]
            conflicts.append((tuple(conflicting_courses),timeslot,))

        conflicts.sort(key=cmp_to_key(gencmp_conflict(self)))
        missing_courses.sort() # -- in alphabetical order.

        return conflicts, missing_courses
