Python script to generate course schedules for a small private school. Requires PuLP and (tested with) CoinMP to be installed. Run

./solve_schedule.py --help
./check_schedule.py --help

for an explanation of the options.

How to run, e.g. on the sample data provided for a duration of 5 minutes:

./solve_schedule.py sample_students sample_teachers sample_schedule_templates/empty_sm.txt -c -t 5

Using a longer duration produces a schedule with fewer conflicts.

Provided under the terms of the MIT License, as stated in the file LICENSE.txt.
