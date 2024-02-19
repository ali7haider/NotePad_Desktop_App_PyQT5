# Import necessary libraries
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtWidgets import QMainWindow, QPlainTextEdit, QAction, QMenu, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QTextCursor
from UI.mainwindow_ui import Ui_MainWindow

# Import Qt's core module
from PyQt5.QtCore import Qt


# Declare widgets variable
widgets = None

# Define the MainWindow class that inherits from QMainWindow
class MainWindow(QMainWindow,Ui_MainWindow):
    # Constructor method for the MainWindow class
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        # Connect the maximizeRestoreAppBtn button to the maximize_window method
        self.maximizeRestoreAppBtn.clicked.connect(self.maximize_window)

        # Connect the closeAppBtn button to the close method
        self.closeAppBtn.clicked.connect(self.close)

        # Connect the minimizeAppBtn button to the showMinimized method
        self.minimizeAppBtn.clicked.connect(self.showMinimized)

        # Set the window flag to remove the window frame
        self.setWindowFlag(Qt.FramelessWindowHint)

        # Connect the btnSubmit button to the save_text_to_file method
        self.btnSubmit.clicked.connect(self.save_text_to_file)

        # Connect the btnBullet button to the bullet_points method
        self.btnBullet.clicked.connect(self.bullet_points)

        # Call the readData method to display the saved text, if any
        self.readData()

    # Define the readData method to read the data from the text file
    def readData(self): 
        try:
            # Open the text file and read its contents
            with open('data/output.txt', 'r') as file:
                self.txtData.setPlainText(file.read())
        # If the file does not exist, do nothing
        except FileNotFoundError:
            pass

    # Define the bullet_points method to format selected text as bullet points
    def bullet_points(self):
        # Get the selected text
        cursor = self.txtData.textCursor()
        selected_text = cursor.selectedText()

        # Check if the selected text is already in bullet points format
        if "• " in selected_text:
            # Remove bullet points and replace with plain text
            plain_text = selected_text.replace("• ", "")
            cursor.insertText(plain_text)
        else:
            # Convert the selected text into bullet points
            bullet_points = "• " + selected_text.replace("\n", "\n• ")
            cursor.insertText(bullet_points)

        # Move the cursor to the end of the inserted text
        cursor.movePosition(QTextCursor.End)
        self.txtData.setTextCursor(cursor)

    # Define the close_Window method to close the window
    def close_Window(self):
        self.Close()

    # Define the maximize_window method to maximize or restore the window
    def maximize_window(self):
        # If the window is already maximized, restore it
        if self.isMaximized():
            self.showNormal()
        # Otherwise, maximize it
        else:
            self.showMaximized()

    # Define the mousePressEvent method to handle mouse button press events
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPos)
            event.accept()
            

    def save_text_to_file(self):
        # Saving the text in a txt file 
        text = self.txtData.toPlainText()
        # Save the text to a file
        with open("data/output.txt", "w") as file:
            file.write(text)
        self.show_text()
    def show_text(self):
        # Show the text on the label
        self.lblSavedOption.setText("Saved Successfully")

        # Create a QTimer to hide the label after 3 seconds
        timer = QTimer(self)
        timer.timeout.connect(self.hide_text)
        timer.start(3000)

    def hide_text(self):
        # Hide the text on the label
        self.lblSavedOption.setText("")
                    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())