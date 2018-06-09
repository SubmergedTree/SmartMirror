import os

JS_FILENAME_END = 'Eval.js'
HTML_FILENAME_END = 'Widget.html'
JS_FILENAME_END_CHAR_COUNT = len(JS_FILENAME_END)
HTML_FILENAME_END_CHAR_COUNT = len(HTML_FILENAME_END)
JS_INJECT_TEMPLATE = 'const {} = {}'
END_SCRIPT_TAG = '</script>'


class HtmlBuilder:
    def __init__(self, js_dir, html_dir, index_html_path):
        self.__js_dir = js_dir
        self.__html_dir = html_dir
        self.__index_html_path = index_html_path

    def build_html(self):
        html_files, js_files = self.__scan_html_js_files()
        js_html_dict = self.__sort_js_html_files(html_files, js_files)
        prepared_js_list = self.__inject_html_in_js(js_html_dict)
        return self.__inject_to_index_html(prepared_js_list)

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

    def __sort_js_html_files(self, html_files, js_files):
        result = {}
        for js in js_files:
            js_without_ending = js[:-JS_FILENAME_END_CHAR_COUNT]
            html_found = ''
            for html in html_files:
                html_without_ending = html[:-HTML_FILENAME_END_CHAR_COUNT]
                if js_without_ending == html_without_ending:
                    html_found = html
                    break
            result.update({js_without_ending: (js, html_found)})
        return result

    def __inject_html_in_js(self, js_html_dict):
        prepared_js =[]
        for key, paths in js_html_dict.items():
            js = self.__load_file(self.__js_dir + paths[0])
            if paths[1] is not '':
                html = self.__load_file(self.__html_dir + paths[1])
                js = JS_INJECT_TEMPLATE.format(key + 'Html', html) + '\n' + js
            prepared_js.append(js)
        return prepared_js

    def __inject_to_index_html(self, js_list):
        full_js = ''
        for js in js_list:
            full_js = full_js + js
        index_html = self.__load_file(self.__index_html_path)
        index_end_script_tag = index_html.find(END_SCRIPT_TAG) + len(END_SCRIPT_TAG)
        index_html_with_js = index_html[:index_end_script_tag] + full_js + index_html[index_end_script_tag:]
        return index_html_with_js
