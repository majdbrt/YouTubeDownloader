from pytube import YouTube
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QLabel

class MainWindow(QMainWindow):
    def __init__(self, video):
        super().__init__()
        self.streamInfo = video
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.general_layout = QVBoxLayout()

        self.setWindowTitle('YouTube Downloader')

        self.status = QStatusBar()

        self.setStatusBar(self.status)

        # select folder/directory implementation
        self.error_msg_directory = 'Error! Download destination is not selected.'
        self.select_directory_layout = QHBoxLayout()
        self.select_directory_button = QPushButton('...')
        self.select_directory_box = QLineEdit()
        self.select_directory_layout.addWidget(self.select_directory_box)
        self.select_directory_layout.addWidget(self.select_directory_button)

        self.general_layout.addLayout(self.select_directory_layout)

        self.select_directory_button.clicked.connect(self.changeDirectory)
        self.select_directory_box.textChanged.connect(self.getDirectory)

        # url text box implementation
        self.error_msg_url = 'Connot retrieve video'
        self.url_layout = QFormLayout()
        self.url_box = QLineEdit()
        self.url_layout.addRow("Enter YouTube's video url: ", self.url_box)

        self.general_layout.addLayout(self.url_layout)

        self.url_box.textChanged.connect(self.getYoutubeStreams)

        # Download button implementation
        self.download_button = QPushButton('Download')
        self.general_layout.addWidget(self.download_button)
        self.download_button.clicked.connect(self.download_stream)

        self.main_widget.setLayout(self.general_layout)

    def changeDirectory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.select_directory_box.setText(folder)
        self.status.clearMessage()

    def getDirectory(self):
        self.streamInfo.directory = self.select_directory_box.text()

    def getYoutubeStreams(self, url):
        self.status.clearMessage()
        if self.url_box.text() != '':
            try:
                video = YouTube(url)
                self.streamInfo.url = url
                self.new_widget = Stream_Widget(video, self.streamInfo)
                self.new_widget.show()

            except:
                self.status.showMessage(self.error_msg_url)
                self.setStatusBar(self.status)

        else:
            self.status.clearMessage()

    def download_stream(self):
        self.status.clearMessage()
        if self.streamInfo.isNone() == False:
            stream = YouTube(self.streamInfo.url)
            chosenStream = stream.streams.get_by_itag(self.streamInfo.itag)
            try:
                chosenStream.download(self.streamInfo.directory)
                self.status.showMessage('Sucessfuly Downloaded!')
            except:
                self.status.showMessage(self.error_msg_directory)
        else:
            self.status.showMessage('Fill all the required information!')


class Stream_Widget(QWidget):
    def __init__(self, video, streamInfo):
        super().__init__()
        self.video = video
        self.streamInfo = streamInfo
        self.setWindowTitle('YouTube Downloader')
        self.general_layout = QVBoxLayout()

        self.select_format_layout = QHBoxLayout()

        self.mp3_button = QRadioButton('mp3')
        self.mp4_button = QRadioButton('mp4')

        self.streams_dict = dict()

        self.stream_selection_box = QLineEdit()
        self.continue_button = QPushButton('Continue')

        self.select_format_layout.addWidget(self.mp3_button)
        self.select_format_layout.addWidget(self.mp4_button)

        self.general_layout.addLayout(self.select_format_layout)
        self.setLayout(self.general_layout)

        self.mp4_button.toggled.connect(self.show_streams)
        self.continue_button.clicked.connect(self.get_stream_type)

    def get_stream(self):
        streams = self.video.streams.filter(file_extension='mp4', progressive=True)

        for stream in streams:
            streamStr = str(stream).split()
            itag = None
            res = None
            for word in streamStr:
                if 'itag' in word:
                    itag = word.strip('itag="')
                elif 'res=' in word:
                    res = word.strip('res="')
            # for

            self.streams_dict[itag] = res
        # for

    def show_streams(self):
        self.streamInfo.type = 'mp4'
        self.get_stream()
        self.general_layout.addWidget(QLabel('Available streams:'))

        for itag in self.streams_dict:
            self.general_layout.addWidget(QLabel(self.streams_dict[itag]))
        self.general_layout.addWidget(QLabel('Please enter the desired stream:'))
        self.general_layout.addWidget(self.stream_selection_box)
        self.general_layout.addWidget(self.continue_button)

    def get_stream_type(self):
        stream_exists = False
        for itag in self.streams_dict:
            if self.stream_selection_box.text() == self.streams_dict[itag]:
                stream_exists = True

        if stream_exists == False:
            self.stream_selection_box.setText('Invalid stream!')
        else:
            self.streamInfo.quality = self.stream_selection_box.text()
            for itag in self.streams_dict:
                if self.streams_dict[itag] == self.streamInfo.quality:
                    self.streamInfo.itag = itag
            self.close()


