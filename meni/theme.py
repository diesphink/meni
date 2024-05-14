from PySide6 import QtGui


class BaseTheme:
    @property
    def stylesheet(self):
        return f"""
    
                DockTitleBar {{
                    background:rgba(0,0,0,0.1);
                }}

                DockTitleBar QLabel {{
                    background: transparent;
                }}

                DockTitleBar QPushButton {{
                    background: rgba(0, 0, 0, 0.1);
                    border: 0px solid white;
                    border-radius: 2px;
                }}

                DockTitleBar QPushButton::hover {{
                    background: rgba(0, 0, 0, 0.3);
                }}

                TagRow QLabel {{
                    background-color: palette(highlight);
                    color: palette(highlightedText);

                    opacity: 0.8;
                    font-size: 10px;
                    font-weight: bold;   

                    padding: 2px;
                    margin: 2px;
                    border-radius: 2px;
                }}
                
                BrowserDock QTreeView::item {{
                    padding: 3px 0px;
                }}
                
                WelcomeWindow QFrame {{
                    background-color: palette(light);   
                    aborder: none;                 
                }}    
                
                WelcomeWindow QLabel {{
                    background: transparent;
                    border: none;
                }}

                WelcomeWindow #path {{
                  border: 1px solid palette(mid);
                  padding: 5px;
                  border-radius: 5px;
                  background-color: palette(light);
                }}

                ViewerDock #title {{
                    font-size: 20px;
                    font-weight: bold;
                    text-decoration: underline;
                }}
                
                ViewerDock #path QLabel {{
                    font-size: 10px; opacity: 0.8;
                }}
                
                ViewerDock #collection QLabel {{
                    font-size: 10px;
                    opacity: 0.8;
                }}
                
                ImportDialog TitleLabel {{
                    font-size: 15px;
                    font-weight: bold;
                    text-decoration: underline;
                }}
                
                DragAndDropTarget QLabel {{
                    background-color: palette(light); 
                    padding: 30px; 
                    border: 2px dashed palette(mid); 
                    border-radius: 5px;
                    font-size: 17px;
                    text-align: center;
                }}
                
                QMenu {{
                    padding: 2px;
                }}

                MainWindow::separator {{
                    width: 4px;
                    border: none;
                    background:rgba(0,0,0,0.2);
                }}

                BrowserDock DeselectableTreeView {{
                    background: palette(window);
                }}

                QMenuBar {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                }}
                                
    """


class ColoredTheme(BaseTheme):
    @property
    def stylesheet(self):
        return f"""
                MainWindow, MainWindow *, WelcomeWindow, WelcomeWindow * {{
                    background-color: {self.main_background};
                    color: {self.main_foreground};
                    selection-background-color: {self.selection_background};
                    selection-color: {self.selection_foreground};
                }}

                {super().stylesheet}
    
                MainWindow::separator {{
                    background-color: rgba(0, 0, 0, 0.15);
                }}

                QPushButton#save:enabled, QPushButton#Ok:enabled {{
                    background-color: {self.green_btn};
                    color: #000;
                }}

                QPushButton#cancel:enabled {{
                    background-color: {self.red_btn};
                    color: #000;
                }}
                
                QLineEdit, QComboBox, QTextEdit, QPlainTextEdit {{
                    background-color: rgba(255, 255, 255, 0.05);
                    border: 1px solid rgba(0, 0, 0, 0.3);
                }}

                QTableView QLineEdit, QTableView QComboBox {{
                    background-color: {self.main_background};
                }}

                QTableView {{
                    gridline-color: rgba(0, 0, 0, 0.2);
                }}


                QMenu {{
                    border: 1px solid rgba(0, 0, 0, 0.2);
                    background-color: {self.main_background};
                    padding: 2px;
                }}
                
                TagRow QLabel {{
                    background-color: {self.tag_background};
                    color: {self.tag_foreground};
                }}

               
                #empty {{
                    color: rgba(255,255,255,0.2);
                }}

                BrowserDock DeselectableTreeView {{
                    background: transparent;
                }}
                
                
                WelcomeWindow QFrame {{
                    background-color: rgba(255, 255, 255, 0.01);
                }}    
                
                WelcomeWindow #path {{
                  border: 1px solid rgba(255,255,255, 0.2);
                  background-color: rgba(255,255,255, 0.1);
                }}
                
                DragAndDropTarget QLabel {{
                    background-color: rgba(255, 255, 255, 0.1); 
                    border: 2px dashed rgba(255, 255, 255, 0.2); 
                }}

                DockTitleBar {{
                    background:rgba(0,0,0,0.1);
                }}

                DockTitleBar QLabel {{
                    background: transparent;
                }}

            """


class Gruvbox(ColoredTheme):
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
    def name(self):
        return "Gruvbox"

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


class Nord(ColoredTheme):
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
    def name(self):
        return "Nord"

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


class Dracula(ColoredTheme):
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
    def name(self):
        return "Dracula"

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


class SystemDefault(BaseTheme):

    @property
    def name(self):
        return "System Default"

    @property
    def icon_color(self):
        return QtGui.QPalette().accent().color().name()

    @property
    def muted(self):
        muted = QtGui.QPalette().text().color()
        muted.setAlpha(100)
        return muted

    @property
    def model_color(self):
        return "#8be9fd"
