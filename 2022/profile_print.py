#!/usr/bin/env python3

import sys
import pstats
from pstats import SortKey


p = pstats.Stats(sys.argv[1])
p.sort_stats(SortKey.CUMULATIVE).print_stats()
