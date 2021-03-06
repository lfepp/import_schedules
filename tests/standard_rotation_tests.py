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

import unittest
import sys
import json
import os
from datetime import datetime
import pytz
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from scheduleduty import scheduleduty  # NOQA

expected_filename = os.path.join(
    os.path.dirname(__file__),
    './expected_results/standard_rotation_expected.json'
)
input_filename = os.path.join(
    os.path.dirname(__file__),
    './input/standard_rotation_input.json'
)
config_filname = os.path.join(os.path.dirname(__file__), './config.json')

with open(expected_filename) as expected_file:
    expected = json.load(expected_file)

with open(input_filename) as input_file:
    input = json.load(input_file)

with open(config_filname) as config_file:
    config = json.load(config_file)

pd_rest = scheduleduty.PagerDutyREST(config['api_key'])
standard_rotation = scheduleduty.StandardRotationLogic(
    config['start_date'],
    config['end_date'],
    config['base_name'],
    config['time_zone']
)


class StandardRotationTests(unittest.TestCase):

    def get_restriction_type(self):
        expected_result = expected['get_restriction_type']['daily1']
        actual_result = standard_rotation.get_restriction_type(
            input['get_restriction_type']['daily1']['restriction_start_day'],
            input['get_restriction_type']['daily1']['restriction_end_day']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_type']['daily2']
        actual_result = standard_rotation.get_restriction_type(
            input['get_restriction_type']['daily2']['restriction_start_day'],
            input['get_restriction_type']['daily2']['restriction_end_day']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_type']['daily3']
        actual_result = standard_rotation.get_restriction_type(
            input['get_restriction_type']['daily3']['restriction_start_day'],
            input['get_restriction_type']['daily3']['restriction_end_day']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_type']['weekly1']
        actual_result = standard_rotation.get_restriction_type(
            input['get_restriction_type']['weekly1']['restriction_start_day'],
            input['get_restriction_type']['weekly1']['restriction_end_day']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_type']['weekly2']
        actual_result = standard_rotation.get_restriction_type(
            input['get_restriction_type']['weekly2']['restriction_start_day'],
            input['get_restriction_type']['weekly2']['restriction_end_day']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_restriction_type(
                input['get_restriction_type']['error']
                ['restriction_start_day'],
                input['get_restriction_type']['error']['restriction_end_day']
            )

    def get_rotation_turn_length(self):
        expected_result = expected['get_rotation_turn_length']['daily']
        actual_result = standard_rotation.get_rotation_turn_length(
            input['get_rotation_turn_length']['daily']['rotation_type'],
            input['get_rotation_turn_length']['daily']['shift_length'],
            input['get_rotation_turn_length']['daily']['shift_type']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_rotation_turn_length']['weekly']
        actual_result = standard_rotation.get_rotation_turn_length(
            input['get_rotation_turn_length']['weekly']['rotation_type'],
            input['get_rotation_turn_length']['weekly']['shift_length'],
            input['get_rotation_turn_length']['weekly']['shift_type']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_rotation_turn_length']['custom_hours']
        actual_result = standard_rotation.get_rotation_turn_length(
            input['get_rotation_turn_length']['custom_hours']['rotation_type'],
            input['get_rotation_turn_length']['custom_hours']['shift_length'],
            input['get_rotation_turn_length']['custom_hours']['shift_type']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_rotation_turn_length']['custom_days']
        actual_result = standard_rotation.get_rotation_turn_length(
            input['get_rotation_turn_length']['custom_days']['rotation_type'],
            input['get_rotation_turn_length']['custom_days']['shift_length'],
            input['get_rotation_turn_length']['custom_days']['shift_type']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_rotation_turn_length']['custom_weeks']
        actual_result = standard_rotation.get_rotation_turn_length(
            input['get_rotation_turn_length']['custom_weeks']['rotation_type'],
            input['get_rotation_turn_length']['custom_weeks']['shift_length'],
            input['get_rotation_turn_length']['custom_weeks']['shift_type']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_rotation_turn_length(
                input['get_rotation_turn_length']['error1']['rotation_type'],
                input['get_rotation_turn_length']['error1']['shift_length'],
                input['get_rotation_turn_length']['error1']['shift_type']
            )
        with self.assertRaises(ValueError):
            standard_rotation.get_rotation_turn_length(
                input['get_rotation_turn_length']['error2']['rotation_type'],
                input['get_rotation_turn_length']['error2']['shift_length'],
                input['get_rotation_turn_length']['error2']['shift_type']
            )

    def get_virtual_start(self):
        expected_result = expected['get_virtual_start']['daily']
        actual_result = standard_rotation.get_virtual_start(
            input['get_virtual_start']['daily']['rotation_type'],
            input['get_virtual_start']['daily']['handoff_day'],
            input['get_virtual_start']['daily']['handoff_time'],
            input['get_virtual_start']['daily']['start_date'],
            input['get_virtual_start']['daily']['time_zone']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_virtual_start']['weekly']
        actual_result = standard_rotation.get_virtual_start(
            input['get_virtual_start']['weekly']['rotation_type'],
            input['get_virtual_start']['weekly']['handoff_day'],
            input['get_virtual_start']['weekly']['handoff_time'],
            input['get_virtual_start']['weekly']['start_date'],
            input['get_virtual_start']['weekly']['time_zone']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_virtual_start']['custom1']
        actual_result = standard_rotation.get_virtual_start(
            input['get_virtual_start']['custom1']['rotation_type'],
            input['get_virtual_start']['custom1']['handoff_day'],
            input['get_virtual_start']['custom1']['handoff_time'],
            input['get_virtual_start']['custom1']['start_date'],
            input['get_virtual_start']['custom1']['time_zone']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_virtual_start']['custom2']
        actual_result = standard_rotation.get_virtual_start(
            input['get_virtual_start']['custom2']['rotation_type'],
            input['get_virtual_start']['custom2']['handoff_day'],
            input['get_virtual_start']['custom2']['handoff_time'],
            input['get_virtual_start']['custom2']['start_date'],
            input['get_virtual_start']['custom2']['time_zone']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_virtual_start(
                input['get_virtual_start']['error1']['rotation_type'],
                input['get_virtual_start']['error1']['handoff_day'],
                input['get_virtual_start']['error1']['handoff_time'],
                input['get_virtual_start']['error1']['start_date'],
                input['get_virtual_start']['error1']['time_zone']
            )
        with self.assertRaises(ValueError):
            standard_rotation.get_virtual_start(
                input['get_virtual_start']['error2']['rotation_type'],
                input['get_virtual_start']['error2']['handoff_day'],
                input['get_virtual_start']['error2']['handoff_time'],
                input['get_virtual_start']['error2']['start_date'],
                input['get_virtual_start']['error2']['time_zone']
            )
        with self.assertRaises(ValueError):
            standard_rotation.get_virtual_start(
                input['get_virtual_start']['error3']['rotation_type'],
                input['get_virtual_start']['error3']['handoff_day'],
                input['get_virtual_start']['error3']['handoff_time'],
                input['get_virtual_start']['error3']['start_date'],
                input['get_virtual_start']['error3']['time_zone']
            )

    def get_restriction_duration(self):
        expected_result = expected['get_restriction_duration']['daily1']
        actual_result = standard_rotation.get_restriction_duration(
            input['get_restriction_duration']['daily1']['restriction_type'],
            input['get_restriction_duration']['daily1']
            ['restriction_start_day'],
            input['get_restriction_duration']['daily1']
            ['restriction_start_time'],
            input['get_restriction_duration']['daily1']['restriction_end_day'],
            input['get_restriction_duration']['daily1']['restriction_end_time']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_duration']['daily2']
        actual_result = standard_rotation.get_restriction_duration(
            input['get_restriction_duration']['daily2']['restriction_type'],
            input['get_restriction_duration']['daily2']
            ['restriction_start_day'],
            input['get_restriction_duration']['daily2']
            ['restriction_start_time'],
            input['get_restriction_duration']['daily2']['restriction_end_day'],
            input['get_restriction_duration']['daily2']['restriction_end_time']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_duration']['weekly1']
        actual_result = standard_rotation.get_restriction_duration(
            input['get_restriction_duration']['weekly1']['restriction_type'],
            input['get_restriction_duration']['weekly1']
            ['restriction_start_day'],
            input['get_restriction_duration']['weekly1']
            ['restriction_start_time'],
            input['get_restriction_duration']['weekly1']
            ['restriction_end_day'],
            input['get_restriction_duration']['weekly1']
            ['restriction_end_time']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_restriction_duration']['weekly2']
        actual_result = standard_rotation.get_restriction_duration(
            input['get_restriction_duration']['weekly2']['restriction_type'],
            input['get_restriction_duration']['weekly2']
            ['restriction_start_day'],
            input['get_restriction_duration']['weekly2']
            ['restriction_start_time'],
            input['get_restriction_duration']['weekly2']
            ['restriction_end_day'],
            input['get_restriction_duration']['weekly2']
            ['restriction_end_time']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_restriction_duration(
                input['get_restriction_duration']['error1']
                ['restriction_type'],
                input['get_restriction_duration']['error1']
                ['restriction_start_day'],
                input['get_restriction_duration']['error1']
                ['restriction_start_time'],
                input['get_restriction_duration']['error1']
                ['restriction_end_day'],
                input['get_restriction_duration']['error1']
                ['restriction_end_time']
            )
        with self.assertRaises(ValueError):
            standard_rotation.get_restriction_duration(
                input['get_restriction_duration']['error2']
                ['restriction_type'],
                input['get_restriction_duration']['error2']
                ['restriction_start_day'],
                input['get_restriction_duration']['error2']
                ['restriction_start_time'],
                input['get_restriction_duration']['error2']
                ['restriction_end_day'],
                input['get_restriction_duration']['error2']
                ['restriction_end_time']
            )

    def parse_csv(self):
        expected_result = expected['parse_csv']
        actual_result = standard_rotation.parse_csv(
            'tests/csv/standard_rotation.csv'
        )
        self.assertEqual(expected_result, actual_result)

    def check_layers(self):
        expected_result = expected['check_layers']['valid1']
        actual_result = standard_rotation.check_layers(
            input['check_layers']['valid1']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['check_layers']['valid2']
        actual_result = standard_rotation.check_layers(
            input['check_layers']['valid2']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['check_layers']['invalid1']
        actual_result = standard_rotation.check_layers(
            input['check_layers']['invalid1']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['check_layers']['invalid2']
        actual_result = standard_rotation.check_layers(
            input['check_layers']['invalid2']
        )
        self.assertEqual(expected_result, actual_result)

    def parse_layers(self):
        expected_result = expected['parse_layers']['valid']
        actual_result = standard_rotation.parse_layers(
            input['parse_layers']['valid']['layers'],
            pd_rest
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(IndexError):
            standard_rotation.parse_layers(
                input['parse_layers']['error']['layers'],
                pd_rest
            )

    def parse_schedules(self):
        expected_result = expected['parse_schedules']
        actual_result = standard_rotation.parse_schedules(
            input['parse_schedules']['layers']
        )
        self.assertEqual(expected_result, actual_result)

    # HELPER FUNCTIONS
    def get_datetime(self):
        expected_result = datetime(2016, 8, 23, 7, 43, 28)
        actual_result = standard_rotation.get_datetime(
            input['get_datetime']['with_seconds']['date'],
            input['get_datetime']['with_seconds']['time']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = datetime(2016, 8, 23, 7, 43, 00)
        actual_result = standard_rotation.get_datetime(
            input['get_datetime']['without_seconds']['date'],
            input['get_datetime']['without_seconds']['time']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_datetime(
                input['get_datetime']['error']['date'],
                input['get_datetime']['error']['time']
            )

    def start_date_timedelta(self):
        tz = pytz.timezone("UTC")
        expected_result = expected['start_date_timedelta']['less']
        actual_result = standard_rotation.start_date_timedelta(
            input['start_date_timedelta']['less']['handoff_day'],
            input['start_date_timedelta']['less']['weekday'],
            datetime(2016, 8, 23, 0, 0, 0),
            tz
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['start_date_timedelta']['greater']
        actual_result = standard_rotation.start_date_timedelta(
            input['start_date_timedelta']['greater']['handoff_day'],
            input['start_date_timedelta']['greater']['weekday'],
            datetime(2016, 8, 23, 0, 0, 0),
            tz
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['start_date_timedelta']['equal']
        actual_result = standard_rotation.start_date_timedelta(
            input['start_date_timedelta']['equal']['handoff_day'],
            input['start_date_timedelta']['equal']['weekday'],
            datetime(2016, 8, 23, 0, 0, 0),
            tz
        )
        self.assertEqual(expected_result, actual_result)

    def get_weekday(self):
        expected_result = expected['get_weekday']['sunday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['sunday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['sunday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['sunday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['monday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['monday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['monday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['monday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['tuesday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['tuesday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['wednesday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['wednesday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['wednesday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['wednesday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['thursday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['thursday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['thursday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['thursday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['friday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['friday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['friday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['friday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['saturday1']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['saturday1']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['get_weekday']['saturday2']
        actual_result = standard_rotation.get_weekday(
            input['get_weekday']['saturday2']['weekday']
        )
        self.assertEqual(expected_result, actual_result)
        with self.assertRaises(ValueError):
            standard_rotation.get_weekday(
                input['get_weekday']['error1']['weekday']
            )
        with self.assertRaises(ValueError):
            standard_rotation.get_weekday(
                input['get_weekday']['error2']['weekday']
            )

    def nullify(self):
        expected_result = expected['nullify']['null']
        actual_result = standard_rotation.nullify(input['nullify']['null'])
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['nullify']['val1']
        actual_result = standard_rotation.nullify(input['nullify']['val1'])
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['nullify']['val2']
        actual_result = standard_rotation.nullify(input['nullify']['val2'])
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['nullify']['val3']
        actual_result = standard_rotation.nullify(input['nullify']['val3'])
        self.assertEqual(expected_result, actual_result)
        expected_result = expected['nullify']['val4']
        actual_result = standard_rotation.nullify(input['nullify']['val4'])
        self.assertEqual(expected_result, actual_result)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(StandardRotationTests('get_restriction_type'))
    suite.addTest(StandardRotationTests('get_rotation_turn_length'))
    suite.addTest(StandardRotationTests('get_virtual_start'))
    suite.addTest(StandardRotationTests('get_restriction_duration'))
    suite.addTest(StandardRotationTests('parse_csv'))
    suite.addTest(StandardRotationTests('get_datetime'))
    suite.addTest(StandardRotationTests('start_date_timedelta'))
    suite.addTest(StandardRotationTests('get_weekday'))
    suite.addTest(StandardRotationTests('nullify'))
    suite.addTest(StandardRotationTests('check_layers'))
    suite.addTest(StandardRotationTests('parse_layers'))
    suite.addTest(StandardRotationTests('parse_schedules'))
    return suite
