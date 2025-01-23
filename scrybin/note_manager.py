import json
import os


class NoteManager:
    """Manages the creation, retrieval, update, and deletion of notes."""

    def __init__(self):
        """Initializes the NoteManager with an empty notes dictionary and no current note."""
        self.notes = {}
        self.current_note = None

    def load_notes(self):
        """
        Loads notes from a JSON file if it exists.

        Returns:
            dict: A dictionary of notes with titles as keys and content as values.
        """
        if os.path.exists("notes.json"):
            with open("notes.json", "r") as file:
                self.notes = json.load(file)
        return self.notes

    def save_notes_to_file(self):
        """
        Saves the current notes dictionary to a JSON file.
        """
        with open("notes.json", "w") as file:
            json.dump(self.notes, file, indent=4)

    def add_new_note(self, note_title):
        """
        Adds a new note with a unique title to the notes dictionary.

        Args:
            note_title (str): The title of the new note.

        Returns:
            str: The final unique title used for the new note.
        """
        original_title = note_title
        count = 1
        while note_title in self.notes:
            note_title = f"{original_title} ({count})"
            count += 1
        self.notes[note_title] = ""
        return note_title

    def delete_note(self, note_title):
        """
        Deletes a note by its title from the notes dictionary.

        Args:
            note_title (str): The title of the note to delete.
        """
        if note_title in self.notes:
            del self.notes[note_title]

    def get_note_content(self, note_title):
        """
        Retrieves the content of a note by its title.

        Args:
            note_title (str): The title of the note.

        Returns:
            str: The content of the note, or an empty string if the note does not exist.
        """
        return self.notes.get(note_title, "")

    def set_note_content(self, note_title, content):
        """
        Updates the content of a note by its title.

        Args:
            note_title (str): The title of the note.
            content (str): The new content of the note.
        """
        self.notes[note_title] = content

    def get_note_titles(self):
        """
        Retrieves a list of all note titles.

        Returns:
            list: A list of note titles.
        """
        return list(self.notes.keys())
