import json
import os
from PySide6.QtWidgets import (
    QDialog,
    QComboBox,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QSpinBox,
)


class PreferencesManager(QDialog):
    """
    Manages the preferences dialog for the application, including themes and font size.
    """

    def __init__(self, parent=None):
        """
        Initializes the PreferencesManager dialog.

        Args:
            parent: The parent widget for the dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setFixedSize(300, 250)
        self.parent = parent

        self.themes = self.load_themes()

        # Create UI components
        self.theme_label = QLabel("Select Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(list(self.themes.keys()))

        self.font_size_label = QLabel("Font Size:")
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 36)  # Allowable font size range
        self.font_size_spinbox.setValue(12)  # Default font size

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_preferences)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.theme_label)
        layout.addWidget(self.theme_combo)
        layout.addWidget(self.font_size_label)
        layout.addWidget(self.font_size_spinbox)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Load and apply saved preferences
        self.load_preferences()

    def load_themes(self):
        """
        Loads available themes from a JSON file.

        Returns:
            dict: A dictionary of themes with theme names as keys and color settings as values.
        """
        if os.path.exists("themes.json"):
            with open("themes.json", "r") as file:
                return json.load(file)
        return {}

    def load_preferences(self):
        """
        Loads user preferences from a JSON file and applies them.
        """
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as file:
                settings = json.load(file)
                bg_color = settings.get("bg_color")
                fg_color = settings.get("fg_color")
                font_size = settings.get("font_size", 12)  # Default to 12

                # Set the theme based on the loaded background color
                theme = self.get_theme_from_colors(bg_color)
                self.theme_combo.setCurrentText(theme)
                self.font_size_spinbox.setValue(font_size)

                # Apply the loaded preferences
                self.apply_preferences(bg_color, fg_color, font_size)

    def get_theme_from_colors(self, bg_color):
        """
        Retrieves the theme name corresponding to a given background color.

        Args:
            bg_color (str): The background color to match.

        Returns:
            str: The name of the theme that matches the given background color, or "Dark" if no match is found.
        """
        for theme, colors in self.themes.items():
            if colors["bg_color"] == bg_color:
                return theme
        return "Dark"  # Default theme

    def save_preferences(self):
        """
        Saves the currently selected preferences to a file and applies them.
        """
        theme = self.theme_combo.currentText()
        bg_color = self.themes[theme]["bg_color"]
        fg_color = self.themes[theme]["fg_color"]
        font_size = self.font_size_spinbox.value()

        # Save preferences to file
        self.save_preferences_to_file(bg_color, fg_color, font_size)

        # Apply the preferences
        self.apply_preferences(bg_color, fg_color, font_size)

        # Close the preferences dialog
        self.accept()

    def apply_preferences(self, bg_color, fg_color, font_size):
        """
        Applies the preferences to the parent TextEditor.

        Args:
            bg_color (str): The background color to apply.
            fg_color (str): The foreground color to apply.
            font_size (int): The font size to apply.
        """
        if self.parent and hasattr(self.parent, "text_area"):
            self.parent.text_area.apply_preferences(bg_color, fg_color, font_size)

    def save_preferences_to_file(self, bg_color, fg_color, font_size):
        """
        Saves preferences to a JSON file.

        Args:
            bg_color (str): The background color to save.
            fg_color (str): The foreground color to save.
            font_size (int): The font size to save.
        """
        settings = {"bg_color": bg_color, "fg_color": fg_color, "font_size": font_size}
        with open("settings.json", "w") as file:
            json.dump(settings, file, indent=4)
