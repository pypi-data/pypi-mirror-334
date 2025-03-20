#!/usr/bin/env python

import os
import sys

import django
from django.conf import (
    settings,
)
from django.test.utils import (
    get_runner,
)


if __name__ == '__main__':
    """"""
    # project_path = os.path.dirname(__file__)
    # sys.path.insert(0, os.path.join(project_path, '../../../gisdo/src'))

    django.setup()
    TestRunner = get_runner(settings, test_runner_class='gisdo.tests.KeepDatabaseTestRunner')
    test_runner = TestRunner()
    failures = test_runner.run_tests(['gisdo.tests.checklist_tests'])
    sys.exit(bool(failures))
