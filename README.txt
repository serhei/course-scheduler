# Course Scheduling Utility

Python script to generate course schedules for a small private school. Requires PuLP and (tested with) CoinMP to be installed. Run

    ./solve_schedule.py --help
    ./check_schedule.py --help

for an explanation of the options.

How to run, e.g. on the sample data provided:

    ./solve_schedule.py -H output.html -p sample_preference_files/test.txt sample_schedule_templates/empty_sm.txt -t 5
    ./solve_schedule.py -H output.html sample_students sample_teachers sample_schedule_templates/empty_sm.txt -t 5

Using a longer duration produces a schedule with fewer conflicts.

Provided under the terms of the MIT License, as stated in the file LICENSE.txt.

## Setting things up

Get the [Pulp-OR LP modeler library](https://code.google.com/p/pulp-or/). Download and extract the 1.5.4 tarball and run `python setup.py install` (possibly as administrator).

Get CoinMP. For instance, download a [Linux tarball](http://www.coin-or.org/download/binary/CoinMP/) and follow the installation instructions, or get the Brew package on OS X using `brew install coinmp`.

Get the progressbar Python module, e.g. `sudo easy_install -U progressbar`.
