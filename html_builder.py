import os

JS_FILENAME_END = 'Eval.js'
HTML_FILENAME_END = 'Widget.html'

class HtmlBuilder:
    def __init__(self, js_dir, html_dir):
        self.__js_dir = js_dir
        self.__html_dir = html_dir

    def build_html(self):
        html_files, js_files = self.__scan_html_js_files()

    def __load_file(self, path):
        with open(path) as fh:
            return fh.read()

    def __scan_html_js_files(self):
        html_files = []
        js_files = []
        for file in os.listdir(self.__js_dir):
            if file.endswith(JS_FILENAME_END):
                js_files.append(os.path.join(self.__js_dir, file))
        for file in os.listdir(self.__html_dir):
            if file.endswith(HTML_FILENAME_END):
                print(os.path.join(self.__html_dir, file))
        return html_files, js_files

    def sort_js_html_files(self, html_files, js_files):


    def __prepare_injection(self):
        pass


