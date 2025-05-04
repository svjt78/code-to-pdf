# code_to_pdf/vscodedark.py
from pygments.style import Style
from pygments.token import Comment, Keyword, Name, String, Number, Operator

class VSDarkPlus(Style):
    background_color = "#1e1e1e"
    default_style = ""
    styles = {
        Comment:       "italic #6A9955",
        Keyword:       "bold #569CD6",
        Name.Function: "#DCDCAA",
        Name.Class:    "#4EC9B0",
        String:        "#CE9178",
        Number:        "#B5CEA8",
        Operator:      "#d4d4d4",
    }
