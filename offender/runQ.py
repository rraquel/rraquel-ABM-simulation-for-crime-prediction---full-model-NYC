#!/usr/bin/python3


import QRunner
a=QRunner.QRunner()
b={"run_id": 3, "step": 7, "agent":9, "way":[1,4,7,9] }
a.store_roads(b)
a.exit()

