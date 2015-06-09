# Copyright 2013 Intel Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Tests for Compute Driver CPU resource monitor."""

from nova.compute.monitors import virt
from nova import test


class ComputeDriverCPUMonitorTestCase(test.NoDBTestCase):
    def setUp(self):
        super(ComputeDriverCPUMonitorTestCase, self).setUp()

        class FakeDriver(object):
            def get_host_cpu_stats(self):
                return {'kernel': 5664160000000,
                        'idle': 1592705190000000,
                        'frequency': 800,
                        'user': 26728850000000,
                        'iowait': 6121490000000}

        class FakeComputeManager(object):
            driver = FakeDriver()

        self.monitor = virt.ComputeDriverCPUMonitor(FakeComputeManager())

    def test_get_metric_names(self):
        names = self.monitor.get_metric_names()
        self.assertEqual(10, len(names))
        self.assertIn("cpu.frequency", names)
        self.assertIn("cpu.user.time", names)
        self.assertIn("cpu.kernel.time", names)
        self.assertIn("cpu.idle.time", names)
        self.assertIn("cpu.iowait.time", names)
        self.assertIn("cpu.user.percent", names)
        self.assertIn("cpu.kernel.percent", names)
        self.assertIn("cpu.idle.percent", names)
        self.assertIn("cpu.iowait.percent", names)
        self.assertIn("cpu.percent", names)

    def test_get_metrics(self):
        metrics_raw = self.monitor.get_metrics()
        names = self.monitor.get_metric_names()
        metrics = {}
        for metric in metrics_raw:
            self.assertIn(metric['name'], names)
            metrics[metric['name']] = metric['value']

        self.assertEqual(metrics["cpu.frequency"], 800)
        self.assertEqual(metrics["cpu.user.time"], 26728850000000)
        self.assertEqual(metrics["cpu.kernel.time"], 5664160000000)
        self.assertEqual(metrics["cpu.idle.time"], 1592705190000000)
        self.assertEqual(metrics["cpu.iowait.time"], 6121490000000)
        self.assertTrue(metrics["cpu.user.percent"] <= 1
                        and metrics["cpu.user.percent"] >= 0)
        self.assertTrue(metrics["cpu.kernel.percent"] <= 1
                        and metrics["cpu.kernel.percent"] >= 0)
        self.assertTrue(metrics["cpu.idle.percent"] <= 1
                        and metrics["cpu.idle.percent"] >= 0)
        self.assertTrue(metrics["cpu.iowait.percent"] <= 1
                        and metrics["cpu.iowait.percent"] >= 0)
        self.assertTrue(metrics["cpu.percent"] <= 1
                        and metrics["cpu.percent"] >= 0)
