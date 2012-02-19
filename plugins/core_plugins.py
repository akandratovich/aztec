import core
import optparse
import os
import tempfile
import subprocess
import sys
import shutil

__az__ = ['ListPlugin', 'CompilePlugin', 'HelpPlugin']

shellstub ="""#!/bin/bash

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

class CompilePlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def parse_argv(self, argv):
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output",
                      help="change default output folder",
                      default=os.path.join(self.ctx.defaults['PROJECT_PATH'], "output"))
    parser.add_option("-s", "--src", dest="source",
                      default=self.ctx.defaults['PROJECT_PATH'],
                      help="set files for compilation")
    parser.add_option("-n", "--name", dest="name",
                      help="set name for jar or pack file")
    parser.add_option("-p", "--pack", action="store_true", dest="pack",
                      help="create executable file", default=False)
    parser.add_option("-j", "--jar", action="store_true", dest="jar",
                      help="create jar file", default=False)
    
    parser.set_usage("az compile [options]")
    (options, args) = parser.parse_args(argv)

    if len(argv) == 0:
      parser.print_help()
      exit(0)

    return options
  
  def execute(self, argv):
    """ compile kotlin source with KotlinCompiler"""

    options = self.parse_argv(argv)
    name = options.name
    jar = options.jar
    pack = (not jar) and options.pack
    if name == None:
      jar = False
      pack = False
    
    source = os.path.abspath(options.source)
    output = os.path.abspath(options.output)
    if os.path.exists(output):
      shutil.rmtree(output)
    core.parent_sure(output)

    cmd = []
    cmd.append(self.ctx.defaults['JAVA_PATH'])
    cmd.append("-cp")
    cmd.append(self.ctx.defaults['KOTLIN_CP'])
    cmd.append("org.jetbrains.jet.cli.KotlinCompiler")
    cmd.append("-includeRuntime")

    if jar or pack:
      of = os.path.join(output, name)
      core.parent_sure(of)

      jarfile = None
      if jar:
        jarfile = (of + '.jar')
      if pack:
        _, jarfile = tempfile.mkstemp(suffix='.jar')
      
      cmd.append("-jar")
      cmd.append(jarfile)
    else:
      cmd.append("-output")
      cmd.append(output)
    
    cmd.append("-src")
    cmd.append(source)

    fail = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)

    if not fail and pack:
        fh_shell = open(of, 'w+b')
        fh_shell.write(shellstub)
        fh_jar   = open(jarfile, 'r')
        fh_shell.write(fh_jar.read())
        fh_shell.close()
        fh_jar.close()
        os.unlink(jarfile)
        os.chmod(of, 0755)
  
  def cmd(self):
    return "compile"
  
  def description(self):
    return "compile sources"

class HelpPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx
  
  def doc(self):
    print "\t%-20s %s %s" % ((self.cmd() + ' [command]'), ':', self.description())
    print "\t%-20s %s " % ("", ": when `COMMAND` specified print documentation for command")
    return True

  def execute(self, argv):
    if len(argv) == 1:
      p = self.ctx.get_command(argv[0])
      if p != None:
        if not p.doc():
          print "\t%-20s%s %s" % (p.cmd(), ':', p.description())
          return
        return
    
    print "Aztec v0.1\t\t[https://github.com/kondratovich/aztec]"
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