import sys
import os
import imp
import urllib
import urllib2
import shutil

# http://teamcity.jetbrains.com/guestAuth/repository/download/bt343/latest.lastSuccessful/
asmr = "https://oss.sonatype.org/service/local/repositories/central/content/"
asml = 'asm/asm-util/3.3.1/asm-util-3.3.1.jar'

jbtc = 'http://teamcity.jetbrains.com/guestAuth/repository/download/'
kl = [
  {'bt343': [
      'teamcity-ivy.xml',
      'core/asm-commons.jar',
      'core/guava-11.0.1.jar',
      'core/intellij-core.jar',
      'core/cli-10.jar',
      'core/trove4j.jar',
      'core/annotations.jar',
      'core/asm.jar',
      'core/picocontainer.jar'
  ]},
  {'bt344': [
      'teamcity-ivy.xml',
      'kotlin-build-tools.jar',
      'kotlin-compiler.jar',
      'kotlin-runtime.jar'
  ]}
]

def find_java():
    """ checks whether `java` can be found in system environment"""
    # executable already contains a path.
    executable = 'java.exe' if os.name == 'nt' else 'java'
    if os.path.dirname(executable) != '':
      if os.access(executable, os.X_OK):
        return executable

    if os.environ.has_key('JDK_HOME'):
      f = os.path.join(os.environ['JDK_HOME'], 'bin', executable)
      if os.access(f, os.X_OK):
        return f

    if os.environ.has_key('JAVA_HOME'):
      f = os.path.join(os.environ['JAVA_HOME'], 'bin', executable)
      if os.access(f, os.X_OK):
        return f

    if not os.environ.has_key('PATH') or os.environ['PATH'] == '':
      p = os.defpath
    else:
      p = os.environ['PATH']

    pathlist = p.split(os.pathsep)

    for path in pathlist:
      f = os.path.join(path, executable)
      if os.access(f, os.X_OK):
        return f

    return None

def check_and_download(path, dest, check):
  if not os.path.exists(dest):
    download(path, dest)

  if check:
    request = urllib2.Request(path)
    request.get_method = lambda : 'HEAD'

    response = urllib2.urlopen(request)
    clh = response.headers['Content-Length']
    if clh != None:
      cl = long(clh)
      if cl != os.path.getsize(dest):
        os.remove(dest)
        download(path, dest)

def download(path, dest):
  print '\t[GET] %s' % path
  parent_sure(dest)
  (_, message) = urllib.urlretrieve(path, dest)

  clh = message.getheader('content-length')
  if clh != None:
    cl = long(clh)
    if cl != os.path.getsize(dest):
      print "\t[ERROR] could not download %s" % path
      os.remove(dest)

def rmtree(path):
  if not os.path.exists(path):
    return

  try:
    shutil.rmtree(path)
  except OSError, e:
    print "\t[ERROR] could not remove folder `%s`" % path

def dir_sure(path):
  if os.path.exists(path):
    return path

  os.makedirs(path)
  return path

def parent_sure(path0):
  path = os.path.abspath(os.path.join(path0, os.path.pardir))
  return dir_sure(path)

def home_path():
  if 'HOME' in os.environ:
    return os.environ['HOME']
  return os.environ['USERPROFILE']

def find_kotlin(check=False):
  azp = dir_sure(os.path.join(home_path(), '.az', 'core'))

  cps = []
  check_and_download(asmr + asml, os.path.join(azp, asml), check)
  cps.append(os.path.join(azp, asml))

  for km in kl:
    for bt in km:
      for jar in km[bt]:
        local = os.path.join(azp, bt, jar)
        check_and_download(jbtc + bt + '/latest.lastSuccessful/' + jar, local, check)
        cps.append(local)

  return os.pathsep.join(cps)

def die(fmt, *args):
    """ print something to stderr and exit(1) """
    if args:
        sys.stderr.write(fmt%(args))
    else:
        sys.stderr.write("%s"%(fmt))
    sys.exit(1)

class Context(object):
  def __init__(self):
    defaults = {}
    defaults['AZ_PATH'] = sys.modules['aztec'].__path__[0]
    defaults['JAVA_PATH'] = find_java()
    defaults['KOTLIN_CP'] = find_kotlin()
    defaults['PROJECT_PATH'] = os.path.abspath(os.path.join("./"))

    plugins = {}
    plgs = os.listdir(os.path.join(defaults['AZ_PATH'], "plugins"))
    for f in plgs:
      fn = f[-3:]
      if fn == '.py':
        pn = imp.load_source(f[:-3], os.path.join(defaults['AZ_PATH'], "plugins", f))
        try:
          clsns = filter(lambda i: i in pn.__az__, pn.__dict__)
          for c in clsns:
            plugins[c] = pn.__dict__[c]
        except AttributeError as e:
          pass

    if not defaults['JAVA_PATH']:
        die("[ERROR] could not find java\n")

    if not defaults['KOTLIN_CP']:
        die("[ERROR] could not find or download Kotlin\n")

    self.plugins = plugins
    self.defaults = defaults

  def get_plugin(self, name):
    if name not in self.plugins:
      return None
    return self.plugins[name](self)

  def get_command(self, command):
    for name in self.plugins:
      p = self.plugins[name](self)
      if p.cmd() == command:
        return p

    return None

class Plugin(object):
  def doc(self):
    return False

  def execute(self, *arg):
    pass

  def cmd(self):
    pass

  def description(self):
    pass

class Aztec(object):
  def __init__(self, argv):
    self.ctx = Context()
    self.parse_argv(argv)

  def parse_argv(self, argv):
    if len(argv) < 2:
      self.help()
      return

    command = argv[1]
    argv0 = argv[2:]

    p = self.ctx.get_command(command)
    if p == None:
      print "[ERROR] could not recognize command `%s`" % command
      return

    p.execute(argv0)

  def help(self):
    hp = self.ctx.get_plugin('HelpPlugin')
    if hp == None:
      return

    hp.execute([])
