#!/usr/bin/env python
# Copyright (c) 2009-2019 Quan Xu <qxuchn@gmail.com>
#
# This module is free software. You can redistribute it and/or modify it under
# the terms of the MIT License, see the file COPYING included with this
# distribution.

from __future__ import print_function
import sys
import os

import pananse.pananse


def run(args):
    if not os.path.exists(args.samplestable):
        print("File %s does not exist!" % args.samplestable)
        sys.exit(1)

    a = pananse.pananse.Runenhancer(
        toolstable=args.toolstable, samplestable=args.samplestable, 
        outfile=args.outfile
    )
    print("bb")
    a.run_enhancer()

