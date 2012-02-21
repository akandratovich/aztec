from setuptools import setup, find_packages

log = open('./.git/logs/HEAD', 'r')
log_data = log.read()
log.close()

data = filter(lambda e: len(e) > 0, log_data.split("\n"))[-1]

cdata = data.split(" ")[1]
print cdata

ldata = data.split("> ")[-1].split(" ")[0]
print ldata

cfgf = open('./aztec/cfg.py', 'w')
cfgf.write("""
aztec_commit = \'%s\'
aztec_time = %s
""" % (cdata, ldata))
cfgf.close()


setup(
    name = "Aztec",
    version = "1",
    packages = find_packages(),

    # metadata for upload to PyPI
    author = "Andrew Kondratovich",
    author_email = "andrew.kondratovich@gmail.com",
    description = "Aztec is build tool for Kotlin",
    keywords = "aztec kotlin buildtool",
    url = "http://github.com/kondratovich/aztec",
    entry_points = {
        'console_scripts': [
            'az = aztec.az:az'
        ]
    }
)
