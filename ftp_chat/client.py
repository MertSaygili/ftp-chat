
# import required modules
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, QInputDialog
from PyQt5 import QtCore

from ftplib import FTP

# Create a class named FTPClientGUI that inherits from QMainWindow
class FTPClientGUI(QMainWindow):
    def __init__(self):
        # Initialize the parent class
        super().__init__()
        # Call the initUI method to initialize the user interface
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FTP Client")

        # Create a main widget and set it as the central widget of the window
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical box layout and set it as the layout of the main widget
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Create a label and a line edit for the user to enter the IP address
        self.user_ip_label = QLabel("Ip:")
        self.user_ip_input = QLineEdit()
        layout.addWidget(self.user_ip_label)
        layout.addWidget(self.user_ip_input)

        # Create a label and a line edit for the user to enter the port
        self.user_port_label = QLabel("Port:")
        self.user_port_input = QLineEdit()
        layout.addWidget(self.user_port_label)
        layout.addWidget(self.user_port_input)

        # Create a label and a line edit for the user to enter the username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Create a label and a line edit for the user to enter the password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Create a login button and connect its clicked signal to the login slot
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        # FTP connection object
        self.ftp = FTP('')

        # Set the main window size and show it
        self.setGeometry(100, 100, 300, 200)
        self.show()

    def initFTPUI(self):
        # window title
        self.setWindowTitle("FTP Client")

        # main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # vertical box layout
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # FTP operations, such as creating a folder/file, uploading, downloading, renaming, listing directory, and deleting a file/folder
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_folder_file)
        layout.addWidget(self.create_button)

        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload)
        layout.addWidget(self.upload_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        layout.addWidget(self.download_button)

        self.rename_button = QPushButton("Rename")
        self.rename_button.clicked.connect(self.rename_file_or_directory)
        layout.addWidget(self.rename_button)

        self.list_directory_button = QPushButton("List Directory")
        self.list_directory_button.clicked.connect(self.list_directory)
        layout.addWidget(self.list_directory_button)

        self.delete_file_folder_button = QPushButton("Delete file/folder")
        self.delete_file_folder_button.clicked.connect(self.delete_file_folder)
        layout.addWidget(self.delete_file_folder_button)

        # Set the main window size and show it
        self.setGeometry(100, 100, 300, 200)
        self.show()

    # The rest of the code follows the same pattern of creating UI elements, adding them to the layout, and connecting them to their respective functions.
    # The functions perform various FTP operations such as login, create folder/file, upload, download, rename file/directory, list directory, and delete file/folder.
    # The functions use the ftplib module to perform the FTP operations.
    def login(self):
    # Establish FTP connection
        ip = self.user_ip_input.text()
        port = self.user_port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        self.ftp.connect(host = ip, port= int(port))

        try:
            self.ftp.login(username, password)
            QMessageBox.information(self, "Login", "Login successful.")
            self.initFTPUI()
        except Exception as e:
            QMessageBox.critical(self, "Login Error", str(e))

    def create_folder_file(self):
        # Create a file or folder on the FTP server
        path, ok = QInputDialog.getText(self, "Create file/folder", "Enter created file path:")
        if ok:
            self.ftp.mkd(path)

    def upload(self):
        # Upload a file to the FTP server
        if not self.ftp:
            QMessageBox.warning(self, "Upload Error", "You are not logged in.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        upload_path, _ = QFileDialog.getSaveFileName(self, "Select Location to Upload File")

        if upload_path:
            with open(file_path, 'rb') as file:
                file_name = file_path.split('/')[-1]
                print(file_name)
                print(upload_path + '/' + file_name)
                try:
                    self.ftp.storbinary('STOR ' + upload_path, file)
                    QMessageBox.information(self, "Upload", "Upload successful.")
                except Exception as e:
                    QMessageBox.critical(self, "Upload Error", str(e))

    def download(self):
        # Download a file from the FTP server
        if not self.ftp:
            QMessageBox.warning(self, "Download Error", "You are not logged in.")
            return

        remote_file_path, _ = QFileDialog.getOpenFileName(self, "Select File to download")
        if not remote_file_path:
            return 

        local_save_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if not local_save_path:
            return 

        try:
            with open(local_save_path, 'wb') as file:
                self.ftp.retrbinary('RETR ' + local_save_path, file)
            QMessageBox.information(self, "Download", "Download successful.")
        except Exception as e:
            QMessageBox.critical(self, "Download Error", str(e))

    def rename_file_or_directory(self):
        # Rename a file or directory on the FTP server
        if not self.ftp:
            QMessageBox.warning(self, "Rename Error", "You are not logged in.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Rename")
        new_name, ok = QInputDialog.getText(self, "Rename", "Enter new name:")
        if ok:
            try:
                old_file_name = file_path.split('/')[-1]
                base_path = file_path.replace(old_file_name, '')

                print(file_path)
                print(base_path)
                print(new_name)

                self.ftp.rename(file_path, base_path + '/' + new_name)
                QMessageBox.information(self, "Rename", "Rename successful.")
            except Exception as e:
                QMessageBox.critical(self, "Rename Error", str(e))

    def list_directory(self):
        # List the contents of a directory on the FTP server
        if not self.ftp:
            QMessageBox.warning(self, "List Directory Error", "You are not logged in.")
            return

        try:
            files = []
            self.ftp.dir(files.append)
            directory_list_dialog = QInputDialog()
            directory_list_dialog.setOption(QInputDialog.UseListViewForComboBoxItems)
            directory_list_dialog.setComboBoxItems(files)
            directory_list_dialog.setWindowTitle("Directory List")
            directory_list_dialog.setLabelText("Files in the directory:")
            directory_list_dialog.setOkButtonText("Close")
            directory_list_dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "List Directory Error", str(e))

    def delete_file_folder(self):
        # Delete a file or directory on the FTP server
        if not self.ftp:
            QMessageBox.warning(self, "Delete Error", "You are not logged in.")
            return
        
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")

        try:
            self.ftp.delete(file_path)  # Delete the file or directory
            QMessageBox.information(self, "Delete", "Delete successful.")
        except Exception as e:
            QMessageBox.critical(self, "Delete Error", str(e))
            if not self.ftp:
                QMessageBox.warning(self, "Delete Error", "You are not logged in.")
                return
            
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")

            try:
                self.ftp.delete(file_path)  # Dosya veya dizini sil
                QMessageBox.information(self, "Delete", "Delete successful.")
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", str(e))

def main():
    app = QApplication(sys.argv)  # Create a QApplication
    window = FTPClientGUI()  # Create an instance of FTPClientGUI
    sys.exit(app.exec_())  # Start the application

if __name__ == "__main__":
    main()  # Run the main function if the script is run directly