import sys
from PyQt5 import QtCore ,QtWidgets
from testing import Ui_Form


class MainWindow(QtWidgets.QWidget, Ui_Form):   
    def __init__(self, parent=None):     
        super(MainWindow, self).__init__(parent)     
        self.setupUi(self)     
        self.go_button.clicked.connect(self.pressed)   
    def pressed(self):     
        self.webView.setUrl(QtCore.QUrl(self.lineEdit.displayText()))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    view = MainWindow() 
    view.showMaximized()
    sys.exit(app.exec_())