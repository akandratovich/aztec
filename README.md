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
    You can use `azs` to run Kotlin file like a script.

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


## Scripting

You can write scripts on Kotlin and execute them with `azs` command. Your scripts will be cached, so only first run will trigger the compilation:

    C:\devel-kotlin\euler>cat demo.kt
    println("hello world")

    C:\devel-kotlin\euler>azs demo.kt
    hello world
    time: 2.1970000267

    C:\devel-kotlin\euler>azs demo.kt
    hello world
    time: 0.0849997997284

On unix systems you can add `#!/usr/bin/env azs` at first line of file and make this script executable.

You can write code in command line for quick testing:

    C:\devel-kotlin\euler>azs "println(\"hello from command line\")"
    hello from command line

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
