from aztec import core
import optparse
import os
import tempfile
import subprocess
import sys
import time
import shutil

__az__ = ['ListPlugin', 'CompilePlugin', 'HelpPlugin', 'JarPlugin', 'PackPlugin', 'CleanPlugin']

pack_unx ="""#!/bin/bash

function die() {
    echo "$1"
    exit 1
}

# Taken from Debian Developers Reference Chapter 6
function pathfind() {
     OLDIFS="$IFS"
     IFS=:
     for p in $PATH; do
         if [ -x "$p/$*" ]; then
             IFS="$OLDIFS"
             return 0
         fi
     done
     IFS="$OLDIFS"
     return 1
}

pathfind "java" || die "[ERROR] could not find: java in \$PATH"

exec java -jar $0 "$@"



"""

pack_win = "@echo off\n\r\"%s\" -jar %%0 %%*\n\rexit /b 0\n\r"


class ListPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def execute(self, argv):
    print "available options:"
    for po in self.ctx.plugins:
      p = self.ctx.get_plugin(po)
      print "\t%-20s%s %s" % (p.cmd(), ':', p.description())

  def cmd(self):
    return "list"

  def description(self):
    return "print list of installed plugins"

class CleanPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.set_usage("az clean [folder]")
    parser.set_description("remove all files from folder (default `output`)")
    return parser

  def execute(self, argv):
    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    output = os.path.abspath('output')
    if len(args) > 0:
      output = os.path.abspath(args[0])

    core.rmtree(output)

  def cmd(self):
    return "clean"

  def description(self):
    return "clean output directory"

class CompilePlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output",
                      help="change default output folder",
                      default=os.path.join(self.ctx.defaults['PROJECT_PATH'], "output"))
    parser.add_option("-s", "--src", dest="source",
                      default=self.ctx.defaults['PROJECT_PATH'],
                      help="set files for compilation")

    parser.set_usage("az compile [options]")
    return parser

  def execute(self, argv):
    """ compile kotlin source with KotlinCompiler"""

    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    source = os.path.abspath(options.source)
    output = os.path.abspath(options.output)
    core.dir_sure(output)

    cmd = []
    cmd.append(self.ctx.defaults['JAVA_PATH'])
    cmd.append("-cp")
    cmd.append(self.ctx.defaults['KOTLIN_CP'])
    cmd.append("org.jetbrains.jet.cli.KotlinCompiler")
    cmd.append("-includeRuntime")
    cmd.append("-output")
    cmd.append(output)
    cmd.append("-src")
    cmd.append(source)

    fail = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)

  def cmd(self):
    return "compile"

  def description(self):
    return "compile sources"

class PackPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output",
                      help="change default output folder",
                      default=os.path.join(self.ctx.defaults['PROJECT_PATH'], "output"))
    parser.add_option("-s", "--src", dest="source",
                      default=self.ctx.defaults['PROJECT_PATH'],
                      help="set files for compilation")

    parser.set_usage("az pack [options] name")
    return parser

  def execute(self, argv):
    """ compile kotlin source with KotlinCompiler"""

    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    if len(args) == 0:
      opts.print_help()
      exit(0)

    name = args[0]
    if os.name == 'nt':
      name += '.bat'

    source = os.path.abspath(options.source)
    output = os.path.abspath(options.output)
    core.dir_sure(output)

    jfile, jarfile = tempfile.mkstemp(suffix='.jar')

    cmd = []
    cmd.append(self.ctx.defaults['JAVA_PATH'])
    cmd.append("-cp")
    cmd.append(self.ctx.defaults['KOTLIN_CP'])
    cmd.append("org.jetbrains.jet.cli.KotlinCompiler")
    cmd.append("-includeRuntime")
    cmd.append("-jar")
    cmd.append(jarfile)
    cmd.append("-src")
    cmd.append(source)

    fail = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)

    if not fail:
      shell = (pack_win % self.ctx.defaults['JAVA_PATH']) if os.name == 'nt' else pack_unx
      of = os.path.join(output, name)
      fh_shell = open(of, 'w+b')
      fh_shell.write(shell)
      # fh_shell.write(shellstub)
      fh_jar   = open(jarfile, 'rb')
      shutil.copyfileobj(fh_jar, fh_shell)
      fh_shell.close()
      fh_jar.close()
      os.close(jfile)
      os.unlink(jarfile)
      os.chmod(of, 0755)

  def cmd(self):
    return "pack"

  def description(self):
    return "compile sources and pack them to executable file"

class JarPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output",
                      help="change default output folder",
                      default=os.path.join(self.ctx.defaults['PROJECT_PATH'], "output"))
    parser.add_option("-s", "--src", dest="source",
                      default=self.ctx.defaults['PROJECT_PATH'],
                      help="set files for compilation")

    parser.set_usage("az jar [options] name")
    return parser

  def execute(self, argv):
    """ compile kotlin source with KotlinCompiler"""

    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    if len(args) == 0:
      opts.print_help()
      exit(0)

    name = args[0]
    source = os.path.abspath(options.source)
    output = os.path.abspath(options.output)
    core.dir_sure(output)

    jarfile = os.path.join(output, name + '.jar')

    cmd = []
    cmd.append(self.ctx.defaults['JAVA_PATH'])
    cmd.append("-cp")
    cmd.append(self.ctx.defaults['KOTLIN_CP'])
    cmd.append("org.jetbrains.jet.cli.KotlinCompiler")
    cmd.append("-includeRuntime")
    cmd.append("-jar")
    cmd.append(jarfile)
    cmd.append("-src")
    cmd.append(source)

    subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)

  def cmd(self):
    return "jar"

  def description(self):
    return "compile sources and pack to jar"

class HelpPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.set_description("print documentation for COMMAND")
    parser.set_usage("az help [command]")
    return parser

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def execute(self, argv):
    if len(argv) == 1:
      p = self.ctx.get_command(argv[0])
      if p != None:
        if not p.doc():
          print "\t%-20s%s %s" % (p.cmd(), ':', p.description())
        return

    print "Aztec\t\t[https://github.com/kondratovich/aztec]"
    # print "Aztec is for automating Kotlin projects without setting your hair on fire."
    print "Aztec is for compiling Kotlin sources without setting your hair on fire."
    print "Usage: az [options]"
    print ""

    lp = self.ctx.get_plugin('ListPlugin')
    lp.execute(self.ctx)

  def cmd(self):
    return "help"

  def description(self):
    return "print help information"
