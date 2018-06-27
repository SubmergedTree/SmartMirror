from util.path import get_files_in_dir

JS_FILENAME_END = 'Eval.js'


class WidgetLoader:
    def __init__(self, WidgetDao, js_dir_path):
        self.__widget_dao = WidgetDao
        self.__js_dir_path = js_dir_path

    def update_widget_table(self):
        js_files = get_files_in_dir(self.__js_dir_path)
        current_widgets_in_table = self.__widget_dao.get_widgets()
        widgets_in_dir = []
        for file in js_files:
            if file.endswith(JS_FILENAME_END):
                widgets_in_dir.append(file[:-len(JS_FILENAME_END)])

        for widget_in_table in current_widgets_in_table:
            if widget_in_table not in widgets_in_dir:
                self.__widget_dao.delete_widget(widget_in_table)

        for widget_in_dir in widgets_in_dir:
            if widget_in_dir not in current_widgets_in_table:
                self.__widget_dao.add_widget()