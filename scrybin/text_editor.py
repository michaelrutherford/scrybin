from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCursor
from PySide6.QtCore import Qt


class TextEditor(QTextEdit):
    """
    A custom text editor widget with support for user preferences, word count,
    and additional helper methods.
    """

    def __init__(self, parent):
        """
        Initializes the TextEditor.

        Args:
            parent: The parent widget for this text editor.
        """
        super().__init__(parent)
        self.parent = parent

        # Set default interaction mode and connect textChanged signal
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.textChanged.connect(self.parent.update_ribbon)

        # Default style
        self.setStyleSheet(
            "background-color: #2e2e2e; color: #ffffff; font-size: 12pt;"
        )

    def apply_preferences(self, bg_color, fg_color, font_size):
        """
        Applies user preferences to the text editor.

        Args:
            bg_color (str): The background color for the text editor.
            fg_color (str): The text color for the text editor.
            font_size (int): The font size for the text editor.
        """
        # Update the background and text colors
        self.setStyleSheet(f"background-color: {bg_color}; color: {fg_color};")

        # Update the font size
        font = self.font()
        font.setPointSize(font_size)
        self.setFont(font)

    def get_word_count(self):
        """
        Returns the word count of the text in the editor.

        Returns:
            int: The number of words in the text editor.
        """
        return len(self.toPlainText().split())

    def clear_text(self):
        """
        Clears all text in the editor.
        """
        self.clear()

    def set_text(self, text):
        """
        Sets the given text in the editor and moves the cursor to the end.

        Args:
            text (str): The text to set in the editor.
        """
        self.setPlainText(text)
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
