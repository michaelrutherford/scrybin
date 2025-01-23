from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction


class MenuBar:
    """Creates and manages the menu bar for the main application window."""

    def __init__(self, parent, text_area):
        """
        Initializes the menu bar.

        Args:
            parent: The parent QMainWindow.
            text_area: The text editor widget for handling text-related actions.
        """
        self.parent = parent
        self.text_area = text_area
        self.create_menu_bar()

    def create_menu_bar(self):
        """Sets up the menu bar with File, Edit, Settings, and Help menus."""
        menu_bar = QMenuBar(self.parent)
        self.parent.setMenuBar(menu_bar)

        # File menu
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(QAction("New", self.parent, triggered=self.parent.new_note))
        file_menu.addAction(
            QAction("Save", self.parent, triggered=self.parent.save_note)
        )
        file_menu.addAction(
            QAction("Save As", self.parent, triggered=self.parent.save_note_as)
        )
        file_menu.addSeparator()
        file_menu.addAction(
            QAction("Delete", self.parent, triggered=self.parent.delete_note)
        )
        file_menu.addSeparator()
        file_menu.addAction(
            QAction("Quit", self.parent, triggered=self.parent.quit_app)
        )

        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(
            QAction("Cut", self.text_area, triggered=self.text_area.cut)
        )
        edit_menu.addAction(
            QAction("Copy", self.text_area, triggered=self.text_area.copy)
        )
        edit_menu.addAction(
            QAction("Paste", self.text_area, triggered=self.text_area.paste)
        )

        # Settings menu
        settings_menu = menu_bar.addMenu("Settings")
        preferences_action = QAction(
            "Preferences", self.parent, triggered=self.parent.show_preferences
        )
        settings_menu.addAction(preferences_action)

        self.parent.zen_mode_action = QAction("Zen Mode", self.parent, checkable=True)
        self.parent.zen_mode_action.triggered.connect(self.parent.toggle_zen_mode)
        settings_menu.addAction(self.parent.zen_mode_action)

        # Help menu
        help_menu = menu_bar.addMenu("Help")
        help_menu.addAction(
            QAction(
                "Keyboard Shortcuts",
                self.parent,
                triggered=self.parent.show_keyboard_shortcuts,
            )
        )
        help_menu.addAction(
            QAction("About", self.parent, triggered=self.parent.show_about)
        )
