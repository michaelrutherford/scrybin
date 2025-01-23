import json
import os
from PySide6.QtWidgets import (
    QMainWindow,
    QListWidget,
    QDialog,
    QMessageBox,
    QInputDialog,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt
from preferences_manager import PreferencesManager
from menu_bar import MenuBar
from text_editor import TextEditor
from note_manager import NoteManager


class App(QMainWindow):
    """
    Main application window for the Notebook app.
    Handles the UI, note management, and user interactions.
    """

    def __init__(self):
        """
        Initialize the main application window.
        """
        super().__init__()
        self.setWindowTitle("Scrybin")
        self.resize(500, 500)

        self.preferences_manager = PreferencesManager()
        self.note_manager = NoteManager()
        self.current_note = None
        self.zen_mode = False

        self.create_widgets()
        self.load_preferences()
        self.load_notes()

    def load_preferences(self):
        """
        Load user preferences from the settings file.
        """
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as file:
                    settings = json.load(file)
                    self.bg_color = settings.get("bg_color", "#2e2e2e")
                    self.fg_color = settings.get("fg_color", "#ffffff")
                    self.font_size = settings.get("font_size", 12)
                    self.apply_styles()
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading settings: {e}")

    def apply_styles(self):
        """
        Apply styles to the text editor based on user preferences.
        """
        self.text_area.setStyleSheet(
            f"background-color: {self.bg_color}; color: {self.fg_color}; font-size: {self.font_size}pt;"
        )

    def create_widgets(self):
        """
        Create and arrange the widgets in the main application window.
        """
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout(self.central_widget)

        self.text_area = TextEditor(self)
        self.menu_bar = MenuBar(self, self.text_area)

        self.notes_list = QListWidget()
        self.notes_list.itemClicked.connect(self.load_selected_note)

        self.ribbon = QLabel()
        self.update_ribbon()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.text_area)
        right_layout.addWidget(self.ribbon)

        self.notes_list.setFixedWidth(self.width() // 3)
        layout.addWidget(self.notes_list)
        layout.addLayout(right_layout)

    def load_notes(self):
        """
        Load notes from the note manager into the UI.
        """
        self.note_manager.load_notes()
        for note_title in self.note_manager.get_note_titles():
            self.notes_list.addItem(note_title)

        if self.notes_list.count() > 0:
            self.notes_list.setCurrentRow(self.notes_list.count() - 1)
            self.load_selected_note(self.notes_list.currentItem())

    def new_note(self):
        """
        Create a new note with a user-provided title.
        """
        note_title, ok = QInputDialog.getText(self, "New Note", "Enter note title:")
        if ok and note_title.strip():
            note_title = note_title.strip()
        else:
            note_title = "New Note"

        self.current_note = self.note_manager.add_new_note(note_title)
        self.notes_list.addItem(self.current_note)
        self.notes_list.setCurrentRow(self.notes_list.count() - 1)
        self.load_selected_note(self.notes_list.currentItem())

    def load_selected_note(self, item):
        """
        Load the content of the selected note into the text editor.
        """
        self.current_note = item.text()
        self.text_area.set_text(self.note_manager.get_note_content(self.current_note))
        self.update_ribbon()

    def save_note(self):
        """
        Save the current note's content to the note manager.
        """
        if self.current_note:
            content = self.text_area.toPlainText().strip()
            self.note_manager.set_note_content(self.current_note, content)
            self.note_manager.save_notes_to_file()
            self.update_ribbon()
        else:
            QMessageBox.warning(self, "Warning", "No note selected!")

    def save_note_as(self):
        """
        Save the current note under a new title.
        """
        if self.current_note:
            note_title, ok = QInputDialog.getText(
                self, "Save As", "Enter new note title:"
            )
            if ok and note_title.strip():
                note_title = note_title.strip()
                content = self.text_area.toPlainText().strip()

                self.note_manager.add_new_note(note_title)
                self.note_manager.set_note_content(note_title, content)

                self.notes_list.addItem(note_title)
                self.notes_list.setCurrentRow(self.notes_list.count() - 1)
                self.current_note = note_title

                self.note_manager.save_notes_to_file()
                self.update_ribbon()
            else:
                QMessageBox.warning(self, "Warning", "Note title cannot be empty!")
        else:
            QMessageBox.warning(self, "Warning", "No note selected!")

    def delete_note(self):
        """
        Delete the currently selected note.
        """
        if self.current_note:
            confirm = QMessageBox.question(
                self,
                "Confirm Delete",
                f"Are you sure you want to delete '{self.current_note}'?",
            )
            if confirm == QMessageBox.StandardButton.Yes:
                self.note_manager.delete_note(self.current_note)
                self.notes_list.takeItem(self.notes_list.currentRow())
                self.text_area.clear()
                self.current_note = None
                self.update_ribbon()
                self.note_manager.save_notes_to_file()
        else:
            QMessageBox.warning(self, "Warning", "No note selected!")

    def update_ribbon(self):
        """
        Update the ribbon with the current note's title and word count.
        """
        word_count = self.text_area.get_word_count() if self.current_note else 0
        self.ribbon.setText(
            f'"{self.current_note}", Words: {word_count}'
            if self.current_note
            else "No note selected."
        )

    def toggle_zen_mode(self, checked):
        """
        Toggle Zen mode.
        """
        self.zen_mode = checked
        self.showFullScreen() if checked else self.showNormal()
        self.notes_list.setVisible(not checked)
        self.ribbon.setVisible(not checked)
        self.menuBar().setVisible(not checked)

    def quit_app(self):
        """
        Exit the application.
        """
        self.close()

    def show_about(self):
        """
        Show the About dialog.
        """
        QMessageBox.information(
            self, "About", "This is a simple note-taking app.\n\nBy: Michael Rutherford"
        )

    def show_keyboard_shortcuts(self):
        """
        Display keyboard shortcuts.
        """
        QMessageBox.information(
            self,
            "Keyboard Shortcuts",
            "Ctrl+N = New note\nCtrl+S = Save\nCtrl+X = Cut\nCtrl+C = Copy\nCtrl+V = Paste\nCtrl+Q = Quit",
        )

    def show_preferences(self):
        """
        Open the preferences dialog.
        """
        dialog = PreferencesManager(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_preferences()

    def keyPressEvent(self, event):
        """
        Handle key press events for application shortcuts.
        """
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_note()
        elif event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.quit_app()
        elif event.key() == Qt.Key_N and event.modifiers() == Qt.ControlModifier:
            self.new_note()
            self.text_area.setFocus()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if self.notes_list.currentItem():
                selected_note = self.notes_list.currentItem().text()
                if selected_note == self.current_note:
                    self.text_area.setFocus()
                    cursor = self.text_area.textCursor()
                    cursor.movePosition(QTextCursor.MoveOperation.End)
                    self.text_area.setTextCursor(cursor)
                else:
                    self.load_selected_note(self.notes_list.currentItem())
        elif event.key() == Qt.Key_Delete:
            self.delete_note()
        elif event.key() == Qt.Key_Escape:
            if self.zen_mode:
                self.zen_mode = False
                self.toggle_zen_mode(False)  # Exit Zen mode
                self.zen_mode_action.setChecked(False)
            else:
                self.text_area.clearFocus()
                self.notes_list.setFocus()
