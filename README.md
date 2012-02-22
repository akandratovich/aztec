# Aztec

Aztec is for compiling Kotlin sources without setting your hair on fire.

## Installation

Aztec is a python tool. So, to use it you need python.

Aztec uses `setuptools` package to install itself. If you haven't it, you can download it from [PyPi](http://pypi.python.org/pypi/setuptools) or install from repository.

1. `git clone https://github.com/kondratovich/aztec.git`
2. `cd aztec`
3. `sudo python setup.py install`

After that you can use Aztec by `az` command.

_First time you launch it, Aztec downloads required Kotlin libraries._

## Usage

You can type `az` to see help.

    andrew@andrew-u100 ~/dev/euler $ az
    Aztec [https://github.com/kondratovich/aztec]
    Aztec is for compiling Kotlin sources without setting your hair on fire.
    
    Usage: az [options]
    
    available options:
            clean               : clean output directory
            help                : print help information
            compile             : compile sources
            pack                : compile sources and pack them to executable file
            upgrade             : upgrade kotlin libraries upto last version
            list                : print list of installed plugins
            version             : show version
            jar                 : compile sources and pack them to jar

Type `az help [command]` for concrete command documentation.

    andrew@andrew-u100 ~/dev/euler $ az help pack
    Usage: az pack [options] name
    
    Options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output=OUTPUT
                            change default output folder
      -s SOURCE, --src=SOURCE
                            set files for compilation


## Plugins

Aztec built on plugin architecture. You can check sources for examples.

## Roadmap

*    Documentation and tutorials
*    Project / module automtic detection
*    IDEA project skeleton integration
*    Project dependencies support
*    Test support

## Contribution

Your ideas, issues and pull requests are welcome.