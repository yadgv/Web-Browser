# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import csv
import sys
from PyQt5.QtCore import Qt


class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(2560, 1440)  # Full 1440p resolution

        # Main browser window background
        self.background = QtWidgets.QWidget(Form)
        self.background.setGeometry(QtCore.QRect(0, 0, 2560, 1440))
        self.background.setStyleSheet("#background{background-color: rgb(212, 212, 212);}")
        self.background.setObjectName("background")

        # Top bar for navigation
        self.TopBar = QtWidgets.QWidget(self.background)
        self.TopBar.setGeometry(QtCore.QRect(20, 20, 2520, 100)) 
        self.TopBar.setStyleSheet(
            """
            #TopBar{background-color: rgb(0, 0, 0); border-radius: 25%; }
            QPushButton{color: rgb(255, 255, 255); background-color: rgb(0, 0, 0); border-radius: 50%; font-size: 30px;}
            QPushButton:hover{font-size: 40px;}
            QPushButton:pressed{font-size: 45px;}
            #refreshButton{font-size: 45px;}
            #refreshButton:hover{font-size: 46px;}
            #refreshButton:pressed{font-size: 50px;}
            #homeButton{font-size: 55px;}
            #homeButton:hover{font-size: 57px;}
            #homeButton:pressed{font-size: 61px;}
            #searchBar{border-radius: 25%; background-color: rgb(30, 30, 30); color: rgb(255, 255, 255); font-size: 22px;}
            #searchBar:focus{background-color: rgb(75, 75, 75);}
            #bookmarkButton{font-size: 40px}
            #bookmarkButton:hover{font-size: 43px}
            #bookmarkButton:pressed{font-size: 46}
            """
        )
        self.TopBar.setObjectName("TopBar")

        # Buttons and search bar
        self.backButton = QtWidgets.QPushButton(self.TopBar)
        self.backButton.setGeometry(QtCore.QRect(20, 10, 80, 80)) 
        self.backButton.setText("◄")
        self.backButton.setToolTip("Backward")
        self.backButton.setObjectName("backButton")

        self.forwardButton = QtWidgets.QPushButton(self.TopBar)
        self.forwardButton.setGeometry(QtCore.QRect(120, 10, 80, 80))
        self.forwardButton.setText("►")
        self.forwardButton.setToolTip("Forward")
        self.forwardButton.setObjectName("forwardButton")

        self.refreshButton = QtWidgets.QPushButton(self.TopBar)
        self.refreshButton.setGeometry(QtCore.QRect(220, 10, 80, 80))
        self.refreshButton.setText("↻")
        self.refreshButton.setToolTip("Refresh")
        self.refreshButton.setObjectName("refreshButton")

        self.homeButton = QtWidgets.QPushButton(self.TopBar)
        self.homeButton.setGeometry(QtCore.QRect(2220, 5, 80, 80))
        self.homeButton.setText("⌂")
        self.homeButton.setToolTip("Home")
        self.homeButton.setObjectName("homeButton")

        self.profileButton = QtWidgets.QPushButton(self.TopBar)
        self.profileButton.setGeometry(QtCore.QRect(2430, 10, 80, 80))
        self.profileButton.setIcon(QtGui.QIcon("Assets/user1.png"))
        self.profileButton.setIconSize(QtCore.QSize(64, 64))
        self.profileButton.setObjectName("profileButton")

        self.searchBar = QtWidgets.QLineEdit(self.TopBar)
        self.searchBar.setGeometry(QtCore.QRect(320, 20, 1900, 60))
        self.searchBar.setPlaceholderText("Enter URL or search query...")
        self.searchBar.setObjectName("searchBar")

        # Web view for displaying pages
        self.webView = QWebEngineView(self.background)
        self.webView.setGeometry(QtCore.QRect(20, 140, 2520, 1280)) 
        self.webView.setObjectName("webView")
        self.webView.setUrl(QtCore.QUrl("file:///homePage.html")) 

        # # Bookmarks and History
        self.bookmarks = []
        self.history = []

        # Add Bookmark Button
        self.bookmarkButton = QtWidgets.QPushButton(self.TopBar)
        self.bookmarkButton.setGeometry(QtCore.QRect(2280, 10, 80, 80))
        self.bookmarkButton.setText("★")
        self.bookmarkButton.setObjectName("bookmarkButton")
        self.bookmarkButton.setToolTip("Add to Bookmarks")
        self.bookmarkButton.clicked.connect(self.add_bookmark)

        # Bookmark Menu
        self.bookmarkMenu = QtWidgets.QListWidget(self.background)
        self.bookmarkMenu.setGeometry(QtCore.QRect(2160, 150, 400, 600))
        self.bookmarkMenu.setWindowTitle("Bookmarks")
        self.bookmarkMenu.setStyleSheet("background-color: rgba(0, 0, 0, 0.1); border-radius: 5px; color: rgb(255, 255, 255);")
        self.bookmarkMenu.hide()
        self.bookmarkMenu.itemClicked.connect(self.load_bookmark)

        # Toggle Bookmarks Button
        self.toggleBookmarksButton = QtWidgets.QPushButton(self.TopBar)
        self.toggleBookmarksButton.setGeometry(QtCore.QRect(2350, 12, 80, 80))
        self.toggleBookmarksButton.setText("☰")
        self.toggleBookmarksButton.setToolTip("Show/Hide Bookmarks")
        self.toggleBookmarksButton.clicked.connect(self.toggle_bookmarks)

        # Web View URL Changed Event
        self.webView.urlChanged.connect(self.track_history)

        # Connect button actions to functions
        self.backButton.clicked.connect(self.webView.back)
        self.forwardButton.clicked.connect(self.webView.forward)
        self.refreshButton.clicked.connect(self.webView.reload)
        self.homeButton.clicked.connect(self.go_home)
        self.searchBar.returnPressed.connect(self.load_url)
    
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()        
        if modifiers & Qt.ControlModifier and key == Qt.Key_H:
            self.openHistory()


    def go_home(self):
        """Navigate to the default home page."""
        self.webView.setUrl(QtCore.QUrl("file:///homePage.html"))

    def load_url(self):
        """Load the URL entered in the search bar."""
        url = self.searchBar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.webView.setUrl(QtCore.QUrl(url))

    def add_bookmark(self):
        """Add the current page to bookmarks."""
        url = self.webView.url().toString()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            self.bookmarkMenu.addItem(url)

    def toggle_bookmarks(self):
        """Show or hide the bookmarks list."""
        if self.bookmarkMenu.isVisible():
            self.bookmarkMenu.hide()
        else:
            self.bookmarkMenu.show()

    def load_bookmark(self, item):
        """Load a bookmarked page when clicked."""
        self.webView.setUrl(QtCore.QUrl(item.text()))

    def track_history(self, url):
        url_str = url.toString()
        if url_str != "file:///homePage.html" and (not self.history or self.history[-1] != url_str):
            self.history.append(url_str)
            self.updateHistory() 


    def updateHistory(self):
        """Save browsing history to a CSV file."""
        os.makedirs("User Info/History", exist_ok=True)
        fileName = "User Info/History/History.csv"
        fieldnames = ["History"]

        # Check if the file already exists
        file_exists = os.path.isfile(fileName) and os.path.getsize(fileName) > 0

        with open(fileName, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file doesn't exist or is empty
            if not file_exists:
                writer.writeheader()

            # Write each URL in the history as a new row
            for url in self.history:
                writer.writerow({"History": url})

    def openHistory(self):
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(os.path.abspath("history.html")))

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = Ui_Form()
    Form.show()
    sys.exit(app.exec_())
