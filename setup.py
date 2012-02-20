from setuptools import setup, find_packages

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
