#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import aztec.core as core
import tempfile
import sys
import os
import hashlib
import subprocess


main_stub = "fun main(args : Array<String>) {\n\r%s\n\r}"

def write_source(source):
  fd, fp = tempfile.mkstemp(suffix='.kt')
  os.write(fd, main_stub % source)
  os.close(fd)
  return fp

def _hash(fp):
  f = open(fp, "r")
  data = f.read()
  f.close()
  return hashlib.sha224(data).hexdigest()

def azc():
  return core.dir_sure(os.path.join(core.home_path(), '.az', 'cache'))

def get_compiled(path):
  shj = _hash(path)
  ex = os.path.join(azc(), shj + '.jar')
  if os.path.exists(ex):
    return ex

  core.Aztec([sys.argv[0], "jar", "-o", azc(), "-s", path, shj])
  return ex

def run(path, argv):
  cmd = []
  cmd.append(core.find_java())
  cmd.append("-cp")
  cmd.append(core.find_kotlin())
  cmd.append("-jar")
  cmd.append(path)
  subprocess.call(cmd + argv, stdout=sys.stdout, stderr=sys.stderr)

def cut(path):
  f = open(path, "r")
  data = f.read().strip()
  f.close()
  if data[0] == '#':
    data = '//' + data
  return data

def azs():
  if len(sys.argv) < 2:
    return

  sp = sys.argv[1]
  uf = os.path.exists(sp)
  source = write_source(cut(sp) if uf else sp)
  if not os.path.exists(source):
    print "\t[ERROR] could not find `%s`" % source
    return

  jpath = get_compiled(source)
  os.unlink(source)

  if not os.path.exists(jpath): return
  run(jpath, sys.argv[2:])
