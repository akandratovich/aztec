from aztec import core, cfg
import optparse
import os
import time
import tempfile

__az__ = ['ListPlugin', 'HelpPlugin', 'CleanPlugin', 'UpgradePlugin', 'VersionPlugin']


def ivy_version(btn, path = None):
  if path == None:
    azp = os.path.join(core.home_path(), '.az', 'core')
    path = os.path.join(azp, btn, 'teamcity-ivy.xml')

  bt = open(path, 'r')
  btc = bt.read()
  bt.close()

  return btc[btc.find('revision="') + 10:].split('"')[0]

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

  def _check(self):
    azp = os.path.join(core.home_path(), '.az', 'core')
    for km in core.kl:
      for bt in km:
        ivy = km[bt][0]

        url = core.jbtc + bt + '/latest.lastSuccessful/' + ivy
        fdivy, tivy = tempfile.mkstemp(suffix='.xml')
        core.download(url, tivy, False)

        btv0 = ivy_version(bt, tivy)
        btv1 = ivy_version(bt)
        os.close(fdivy)
        os.unlink(tivy)
        if btv0 != btv1:
          for lib in km[bt]:
            local = os.path.join(azp, bt, lib)
            os.remove(local)

  def execute(self, argv):
    opts = self.make_opts()
    (options, args) = opts.parse_args(argv)

    if options.force:
      azp = os.path.join(core.home_path(), '.az', 'core')
      core.rmtree(azp)
    else:
      self._check()

    self.ctx.defaults['KOTLIN_CP'] = core.find_kotlin()

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

    print "Kotlin compiler version : %s" % ivy_version('bt344')
    print "Core libraries version  : %s" % ivy_version('bt343')

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
