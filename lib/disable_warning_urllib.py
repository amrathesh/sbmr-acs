#!/usr/bin/env python3

# Copyright (c) 2023, Arm Limited or its affiliates. All rights reserved.
# SPDX-License-Identifier : Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import warnings

try:
    import httplib
except ImportError:
    import http.client

warnings.filterwarnings("ignore")

# Hijack the HTTP lib logger message and Log only once
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.CRITICAL)
requests_log.propagate = False


class disable_warning_urllib:
    def do_nothing():
        return
