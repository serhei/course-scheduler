#!/usr/bin/env python
# Takes a list of students and a schedule and tries to figure out
# timeslots where they could be placed in a section.
#
# This is very good for splitting a large class, or for adding a
# last-minute course offering.
#
# Provided under the terms of the MIT License, as stated in LICENSE.txt.

from course_selection import Preferences, Schedule, read_combined_file
from check_schedule import format_list
from optparse import OptionParser

def read_classlist(path):
    # TODOXXX should also consider comma separation on each line
    # TODOXXX should also consider comments
    input_file = open(path, "r")
    return [line.strip() for line in input_file]

if __name__=="__main__":
    # TODOXXX add -o option?
    usage = "%prog <classlist> <preferences> <schedule>\n%prog -p <preference file> <classlist> <schedule>"
    parser = OptionParser(usage=usage)
    parser.add_option('-p', '--preferences', dest="preference_file", default="",
                      help="obtain student preferences from single file")
    (opts, args) = parser.parse_args()

    if opts.preference_file != "":
        if len(args) != 2:
            parser.error("two arguments required with option '-p': class list, and schedule")
        classlist_file = args[0]
        selection_file = args[1]
        students = read_classlist(classlist_file)
        offering, preferences = read_combined_file(opts.preference_file)
        schedule = Schedule(selection_file, True)
    else:
        if len(args) != 3:
            parser.error("three arguments required: student preferences, class list, and schedule")
        data_dir = args[0]
        classlist_file = args[1]
        selection_file = args[2]
        students = read_classlist(classlist_file)
        preferences, schedule = Preferences(data_dir), Schedule(selection_file, True)

    # Print initial classlist:
    print "Total %d students in class: %s" % (len(students), format_list(students))

    # Iterate through slots and show conflicts wrt classlist:
    for slot in schedule.slotlist:
        print "" # -- extra newline acts as separator
        print "Conflicts in slot " + slot
        seen_students = set()
        for teacher in schedule.timeslots[slot]:
            course_name = schedule.timeslots[slot][teacher]
            conflicts = []
            for student in students:
                for other_course, _comment in preferences.people[student]:
                    if course_name == other_course:
                        conflicts.append(student)
                        seen_students.add(student)
                        break
            if len(conflicts) != 0:
                print "\t%d students take %s: %s" \
                    % (len(conflicts), course_name, format_list(conflicts))

        remaining = []
        for student in students:
            if student not in seen_students:
                remaining.append(student)
        print "-- can put %d people in a section at this timeslot: %s" \
            % (len(remaining), format_list(remaining))
