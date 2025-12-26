import os
from PyQt5.QtWidgets import QApplication

class StyleManager:
    @staticmethod
    def load_stylesheet(filename="main.qss"):
        """Load the QSS stylesheet from the assets/styles directory."""
        try:
            # Assuming the assets directory is in the root of the project
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            style_path = os.path.join(base_dir, "assets", "styles", filename)
            
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
