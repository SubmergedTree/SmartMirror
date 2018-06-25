from root_dir import ROOT_DIR
import json


class APIKey:
    def __init__(self, name, key):
        self.name = name
        self.key = key


class Config:
    def __init__(self, web_engine, camera, server_port, widget_show_time):
        self.web_engine = web_engine
        self.camera = camera
        self.server_port = server_port
        self.widget_show_time = widget_show_time


class ConfigLoader:
    def __init__(self, default_web_engine, default_camera, default_server_port, default_widget_show_time, mapping):
        self.__default_web_engine = default_web_engine
        self.__default_camera = default_camera
        self.__default_server_port = default_server_port
        self.__default_widget_show_time = default_widget_show_time
        self.__mapping = mapping

    def __get_default_config(self):
        return Config(self.__default_web_engine, self.__default_camera,
                      self.__default_server_port, self.__default_widget_show_time)

    def __evaluate_simple(self, web_engine_str, camera_str):
        return self.__mapping[web_engine_str], self.__mapping[camera_str]

    def __api_keys_list_to_dict(self, api_key_list):
        api_key_dict = {}
        for item in api_key_list:
            widget = item["widget"]
            name = item["name"]
            key = item["key"]
            api_key_dict.update({widget: APIKey(name=name, key=key)})
        return api_key_dict

    def load(self, relative_path):
        full_path = ROOT_DIR + relative_path
        try:
            fh = open(full_path, "r")
            config_dict = json.load(fh)
            web_engine_str = config_dict["webEngine"]
            camera_str = config_dict["camera"]
            port = config_dict["serverPort"]
            widget_show_time = config_dict["widgetShowTime"]
            api_keys_list = config_dict["apiKeys"]
            web_engine, camera = self.__evaluate_simple(web_engine_str=web_engine_str, camera_str=camera_str)
            api_key_dict = self.__api_keys_list_to_dict(api_keys_list)
            return api_key_dict, Config(web_engine, camera, port, widget_show_time)
        except (IOError, KeyError, ValueError) as e:
            return {}, self.__get_default_config()
        # TODO: log error
        finally:
            try:
                fh.close()
            except Exception as e:
                pass
            # TODO: log error