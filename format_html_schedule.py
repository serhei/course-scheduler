#!/usr/bin/env python
# Reformat an old-style schedule as HTML.
# Provided under the terms of the MIT License as stated in LICENSE.txt.

from course_selection import Preferences, Schedule, read_combined_file
from solve_schedule import format_schedules_html
from optparse import OptionParser

if __name__=="__main__":
	usage = "%prog <offerings> <schedule>\n%prog -p <preference file> <schedule>"
	parser = OptionParser(usage=usage)
	parser.add_option('-p', '--preferences', dest="preference_file", default="",
	                  help="obtain student preferences from single file")
	(opts, args) = parser.parse_args()

	if opts.preference_file != "":
		if len(args) != 1:
			parser.error("one argument required with option '-p': schedule")
		selection_file = args[0]
		offering, preferences = read_combined_file(opts.preference_file)
		schedule = Schedule(selection_file, lenient=True)
	else:
		if len(args) != 2:
			parser.error("two arguments required: course offering, and schedule")
		data_dir, selection_file = args[0], args[1]
		offering = Preferences(data_dir)
		schedule = Schedule(selection_file, lenient=True)

	solutions = [(schedule, 0)]
	format_schedules_html(offering, schedule, -1, None, opts)
