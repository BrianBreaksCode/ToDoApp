"""
main.py
_______
Application entry point.
"""
import sys
from PyQt6.QtWidgets import QApplication

def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("PyQt6 To-Do App")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()