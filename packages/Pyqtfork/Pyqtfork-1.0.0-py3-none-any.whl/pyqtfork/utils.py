"""
Pyqtfork Utilities

This module provides utility functions to simplify common tasks in UI development.
"""

import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap


def get_app():
    """
    Get the current QApplication instance or create a new one if none exists.
    
    Returns:
        QApplication: The application instance
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app


def show_message(title, message, icon=QMessageBox.Information, parent=None):
    """
    Show a message box with the specified title and message.
    
    Args:
        title (str): The title of the message box
        message (str): The message to display
        icon (QMessageBox.Icon): The icon to display (default: Information)
        parent (QWidget): The parent widget (default: None)
        
    Returns:
        int: The button clicked (QMessageBox.StandardButton)
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    return msg_box.exec_()


def confirm(message, title="Confirm", parent=None):
    """
    Show a confirmation dialog with Yes/No buttons.
    
    Args:
        message (str): The message to display
        title (str): The title of the dialog (default: "Confirm")
        parent (QWidget): The parent widget (default: None)
        
    Returns:
        bool: True if Yes was clicked, False otherwise
    """
    result = QMessageBox.question(
        parent, title, message, 
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No
    )
    return result == QMessageBox.Yes


def resource_path(relative_path):
    """
    Get the absolute path to a resource file.
    Works for development and for PyInstaller.
    
    Args:
        relative_path (str): The relative path to the resource
        
    Returns:
        str: The absolute path to the resource
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_icon(path, size=None):
    """
    Load an icon from a file path.
    
    Args:
        path (str): The path to the icon file
        size (tuple): Optional size to resize the icon (width, height)
        
    Returns:
        QIcon: The loaded icon
    """
    icon = QIcon(path)
    if size is not None:
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(QSize(*size), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon = QIcon(pixmap)
    return icon