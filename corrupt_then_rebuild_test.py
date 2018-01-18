#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2017 ScyllaDB

from avocado import main
from sdcm.tester import ClusterTester
from sdcm.nemesis import CorruptThenRebuildMonkey


class CorruptThenRebuildTest(ClusterTester):
    """
    :avocado: enable
    """
    def test_corrupt_then_rebuild_nodes(self):
        self.db_cluster.add_nemesis(nemesis=CorruptThenRebuildMonkey,
                                    loaders=self.loaders,
                                    monitoring_set=self.monitors)

        # run a prepare write workload
        stress_queue = self.run_stress_thread(stress_cmd=self.params.get('stress_write_cmd'),
                                              stress_num=1,
                                              keyspace_num=1)

        self.db_cluster.wait_total_space_used_per_node()
        self.verify_stress_thread(queue=stress_queue)

        self.db_cluster.start_nemesis(interval=15)
        self.db_cluster.stop_nemesis(timeout=1000)

        # READ part
        # stress_queue = self.run_stress_thread(stress_cmd=self.params.get('stress_read_cmd'),
        #                                       stress_num=2, keyspace_num=1)
        # self.get_stress_results(queue=stress_queue)


if __name__ == '__main__':
    main()
