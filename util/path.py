
def string_after_last_slash(to_cut):
    cut_list = to_cut.split('/')
    if len(cut_list) == 0:
        return ''
    else:
        return cut_list[-1]


def compare_filenames_in_path(first, second):
    name_first = string_after_last_slash(first)
    name_second = string_after_last_slash(second)
    return name_first == name_second
