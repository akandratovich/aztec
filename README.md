# Aztec

Aztec is for compiling Kotlin sources without setting your hair on fire.

## Installation

Aztec bootstraps itself using the `az` python script. There is no separate install script for libraries. It installs its dependencies upon the first run, so the first run will take longer.

1. `git clone https://github.com/kondratovich/aztec.git`
2. Add folder to your `$PATH`.
3. Set it to be executable. (`chmod 755 az`)

## Compile

You can use `az compile` command.

    andrew@andrew-u100 ~/dev/euler $ ../aztec/az compile
    Usage: az compile [options]

    Options:
      -h, --help            show this help message and exit
      -o OUTPUT, --output=OUTPUT
                            change default output folder
      -s SOURCE, --src=SOURCE
                            set files for compilation
      -n NAME, --name=NAME  set name for jar or pack file
      -p, --pack            create executable file
      -j, --jar             create jar file

## Plugins

Aztec built on plugin architecture. You can check sources for examples.

## Roadmap

*    Documentation and tutorials
*    Project / module automtic detection
*    IDEA skeleton integration
*    Project dependencies support
*    Test support