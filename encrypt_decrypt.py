import json
import os
from cryptography.fernet import Fernet

class Notes:

    def __init__(self, notes_file="data.json", key_file="secret.key"):
        self.notes_file = notes_file
        self.key_file = key_file
        self.notes = []
        self.fernet = None
        self.set_fernet()
        self.load_notes()

    def set_fernet(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                crypto_key = f.read()
        else:
            crypto_key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(crypto_key)
        self.fernet = Fernet(crypto_key)

    def encrypt_text(self, text):
        if not self.fernet:
            raise ValueError("Fernet key is not set")
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt_text(self, text):
        if not self.fernet:
            raise ValueError("Fernet key is not set")
        return self.fernet.decrypt(text.encode()).decode()

    def save_notes(self):
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(self.notes, f, indent=4)
            print("Notes saved successfully")
        except Exception as e:
            print("Error saving notes:", str(e))

    def load_notes(self):
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r') as f:
                    self.notes = json.load(f)
            except json.JSONDecodeError:
                self.notes = []
                print("The notes file is corrupted or empty. Starting fresh.")
            except Exception as e:
                self.notes = []
                print("Error loading notes:", str(e))
        else:
            self.notes = []

    def add_note(self):
        print("\nAdd a new note")
        title = input("Enter note title: ").strip()
        if not title:
            print("Title cannot be empty")
            return
        content = input("Enter note content: ").strip()
        if not content:
            print("Content cannot be empty")
            return

        try:
            encrypted_content = self.encrypt_text(content)
            note = {
                "id": len(self.notes) + 1,
                "title": title,
                "content": encrypted_content
            }
            self.notes.append(note)
            self.save_notes()
            print("Note added successfully")
        except Exception as e:
            print("Error adding note:", str(e))

    def list_notes(self):
        if not self.notes:
            print("\nNo notes available.")
            return
        print("\nList of Notes:")
        for note in self.notes:
            print(f"{note['id']}. {note['title']}")

    def view_note(self):
        if not self.notes:
            print("\nNo notes to view.")
            return
        try:
            note_id = int(input("Enter note ID to view: "))
            for note in self.notes:
                if note["id"] == note_id:
                    print(f"\nTitle: {note['title']}")
                    decrypted_content = self.decrypt_text(note["content"])
                    print(f"Content: {decrypted_content}")
                    return
            print("Note not found.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def delete_note(self):
        if not self.notes:
            print("\nNo notes to delete.")
            return
        try:
            note_id = int(input("Enter note ID to delete: "))
            for note in self.notes:
                if note["id"] == note_id:
                    self.notes.remove(note)
                    self.save_notes()
                    print("Note deleted successfully.")
                    return
            print("Note not found.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def menu(self):
        print("\n=== Notes CLI App ===")
        while True:
            print("\nOptions:")
            print("1. Add Note")
            print("2. List Notes")
            print("3. View Note")
            print("4. Delete Note")
            print("5. Exit")

            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.add_note()
            elif choice == '2':
                self.list_notes()
            elif choice == '3':
                self.view_note()
            elif choice == '4':
                self.delete_note()
            elif choice == '5':
                print("Exiting the app.")
                break
            else:
                print("Invalid option. Please try again.")

def main():
    notes = Notes()
    notes.menu()

if __name__ == "__main__":
    main()
