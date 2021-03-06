# Copyright 2013, Couchbase, Inc.
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from tests.base import ConnectionTestCase
from couchbase.result import ObserveInfo
from couchbase.user_constants import OBS_MASK, OBS_FOUND, OBS_PERSISTED

class ConnectionObserveTest(ConnectionTestCase):

    def test_single_observe(self):
        key = self.gen_key("test_single_observe")
        self.cb.set(key, "value")
        rv = self.cb.observe(key)
        grv = self.cb.get(key)
        print(rv)

        self.assertTrue(rv.success)
        self.assertIsInstance(rv.value, list)
        self.assertTrue(rv.value)

        found_master = False


        for oi in rv.value:
            self.assertIsInstance(oi, ObserveInfo)
            oi.cas
            oi.from_master
            self.assertEqual(oi.flags, oi.flags & OBS_MASK)

            if oi.from_master:
                found_master = True
                self.assertTrue(oi.flags & (OBS_FOUND) == OBS_FOUND)
                self.assertEqual(oi.cas, grv.cas)

        self.assertTrue(found_master)
        repr(oi)
        str(oi)

    def test_multi_observe(self):
        kexist = self.gen_key("test_multi_observe-exist")
        kmissing = self.gen_key("test_multi_observe-missing")
        self.cb.set(kexist, "value")
        self.cb.delete(kmissing, quiet=True)
        grv = self.cb.get(kexist)

        mres = self.cb.observe_multi((kexist, kmissing))
        self.assertTrue(mres.all_ok)
        self.assertEqual(len(mres), 2)

        v_exist = mres[kexist]
        v_missing = mres[kmissing]

        for v in (v_exist.value, v_missing.value):
            self.assertIsInstance(v, list)
            self.assertTrue(len(v))
            found_master = False

            for oi in v:
                self.assertIsInstance(oi, ObserveInfo)
                oi.flags
                oi.cas
                if oi.from_master:
                    found_master = True
