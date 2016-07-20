#!/usr/bin/env python
#
# Copyright (c) 2016, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import csv
import glob


# TODO: Create a WeeklyUserLogic class for extensibility
def create_days_of_week(file):
    """Parse CSV file into days of week"""

    sunday_entries = []
    monday_entries = []
    tuesday_entries = []
    wednesday_entries = []
    thursday_entries = []
    friday_entries = []
    saturday_entries = []
    reader = csv.DictReader(open(file), fieldnames=('escalation_level',
                                                    'user_or_team',
                                                    'type',
                                                    'day_of_week',
                                                    'start_time',
                                                    'end_time'))
    reader.next()
    for row in reader:
        entry = {
            'escalation_level': int(row['escalation_level']),
            'id': row['user_or_team'],
            'type': row['type'],
            'start_time': row['start_time'],
            'end_time': row['end_time']
        }
        if row['day_of_week'] == 0 or row['day_of_week'].lower() == 'sunday':
            sunday_entries.append(entry)
        elif row['day_of_week'] == 1 or row['day_of_week'].lower() == 'monday':
            monday_entries.append(entry)
        elif (row['day_of_week'] == 2 or
              row['day_of_week'].lower() == 'tuesday'):
            tuesday_entries.append(entry)
        elif (row['day_of_week'] == 3 or
              row['day_of_week'].lower() == 'wednesday'):
            wednesday_entries.append(entry)
        elif (row['day_of_week'] == 4 or
              row['day_of_week'].lower() == 'thursday'):
            thursday_entries.append(entry)
        elif row['day_of_week'] == 5 or row['day_of_week'].lower() == 'friday':
            friday_entries.append(entry)
        elif (row['day_of_week'] == 6 or
              row['day_of_week'].lower() == 'saturday'):
            saturday_entries.append(entry)
        else:
            print ("Error: Entry {0} does not have a valid day_of_week: {1}"
                   .format(row['user_or_team'], row['day_of_week']))
    # Create days with entries
    sunday = {'day_of_week': 0, 'entries': sunday_entries}
    monday = {'day_of_week': 1, 'entries': monday_entries}
    tuesday = {'day_of_week': 2, 'entries': tuesday_entries}
    wednesday = {'day_of_week': 3, 'entries': wednesday_entries}
    thursday = {'day_of_week': 4, 'entries': thursday_entries}
    friday = {'day_of_week': 5, 'entries': friday_entries}
    saturday = {'day_of_week': 6, 'entries': saturday_entries}
    return [sunday, monday, tuesday, wednesday, thursday, friday, saturday]


def split_days_by_level(base_ep):
    """Split days in escalation policy by level"""

    levels = {}
    ep_by_level = []
    for day in base_ep[0]['schedules'][0]['days']:
        for entry in day['entries']:
            if str(entry['escalation_level']) in levels:
                (levels[str(entry['escalation_level'])]['days']
                 [str(day['day_of_week'])].append(entry))
            else:
                levels[str(entry['escalation_level'])] = ({'days': {'0': [],
                                                          '1': [], '2': [],
                                                          '3': [], '4': [],
                                                          '5': [], '6': []}})
                (levels[str(entry['escalation_level'])]['days']
                 [str(day['day_of_week'])].append(entry))
    for level in levels.keys():
        days = []
        i = 0
        while i <= 6:
            for day in levels[level]['days']:
                if int(day) == i:
                    days.append(levels[level]['days'][day])
                    i += 1
        ep_by_level.insert(int(level), {
            'schedules': [{
                'name': ("{0}_level_{1}".format(base_ep[0]['schedules'][0]
                         ['name'], level)),
                'days': days
            }]
        })
    return ep_by_level


