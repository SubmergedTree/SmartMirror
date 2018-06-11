
def to_string_with_escape_sequences(string):
    inline_str = string.replace("\n", "\\n")
    return inline_str.replace("\"", "\\\"")
