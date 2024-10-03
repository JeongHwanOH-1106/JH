import os
import shutil
from dirsync import sync
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, QLineEdit, QLabel

class BackupApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("데이터 백업 프로그램")
        self.source_folders = []
        self.target_folder = ""

        self.layout = QVBoxLayout()

        self.source_label = QLabel("백업할 폴더들:")
        self.layout.addWidget(self.source_label)

        self.source_listbox = QListWidget()
        self.layout.addWidget(self.source_listbox)

        self.add_button = QPushButton("폴더 추가")
        self.add_button.clicked.connect(self.add_source_folder)
        self.layout.addWidget(self.add_button)

        self.delete_button = QPushButton("선택된 폴더 삭제")
        self.delete_button.clicked.connect(self.delete_selected_folders)
        self.layout.addWidget(self.delete_button)

        self.target_label = QLabel("백업 위치:")
        self.layout.addWidget(self.target_label)

        self.target_entry = QLineEdit()
        self.layout.addWidget(self.target_entry)

        self.select_target_button = QPushButton("폴더 선택")
        self.select_target_button.clicked.connect(self.select_target_folder)
        self.layout.addWidget(self.select_target_button)

        self.backup_button = QPushButton("백업 시작")
        self.backup_button.clicked.connect(self.backup)
        self.layout.addWidget(self.backup_button)

        self.setLayout(self.layout)

    def add_source_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if folder_selected:
            self.source_folders.append(folder_selected)
            self.update_source_listbox()

    def select_target_folder(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "폴더 선택")
        if folder_selected:
            self.target_folder = folder_selected
            self.target_entry.setText(self.target_folder)

    def delete_selected_folders(self):
        selected_items = self.source_listbox.selectedItems()
        for item in selected_items:
            self.source_folders.remove(item.text())
        self.update_source_listbox()

    def update_source_listbox(self):
        self.source_listbox.clear()
        for folder in self.source_folders:
            self.source_listbox.addItem(folder)

    def backup(self):
        target = self.target_folder
        for source in self.source_folders:
            source_folder_name = os.path.basename(source)
            new_target = os.path.join(target, source_folder_name)
            
            if not os.path.exists(new_target):
                os.makedirs(new_target)
            
            sync(source, new_target, 'sync', purge=True)
        
        QMessageBox.information(self, "백업 완료", "백업이 완료되었습니다!")

if __name__ == "__main__":
    app = QApplication([])
    window = BackupApp()
    window.show()
    app.exec()
    #add change
