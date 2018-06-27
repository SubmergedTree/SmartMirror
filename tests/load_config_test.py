import unittest
from loader.load_config import ConfigLoader, APIKey


class Values:
    Standard = "standard"
    Legacy = "legacy"
    Generic = "generic"
    Pi = "pi"


class LoadConfigTest(unittest.TestCase):

    def setUp(self):
        mapping = {"standard": Values.Standard, "legacy": Values.Legacy,
                   "generic":Values.Generic, "pi": Values.Pi}

        self.config_loader = ConfigLoader(default_web_engine=Values.Standard,
                                          default_camera=Values.Generic,
                                          default_server_port=999,
                                          default_widget_show_time=3000,
                                          mapping=mapping)

    '''it should return values defined in config file'''
    def test_load_config(self):
        should_api_key_dict = {"WeatherNow": APIKey("APPID", "*****"), "WeatherForecast": APIKey("APPID", "*****")}
        should_web_engine =  Values.Legacy
        should_camera = Values.Pi
        should_port = 5000
        should_show_time = 3000
        api_key_dict, config = self.config_loader.load("/tests/test_configs/test_config.json")

        self.assertEqual(config.server_port, should_port)
        self.assertEqual(config.camera, should_camera)
        self.assertEqual(config.web_engine, should_web_engine)
        self.assertEqual(config.widget_show_time, should_show_time)
        self.assertTrue(self.__compare_api_key_dict(api_key_dict, should_api_key_dict))

    '''it should return default config'''
    def test_load_malformed_config(self):
        api_key_dict, config = self.config_loader.load("/tests/test_configs/test_config2.json")

        self.assertEqual(config.server_port, 999)
        self.assertEqual(config.camera, Values.Generic)
        self.assertEqual(config.web_engine, Values.Standard)
        self.assertTrue(self.__compare_api_key_dict(api_key_dict, {}))

    '''it should return default config'''
    def test_load_malformed_config_invalid_json(self):
        api_key_dict, config = self.config_loader.load("/tests/test_configs/test_config2.json")

        self.assertEqual(config.server_port, 999)
        self.assertEqual(config.camera, Values.Generic)
        self.assertEqual(config.web_engine, Values.Standard)
        self.assertTrue(self.__compare_api_key_dict(api_key_dict, {}))

    '''it should return default config'''
    def test_load_config_malformed_api_key(self):
        api_key_dict, config = self.config_loader.load("/tests/test_configs/test_config3.json")

        self.assertEqual(config.server_port, 999)
        self.assertEqual(config.camera, Values.Generic)
        self.assertEqual(config.web_engine, Values.Standard)
        self.assertTrue(self.__compare_api_key_dict(api_key_dict, {}))

    def __compare_api_key_dict(self, is_dict, should_dict):
        try:
            for key, value in should_dict.items():
                if not (value.name == is_dict[key].name and value.key == is_dict[key].key):
                    return False
        except:
            return False
        return True