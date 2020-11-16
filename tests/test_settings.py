from base.file_plugin import load_file


class TestSettings:

    def setup(self):
        self.file_path = './../examples/settings.ini'
        self.instance_ini = load_file(self.file_path, load_type='ini')

    def test_ini_caps_msg(self):
        assert self.instance_ini.get('appium_caps', 'host') == '127.0.0.1'
        assert self.instance_ini.get('appium_caps', 'appium_port') == '4723'

    def test_ini_sections(self):
        sections = self.instance_ini.options('appium_caps')
        assert 'host' in sections
        assert 'appium_port' in sections

    def test_ini_value(self):
        # option_values = [(host, "127.0.0.1"), (appium_port, "4723")]
        option_values = self.instance_ini.items('appium_caps')
        assert '127.0.0.1' in option_values[0]
        assert '4723' in option_values[1]
        assert isinstance(option_values, list)