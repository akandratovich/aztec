#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import aztec.core
import sys

def az():
# if __name__ == '__main__':
  print "Aztec [https://github.com/kondratovich/aztec]"
    # print "Aztec is for automating Kotlin projects without setting your hair on fire."
  print "Aztec is for compiling Kotlin sources without setting your hair on fire."
  print "You can use `azs` to run Kotlin file like a script.\n"
  aztec.core.Aztec(sys.argv)
