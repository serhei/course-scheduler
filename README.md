# Course Scheduling Utility

Python script to generate course schedules for a small private school. Given a schedule template (listing teachers, timeslots, and exclusions, as in [`sample_schedule_templates/empty_sm.txt`](sample_schedule_templates/empty_sm.txt)) and a set of preferences (that is, lists of courses offered by each teacher, as well as classlists listing the students that would *prefer* to take each course, as in [`sample_preference_files/test.txt`](sample_preference_files/test.txt)), the script generates an Integer Linear Programming model and solves it using CoinMP in order to minimize the number of schedule conflicts students experience (in aggregate).

(Other utilities are included, such as `jam_in_course.py` which was developed to assist in determining how to split a class into two sections, or where to add a new course without having to recalculate the entire schedule. For advanced users, poking around in the `solve_schedule.py` will also reveal a way to identify a course to de-prioritize. The logic behind this is that certain courses may be essential to a student's graduation, whereas others are optional extras; conflicts involving the optional courses could be weighted slightly less in order to ensure the scheduler prioritizes working on the essential courses.)

Requires PuLP and (tested with) CoinMP to be installed. Run

    ./solve_schedule.py --help
    ./check_schedule.py --help

for an explanation of the options.

How to run, e.g. on the sample data provided:

    ./solve_schedule.py -H output.html -p sample_preference_files/test.txt sample_schedule_templates/empty_sm.txt -t 5
    ./solve_schedule.py -H output.html sample_students sample_teachers sample_schedule_templates/empty_sm.txt -t 5

This produces a file like [`sample_output/output.html`](sample_output/output.html). Using a longer duration (`-t` option) produces a schedule with fewer conflicts.

Provided under the terms of the MIT License, as stated in the file LICENSE.txt.

## Setting things up

Get the [Pulp-OR LP modeler library](https://code.google.com/p/pulp-or/). Download and extract the 1.5.4 tarball and run `python setup.py install` (possibly as administrator).

Get CoinMP. For instance, download a [Linux tarball](http://www.coin-or.org/download/binary/CoinMP/) and follow the installation instructions, or get the Brew package on OS X using `brew install coinmp`.

Get the progressbar Python module, e.g. `sudo easy_install -U progressbar`.
