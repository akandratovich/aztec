from setuptools import setup, find_packages

commit = open('./.git/FETCH_HEAD', 'r')
commit_data = commit.read()
commit.close()

cdata = commit_data[:40]

log = open('./.git/logs/HEAD', 'r')
log_data = log.read()
log.close()

cp0 = log_data.find(cdata)
cp1 = log_data[cp0 + 40:].find('>')
cp = log_data[cp0 + cp1 + 42:]

ldata = cp.split(' ')[0]

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