def get_time_periods(ep_by_level):
    """Breaks out each day by time period"""

    for level in ep_by_level:
        for i, day in enumerate(level['schedules'][0]['days']):
            time_periods = []
            for entry in day:
                # Loop through current time_periods to check for overlaps
                if len(time_periods) > 0:
                    overlap = False
                    for period in time_periods:
                        # TODO: Handle cases where times overlap but are not exactly the same start & end # NOQA
                        if (entry['start_time'] == period['start_time'] and
                           entry['end_time'] == period['end_time']):
                            period['entries'].append({
                                'id': entry['id'],
                                'type': entry['type']
                            })
                            overlap = True
                            break
                    if not overlap:
                        time_periods.append({
                            'start_time': entry['start_time'],
                            'end_time': entry['end_time'],
                            'entries': [{
                                'id': entry['id'],
                                'type': entry['type']
                            }]
                        })
                else:
                    time_periods.append({
                        'start_time': entry['start_time'],
                        'end_time': entry['end_time'],
                        'entries': [{
                            'id': entry['id'],
                            'type': entry['type']
                        }]
                    })
            level['schedules'][0]['days'][i] = {"time_periods": time_periods}
    return ep_by_level


def check_for_overlap(ep_by_level):
    """Checks time periods for multiple entries and breaks the entries into \
    multiple schedules
    """
    # 4) Check for multiple entires in a time period and break them out into two schedules # NOQA
    for level in ep_by_level:
        # Save schedule name
        schedule_name = level['schedules'][0]['name']
        for i, day in enumerate(level['schedules'][0]['days']):
            for ind, period in enumerate(day['time_periods']):
                if len(period['entries']) > 1:
                    # Update name for multis
                    level['schedules'][0]['name'] = "{0}_multi_1".format(schedule_name)
                    for index, entry in enumerate(period['entries']):
                        # Loop through schedules to see if multi schedule already exists skipping first index
                        # FIXME: Create many more schedules than needed, not properly finding dupes
                        # TODO: move up under the level loop? I think this might be a problem with exists getting set to false on each entry
                        schedule_exists = False
                        for idx, schedule in enumerate(level['schedules']):
                            if "multi_{0}".format(str(index + 1)) == schedule['name'][-(6 + len(str(index + 1))):] and index > 0:
                                schedule_exists = True
                                # Append time period if day exists or create new day
                                try:
                                    level['schedules'][idx]['days'][i]['time_periods'].append({
                                        'start_time': period['start_time'],
                                        'end_time': period['end_time'],
                                        'entries': [entry]
                                    })
                                except IndexError:
                                    level['schedules'][idx]['days'].insert(i, {
                                        'time_periods': {
                                            'start_time': period['start_time'],
                                            'end_time': period['end_time'],
                                            'entries': [entry]
                                        }
                                    })
                                break
                        if not schedule_exists:
                            # Create days for the new schedule
                            days = []
                            for n in range(i):
                                days.append({'time_periods': []})
                            days.append({'time_periods': [period]})
                            # Create new schedule with days
                            level['schedules'].append({
                                'name': "{0}_multi_{1}".format(schedule_name, str(index + 1)),
                                'days': days
                            })
        # TODO: Move this to new function
        # Delete all indices that have been moved to new schedules
        # for item in to_delete:
        #     del level['schedules'][0]['days'][item['day']]['time_periods'][item['period']]['entries'][item['entry']]
    return ep_by_level


def main():
    # Loop through all CSV files
    files = glob.glob('src/csv/*.csv')
    for file in files:
        # TODO: Add logic to handle non-weekly schedules
        days = create_days_of_week(file)
        # Create list of escalation policies by level
        base_ep = [{
            'schedules': [{
                # TODO: Use regex to parse filename
                'name': file[8:len(file) - 4],
                'days': days
            }]
        }]
        ep_by_level = split_days_by_level(base_ep)
        # TODO: Handle cominbing cases where one on-call starts at 0:00 and another ends at 24:00 # NOQA
        ep_by_level = get_time_periods(ep_by_level)
        print ep_by_level
    # 5) Remove entries list from the ep_by_level object
    # 6) Break each day down by time period
    # 7) Loop through consecutive days for patterns
    # 8) Each batch of user/time period/consecutive days becomes a new layer
    # 9) When a batch has a team, get the users on that team instead
    # 10) Each possible schedule on each EP level becomes a schedule based on layers in 7 # NOQA
    # 11) EP is created

if __name__ == '__main__':
    sys.exit(main())