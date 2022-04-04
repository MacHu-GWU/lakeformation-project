# -*- coding: utf-8 -*-

import os

IS_CI = False
IS_LOCAL = False

if "CI" in os.environ:
    IS_CI = True
else:
    IS_LOCAL = True
