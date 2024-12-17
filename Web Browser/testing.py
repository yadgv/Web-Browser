import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        button = QPushButton("Button")
        layout.addWidget(button)

        self.setMinimumSize(4000, 2000)  # set minimum size
        self.setMaximumSize(8000, 6000)  # set maximum size

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())