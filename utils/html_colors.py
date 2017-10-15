# class Colors:
#     black   = "171717"
#     red     = "C62828"
#     green   = "43A047"
#     orange  = "EF6C00"
#     blue    = "2979FF"
#     purple  = "651FFF"
#     cyan    = "00BFA5"
#     white   = "78909C"

#     b_black  = "424242"
#     b_red    = "E53935"
#     b_green  = "00C853"
#     b_orange = "FB8C00"
#     b_blue   = "2196F3"
#     b_purple = "7C4DFF"
#     b_cyan   = "64FFDA"
#     b_white  = "B0BEC5"

class Colors:
    red         = "F44336"
    pink        = "E91E63"
    purple      = "9C27B0"
    deep_purple = "673AB7"
    indigo      = "3F51B5"
    blue        = "2196F3"
    light_blue  = "03A9F4"
    cyan        = "00BCD4"
    teal        = "00BFA5"
    green       = "4CAF50"
    light_green = "8BC34A"
    lime        = "CDDC39"
    yellow      = "FFEB3B"
    amber       = "FFC107"
    orange      = "FF9800"
    deep_orange = "FF5722"
    brown       = "795548"
    grey        = "9E9E9E"
    blue_grey   = "607D8B"

    dark_grey   = "515151"

    black = "212121"
    white = "EDEDED"

    a_red         = "FF1744"
    a_pink        = "F50057"
    a_purple      = "D500F9"
    a_deep_purple = "651FFF"
    a_indigo      = "3D5AFE"
    a_blue        = "2979FF"
    a_light_blue  = "00B0FF"
    a_cyan        = "00E5FF"
    a_teal        = "1DE9B6"
    a_green       = "00E676"
    a_light_green = "76FF03"
    a_lime        = "C6FF00"
    a_yellow      = "FFEA00"
    a_amber       = "FFC400"
    a_orange      = "FF9100"
    a_deep_orange = "FF3D00"
    a_brown       = "8D6E63"
    a_grey        = "BDBDBD"
    a_blue_grey   = "78909C"

class Text:
    underscore = "<span style=\"text-decoration: underline\">{}</span>"
    bold       = "<strong>{}</strong>"
    italic     = "<em>{}</em>"
    strikethru = "<span style=\"text-decoration: line-through\">{}</span>"

def paint(text, color_name):
    if hasattr(Colors, color_name):
        return f"<span style=\"color: #{getattr(Colors, color_name)}\">{text}</span>"
    raise ValueError(f"invalid color name: {color_name}")

def back(text, color_name):
    if hasattr(Colors, color_name):
        return f"<span style=\"background-color: #{getattr(Colors, color_name)}\">{text}</span>"
    raise ValueError(f"invalid color name: {color_name}")

def attr(text, attr_name):
    if hasattr(Text, attr_name):
        return getattr(Text, attr_name).format(text)
    raise ValueError(f"invalid attribute name: {attr_name}")


# QScrollBar:vertical {
#     background: transparent;
#     border: transparent;
#     width: 15px;
#     margin: 22px 0 22px 0;
# }

# QScrollBar::handle:vertical {
#     background: #00bfa5;
#     min-height: 20px;
# }

# QScrollBar::add-line:vertical {
#     border: transparent;
#     background: transparent;
#     height: 20px;
#     border-width: 2px 0 0 0;
#     subcontrol-position: bottom;
#     subcontrol-origin: margin;
# }

# QScrollBar::sub-line:vertical {
#     border: transparent;
#     background: transparent;
#     height: 20px;
#     border-width: 0 0 2px 0;
#     subcontrol-position: top;
#     subcontrol-origin: margin;
# }

# QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
#     border: transparent;
#     width: 9px;
#     height: 9px;
#     background: transparent;
# }

#  QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
#      background: #515151;
#  }