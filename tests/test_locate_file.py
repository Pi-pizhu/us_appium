import os

from base.file_plugin import locate_file


class TestLocateFile:

    def test_locat_file(self):
        locate_abs_file = locate_file(os.getcwd(), "examples/capabilities.json")
        print(locate_abs_file)