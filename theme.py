class Gruvbox:
    def __init__(self):
        self.background = "#282828"
        self.red = "#cc241d"
        self.green = "#98971a"
        self.yellow = "#d79921"
        self.blue = "#458588"
        self.purple = "#b16286"
        self.aqua = "#689d6a"
        self.gray = "#a89984"
        self.orange = "#d65d0e"
        self.bright_red = "#fb4934"
        self.bright_green = "#b8bb26"
        self.bright_yellow = "#fabd2f"
        self.bright_blue = "#83a598"
        self.bright_purple = "#d3869b"
        self.bright_aqua = "#8ec07c"
        self.bright_orange = "#fe8019"

        self.foreground = "#ebdbb2"
        self.foreground0 = "#fbf1c7"
        self.foreground1 = "#ebdbb2"
        self.foreground2 = "#d5c4a1"
        self.foreground3 = "#bdae93"
        self.foreground4 = "#a89984"

        self.background0 = "#282828"
        self.background1 = "#3c3836"
        self.background2 = "#504945"
        self.background3 = "#665c54"
        self.background4 = "#7c6f64"

    @property
    def main_background(self):
        return self.background

    @property
    def main_foreground(self):
        return self.foreground

    @property
    def icon_color(self):
        return self.bright_blue

    @property
    def model_color(self):
        return self.aqua

    @property
    def tag_background(self):
        return self.gray

    @property
    def tag_foreground(self):
        return self.background

    @property
    def selection_background(self):
        return self.background4

    @property
    def selection_foreground(self):
        return self.background

    @property
    def green_btn(self):
        return self.green

    @property
    def red_btn(self):
        return self.red

    @property
    def muted(self):
        return "#666666"


class Nord:
    def __init__(self):

        self.background = "#2e3440"
        self.foreground = "#d8dee9"
        self.comment = "#4c566a"
        self.red = "#bf616a"
        self.green = "#a3be8c"
        self.yellow = "#ebcb8b"
        self.blue = "#81a1c1"
        self.purple = "#b48ead"
        self.aqua = "#88c0d0"
        self.orange = "#d08770"
        self.bright_red = "#bf616a"
        self.bright_green = "#a3be8c"
        self.bright_yellow = "#ebcb8b"
        self.bright_blue = "#81a1c1"
        self.bright_purple = "#b48ead"
        self.bright_aqua = "#88c0d0"
        self.bright_orange = "#d08770"

        self.foreground0 = "#d8dee9"
        self.foreground1 = "#e5e9f0"
        self.foreground2 = "#eceff4"
        self.foreground3 = "#8fbcbb"
        self.foreground4 = "#88c0d0"

        self.background0 = "#2e3440"
        self.background1 = "#3b4252"
        self.background2 = "#434c5e"
        self.background3 = "#4c566a"
        self.background4 = "#5e81ac"

    @property
    def main_background(self):
        return self.background

    @property
    def main_foreground(self):
        return self.foreground

    @property
    def icon_color(self):
        return self.bright_blue

    @property
    def model_color(self):
        return self.green

    @property
    def tag_background(self):
        return self.orange

    @property
    def tag_foreground(self):
        return self.background0

    @property
    def selection_background(self):
        return self.background4

    @property
    def selection_foreground(self):
        return self.background

    @property
    def green_btn(self):
        return self.green

    @property
    def red_btn(self):
        return self.red

    @property
    def muted(self):
        return "#5b6880"


class Dracula:
    def __init__(self):
        self.background = "#282a36"
        self.current_line = "#44475a"
        self.foreground = "#f8f8f2"
        self.comment = "#6272a4"
        self.cyan = "#8be9fd"
        self.green = "#50fa7b"
        self.orange = "#ffb86c"
        self.pink = "#ff79c6"
        self.purple = "#bd93f9"
        self.red = "#ff5555"
        self.yellow = "#f1fa8c"

    @property
    def main_background(self):
        return self.background

    @property
    def main_foreground(self):
        return self.foreground

    @property
    def icon_color(self):
        return self.cyan

    @property
    def model_color(self):
        return self.green

    @property
    def tag_background(self):
        return self.red

    @property
    def tag_foreground(self):
        return self.background

    @property
    def selection_background(self):
        return self.comment

    @property
    def selection_foreground(self):
        return self.foreground

    @property
    def green_btn(self):
        return self.green

    @property
    def red_btn(self):
        return self.red

    @property
    def muted(self):
        return "#5f6380"
