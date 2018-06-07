

# TODO When loading widgets (do rest call) in python evaluate usage of an async waterfall like structure
class WidgetController:

    def __init__(self, api_keys, widget_user_dao, widget_dao):
        self.__api_keys = api_keys
        self.__widget_user_dao = widget_user_dao
        self.__widget_dao = widget_dao

    def process_widgets(self, username):
        pass

    def __get_widget_user_mapping(self, username):
        mapping = self.__widget_user_dao.get_widget_position_context(username)

    def __build_url(self, widget):
        url = self.__widget_dao.get_base_url(widget)
        if widget in self.__api_keys:
            api_key = self.__api_keys[widget]
            url = url + '&' + api_key.name + '=' + api_key.key
        return url
