from widget.widget import Widget


class WidgetResolver:
    def __init__(self, api_keys, widget_user_dao, widget_dao):
        self.__api_keys = api_keys
        self.__widget_user_dao = widget_user_dao
        self.__widget_dao = widget_dao

    def process_widgets(self, username):
        widgets = []
        mapping_table = self.__widget_user_dao.get_mapping(username)
        for mapping in mapping_table:
            widgets.append(Widget(mapping.widget, self.__build_url(mapping.widget),
                                  mapping.position, mapping.context))
        return widgets

    def __build_url(self, widget):
        url = self.__widget_dao.get_base_url(widget)
        if widget in self.__api_keys:
            api_key = self.__api_keys[widget]
            url = url + '?' + api_key.name + '=' + api_key.key
        return url
