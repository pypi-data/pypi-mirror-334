# -*- coding: utf-8 -*-
# *********************************************************************
# lewis - a library for creating hardware device simulators
# Copyright (C) 2016-2021 European Spallation Source ERIC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************

import unittest
from unittest.mock import call, patch

from lewis.core.processor import CanProcess, CanProcessComposite


class TestCanProcess(unittest.TestCase):
    def test_process_calls_doProcess(self):
        processor = CanProcess()

        with patch.object(processor, "doProcess", create=True) as do_process_mock:
            processor.process(1.0)

        do_process_mock.assert_called_once_with(1.0)

    def test_process_calls_doBeforeProcess_only_if_doProcess_is_present(self):
        processor = CanProcess()

        with patch.object(processor, "doBeforeProcess", create=True) as do_before_process_mock:
            processor.process(1.0)

            do_before_process_mock.assert_not_called()

            with patch.object(processor, "doProcess", create=True):
                processor.process(2.0)

            do_before_process_mock.assert_called_once_with(2.0)

    def test_process_calls_doAfterProcess_only_if_doProcess_is_present(self):
        processor = CanProcess()

        with patch.object(processor, "doAfterProcess", create=True) as do_after_process:
            processor.process(1.0)

            do_after_process.assert_not_called()

            with patch.object(processor, "doProcess", create=True):
                processor.process(2.0)

            do_after_process.assert_called_once_with(2.0)

    @patch.object(CanProcess, "process")
    def test_call_invokes_process(self, process_mock):
        processor = CanProcess()

        processor(45.0)

        process_mock.assert_called_once_with(45.0)


class TestCanProcessComposite(unittest.TestCase):
    def test_process_calls_doBeforeProcess_if_present(self):
        composite = CanProcessComposite()

        with patch.object(composite, "doBeforeProcess", create=True) as do_before_process_mock:
            composite.process(3.0)

        do_before_process_mock.assert_called_once_with(3.0)

    def test_addProcessor_if_argument_CanProcess(self):
        composite = CanProcessComposite()

        with patch.object(composite, "_append_processor") as append_processor_mock:
            composite.add_processor(CanProcess())

        self.assertEqual(append_processor_mock.call_count, 1)

    def test_addProcessor_if_argument_not_CanProcess(self):
        composite = CanProcessComposite()

        with patch.object(composite, "_append_processor") as append_processor_mock:
            composite.add_processor(None)

        append_processor_mock.assert_not_called()

    def test_init_from_iterable(self):
        with patch.object(CanProcess, "doProcess", create=True) as mock_process_method:
            devices = (
                CanProcess(),
                CanProcess(),
            )

            composite = CanProcessComposite(devices)
            composite(4.0)

            mock_process_method.assert_has_calls([call(4.0), call(4.0)])
