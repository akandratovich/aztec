from aztec import core, cfg
import optparse
import os
import time

__az__ = ['ListPlugin', 'HelpPlugin', 'CleanPlugin', 'UpgradePlugin', 'VersionPlugin']


class UpgradePlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.add_option("-f", "--force", action="store_true",
                      help="force reload of libraries",
                      default=False)

    parser.set_usage("az upgrade [options]")
    return parser

  def execute(self, argv):
    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    if options.force:
      azp = os.path.join(core.home_path(), '.az', 'core')
      core.rmtree(azp)

    self.ctx.defaults['KOTLIN_CP'] = core.find_kotlin(True)

  def cmd(self):
    return "upgrade"

  def description(self):
    return "upgrade kotlin libraries upto last version"

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

class VersionPlugin(core.Plugin):
  def __init__(self, ctx):
    self.ctx = ctx

  def doc(self):
    opts = self.make_opts()
    opts.print_help()
    return True

  def make_opts(self):
    parser = optparse.OptionParser()
    parser.set_usage("az version")
    parser.set_description("show version of Aztec and Kotlin")
    return parser

  def execute(self, argv):
    print "Aztec commit            : %s" % cfg.aztec_commit
    print "Aztec commit time       : %s" % time.ctime(cfg.aztec_time)

    azp = os.path.join(core.home_path(), '.az', 'core')

    bt343 = open(os.path.join(azp, 'bt343', 'teamcity-ivy.xml'), 'r')
    bt343c = bt343.read()
    bt343.close()

    bt344 = open(os.path.join(azp, 'bt344', 'teamcity-ivy.xml'), 'r')
    bt344c = bt344.read()
    bt344.close()

    bt343v = bt343c[bt343c.find('revision="') + 10:].split('"')[0]
    bt344v = bt344c[bt344c.find('revision="') + 10:].split('"')[0]

    print "Kotlin compiler version : %s" % bt344v
    print "Core libraries version  : %s" % bt343v

  def cmd(self):
    return "version"

  def description(self):
    return "show version"

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

    print "Usage: az [options]"
    print ""

    lp = self.ctx.get_plugin('ListPlugin')
    lp.execute(self.ctx)

  def cmd(self):
    return "help"

  def description(self):
    return "print help information"
