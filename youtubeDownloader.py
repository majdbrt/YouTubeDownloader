import sys
from PyQt5.QtWidgets import QApplication
from GUI import MainWindow

__author__ = 'Majd Barakat'
__version__ = "1.0.1"

class Stream:
    def __init__(self):
        """Class to contain video information"""
        self.url = None
        self.type = None
        self.quality = None
        self.itag = None
        self.directory = None

    def isNone(self):
        if self.url == None or self.type == None or self.quality == None or self.itag == None or self.directory == None:
            return True
        return False

def main():
    app = QApplication(sys.argv)
    video = Stream()
    window = MainWindow(video)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()