import os
import sys
from PyQt5.QtWidgets import QApplication

class StyleManager:
    @staticmethod
    def get_resource_path(relative_path):
        """Get the absolute path to a resource, works for dev and for PyInstaller."""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        return os.path.join(base_path, relative_path)

    @staticmethod
    def load_stylesheet(filename="main.qss"):
        """Load the QSS stylesheet from the assets/styles directory."""
        try:
            style_path = StyleManager.get_resource_path(os.path.join("assets", "styles", filename))
            
            if os.path.exists(style_path):
                with open(style_path, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                print(f"Stylesheet not found: {style_path}")
                return ""
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            return ""

    @staticmethod
    def apply_styles(app):
        """Apply the global stylesheet to the application."""
        stylesheet = StyleManager.load_stylesheet()
        if stylesheet:
            app.setStyleSheet(stylesheet)
