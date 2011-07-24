#!/usr/bin/env python
# Takes a (possibly partial) schedule and checks it for conflicts.
# Provided under the terms of the MIT License, as stated in LICENSE.txt.

from course_selection import Preferences, Schedule, gencmp_conflict, cmp_to_key
from optparse import OptionParser

# Helper functions for formatting the final report in user-readable form:

def format_list(items):
  if len(items) == 2:
    return items[0] + " and " + items[1]
  first, ret = True, ""
  for item in items:
    if first:
      first = False
    else:
      ret = ret + ", "
    ret = ret + item
  return ret

def format_conflict(conflict):
  people, courses, timeslot = conflict
  if len(people) == 1:
    students_take = "student takes"
  else:
    students_take = "students take"
  many_courses = format_list(courses)
  str1 = "COURSE CONFLICT: %d %s %s at %s:" \
      % (len(people), students_take, many_courses, timeslot)
  str2 = format_list(people)
  return str1 + "\n\t" + str2

def format_missing_course(course_missing):
  people, course = course_missing
  if len(people) == 1:
    students_request = "student requests"
  else:
    students_request = "students request"
  str1 = "COURSE NOT OFFERED: %d %s %s, which isn't scheduled:" \
      % (len(people), students_request, course)
  str2 = format_list(people)
  return str1 + "\n\t" + str2

def format_student_conflict(conflicting_courses, timeslot):
  return "CONFLICT: %s at %s" % (format_list(conflicting_courses), timeslot)

def format_student_missing_course(missing_course):
  return "COURSE NOT OFFERED: %s" % missing_course

# Actual logic for assembling a conflict report:

def gencmp_named_conflicts(schedule):
  old_comparator = gencmp_conflict(schedule) # -- simpler criteria.
  def comparator(conflict1, conflict2):
    people1, courses1, timeslot1 = conflict1
    people2, courses2, timeslot2 = conflict2

    # First compare by # of people affected, largest first:
    lendelta = -cmp(len(people1), len(people2))
    if lendelta is not 0: return lendelta

    # Then use criteria for non-named conflicts:
    return old_comparator((courses1, timeslot1,), (courses2, timeslot2,))
  return comparator

def cmp_missing_courses(missing1, missing2):
  people1, course1 = missing1
  people2, course2 = missing2

  # First compare by # of people affected, largest first:
  lendelta = -cmp(len(people1), len(people2))
  if lendelta is not 0: return lendelta
  
  # Then compare by course name:
  return cmp(course1, course2)

def cmp_lastname(student1, student2):
  lastname1 = student1[student1.find(' ') + 1:]
  lastname2 = student2[student2.find(' ') + 1:]
  return cmp(lastname1, lastname2)

def cmp_student_conflicts(student_cfl_info1, student_cfl_info2):
  student1, cfl1, missing1 = student_cfl_info1
  student2, cfl2, missing2 = student_cfl_info2

  # First compare by # of conflicts, largest first:
  lendelta = -cmp(len(cfl1) + len(missing1), len(cfl2) + len(missing2))
  if lendelta is not 0: return lendelta
  
  # Then compare by course name:
  return cmp_lastname(student1, student2)

def print_conflict_report(preferences, schedule):
  # Go through the students in preferences and build conflicts, missing_courses:
  conflicts, missing_courses = {}, {}
  for student, courses in preferences.people.items():
    student_conflicts, student_missing_courses = \
        schedule.problems_for_selection(courses)
    for conflict_info in student_conflicts:
      if conflict_info in conflicts:
        conflicts[conflict_info].append(student)
      else:
        conflicts[conflict_info] = [student]
      conflicts[conflict_info].sort(key=cmp_to_key(cmp_lastname))
    for missing_course_info in student_missing_courses:
      if missing_course_info in missing_courses:
        missing_courses[missing_course_info].append(student)
      else:
        missing_courses[missing_course_info] = [student]
      missing_courses[missing_course_info].sort(key=cmp_to_key(cmp_lastname))

  def util_combine(conflict, people):
    courses, timeslot = conflict
    return people, courses, timeslot
  conflicts = [util_combine(i, p) for i, p in conflicts.items()]
  missing_courses = [(p, c) for c, p in missing_courses.items()]

  conflicts.sort(key=cmp_to_key(gencmp_named_conflicts(schedule)))
  missing_courses.sort(key=cmp_to_key(cmp_missing_courses))

  # Then, print a conflict report:
  for conflict in conflicts:
    print format_conflict(conflict)
  print "" # -- extra newline for readability.
  for course_missing in missing_courses:
    print format_missing_course(course_missing)

def print_student_report(preferences, schedule):
  conflict_lst = []
  for student, courses in preferences.people.items():
    student_conflicts, student_missing_courses = \
        schedule.problems_for_selection(courses)
    if student_conflicts == [] and student_missing_courses == []:
      continue # -- skip the student if there are no problems.
    conflict_lst.append((student, student_conflicts, student_missing_courses,))

  conflict_lst.sort(key=cmp_to_key(cmp_student_conflicts))

  for student, student_conflicts, student_missing_courses in conflict_lst:
    print "Conflicts for: " + student
    for conflicting_courses, timeslot in student_conflicts:
      print "\t" + format_student_conflict(conflicting_courses, timeslot)
    for missing_course in student_missing_courses:
      print "\t" + format_student_missing_course(missing_course)
    print "" # -- extra newline at the end.

if __name__=="__main__":
  usage = "%prog <preferences> <schedule>"
  parser = OptionParser(usage=usage)
  parser.add_option('-s', '--by-student', action="store_true", default=False, \
                    help="print conflict report by student, not by course")
  (opts, args) = parser.parse_args()

  if len(args) != 2:
    parser.error("two arguments required: student preferences, and schedule")

  data_dir, selection_file = args[0], args[1]
  preferences, schedule = Preferences(data_dir), Schedule(selection_file)
  # Check for the --by-student option:
  if opts.by_student:
    print_student_report(preferences, schedule)
  else:
    print_conflict_report(preferences, schedule)
