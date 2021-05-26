import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout

class WidgetWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.general_layout = QVBoxLayout()

        # select folder/directory implementation
        self.directoryText = None
        self.select_directory_layout = QHBoxLayout()
        self.select_directory_button = QPushButton('...')
        self.select_directory_box = QLineEdit()
        self.select_directory_layout.addWidget(self.select_directory_box)
        self.select_directory_layout.addWidget(self.select_directory_button)

        self.general_layout.addLayout(self.select_directory_layout)

        self.select_directory_button.clicked.connect(self.changeDirectory)
        self.select_directory_box.textChanged.connect(self.getDirectory)

        # url text box implementation
        self.url = None
        self.url_layout = QFormLayout()
        self.url_box = QLineEdit()
        self.url_layout.addRow("Enter YouTube's video url: ", self.url_box)

        self.general_layout.addLayout(self.url_layout)

        self.url_box.textChanged.connect(self.getURL)

        self.setLayout(self.general_layout)


    def changeDirectory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.select_directory_box.setText(folder)

    def getDirectory(self):
        self.directoryText = self.select_directory_box.text()
        print(self.directoryText)

    def getURL(self):
        self.url = self.url_box.text()
        print(self.url)





def main():
    app = QApplication(sys.argv)
    window = WidgetWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()