
class WidgetLoader:
    def __init__(self, widget_dao, url_mapping):
        self.__widget_dao = widget_dao
        self.__url_mapping = url_mapping

    def update_widget_table(self):
        current_widgets_in_table = self.__widget_dao.get_widgets()

        for item in self.__url_mapping:
            if item.widget not in current_widgets_in_table:
                self.__widget_dao.add_widget(item.widget, item.url)

        for widget in current_widgets_in_table:
            if widget not in self.__get_widget_list_from_url_mapping():
                self.__widget_dao.delete_widget(widget)

    def __get_widget_list_from_url_mapping(self):
        widget_list = []
        for item in self.__url_mapping:
            widget_list.append(item.widget)
        return widget_list
