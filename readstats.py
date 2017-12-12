#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pstats
p = pstats.Stats('profiler_stats')
p.sort_stats('cumulative').print_stats(20)
