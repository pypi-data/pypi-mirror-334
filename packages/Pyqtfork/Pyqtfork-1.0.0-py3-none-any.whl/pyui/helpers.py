"""
PYUI Helper Functions

This module provides helper functions to simplify common UI development tasks.
"""

import os
import json
from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox, QInputDialog, QColorDialog,
    QFontDialog, QApplication, QDesktopWidget
)
from PyQt5.QtCore import QSettings, QSize, QPoint, QRect
from PyQt5.QtGui import QColor, QFont


def center_window(window):
    """
    Center a window on the screen.
    
    Args:
        window (QWidget): The window to center
    """
    frame_geometry = window.frameGeometry()
    screen_center = QDesktopWidget().availableGeometry().center()
    frame_geometry.moveCenter(screen_center)
    window.move(frame_geometry.topLeft())


def save_window_state(window, settings_name="app_settings", group="MainWindow"):
    """
    Save the window state (position, size) to QSettings.
    
    Args:
        window (QWidget): The window to save state for
        settings_name (str): The name for the settings file
        group (str): The settings group name
    """
    settings = QSettings(settings_name, QSettings.IniFormat)
    settings.beginGroup(group)
    settings.setValue("geometry", window.saveGeometry())
    settings.setValue("state", window.saveState() if hasattr(window, "saveState") else None)
    settings.setValue("maximized", window.isMaximized())
    if not window.isMaximized():
        settings.setValue("pos", window.pos())
        settings.setValue("size", window.size())
    settings.endGroup()


def restore_window_state(window, settings_name="app_settings", group="MainWindow"):
    """
    Restore the window state (position, size) from QSettings.
    
    Args:
        window (QWidget): The window to restore state for
        settings_name (str): The name for the settings file
        group (str): The settings group name
        
    Returns:
        bool: True if state was restored, False otherwise
    """
    settings = QSettings(settings_name, QSettings.IniFormat)
    settings.beginGroup(group)
    
    # Check if we have saved settings
    if not settings.contains("pos"):
        settings.endGroup()
        return False
    
    # Restore geometry
    geometry = settings.value("geometry")
    if geometry:
        window.restoreGeometry(geometry)
    
    # Restore state for QMainWindow
    state = settings.value("state")
    if state and hasattr(window, "restoreState"):
        window.restoreState(state)
    
    # Restore maximized state
    maximized = settings.value("maximized", False, type=bool)
    if maximized:
        window.showMaximized()
    else:
        pos = settings.value("pos", QPoint(200, 200), type=QPoint)
        size = settings.value("size", QSize(400, 400), type=QSize)
        window.resize(size)
        window.move(pos)
    
    settings.endGroup()
    return True


def save_settings(settings_dict, settings_name="app_settings", group="Settings"):
    """
    Save settings to QSettings.
    
    Args:
        settings_dict (dict): Dictionary of settings to save
        settings_name (str): The name for the settings file
        group (str): The settings group name
    """
    settings = QSettings(settings_name, QSettings.IniFormat)
    settings.beginGroup(group)
    
    for key, value in settings_dict.items():
        settings.setValue(key, value)
    
    settings.endGroup()


def load_settings(settings_name="app_settings", group="Settings"):
    """
    Load settings from QSettings.
    
    Args:
        settings_name (str): The name for the settings file
        group (str): The settings group name
        
    Returns:
        dict: Dictionary of loaded settings
    """
    settings_dict = {}
    settings = QSettings(settings_name, QSettings.IniFormat)
    settings.beginGroup(group)
    
    for key in settings.childKeys():
        settings_dict[key] = settings.value(key)
    
    settings.endGroup()
    return settings_dict


def get_open_filename(caption="Open File", directory="", filter="All Files (*)"):
    """
    Show a file open dialog.
    
    Args:
        caption (str): Dialog caption
        directory (str): Initial directory
        filter (str): File filter string
        
    Returns:
        str: Selected filename or empty string if canceled
    """
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getOpenFileName(
        None, caption, directory, filter, options=options
    )
    return filename


def get_save_filename(caption="Save File", directory="", filter="All Files (*)"):
    """
    Show a file save dialog.
    
    Args:
        caption (str): Dialog caption
        directory (str): Initial directory
        filter (str): File filter string
        
    Returns:
        str: Selected filename or empty string if canceled
    """
    options = QFileDialog.Options()
    filename, _ = QFileDialog.getSaveFileName(
        None, caption, directory, filter, options=options
    )
    return filename


def get_existing_directory(caption="Select Directory", directory=""):
    """
    Show a directory selection dialog.
    
    Args:
        caption (str): Dialog caption
        directory (str): Initial directory
        
    Returns:
        str: Selected directory or empty string if canceled
    """
    options = QFileDialog.Options()
    directory = QFileDialog.getExistingDirectory(
        None, caption, directory, options=options
    )
    return directory


def get_text_input(title="Input", label="Enter value:", default=""):
    """
    Show a text input dialog.
    
    Args:
        title (str): Dialog title
        label (str): Input label
        default (str): Default value
        
    Returns:
        tuple: (text, ok) where text is the entered text and ok is True if OK was clicked
    """
    return QInputDialog.getText(None, title, label, text=default)


def get_item_input(title="Select Item", label="Select an item:", items=None, current=0, editable=False):
    """
    Show an item selection dialog.
    
    Args:
        title (str): Dialog title
        label (str): Input label
        items (list): List of items to select from
        current (int): Index of the current item
        editable (bool): Whether the combo box is editable
        
    Returns:
        tuple: (item, ok) where item is the selected item and ok is True if OK was clicked
    """
    if items is None:
        items = []
    return QInputDialog.getItem(None, title, label, items, current, editable)


def get_int_input(title="Input", label="Enter value:", default=0, min_val=-2147483647, max_val=2147483647, step=1):
    """
    Show an integer input dialog.
    
    Args:
        title (str): Dialog title
        label (str): Input label
        default (int): Default value
        min_val (int): Minimum value
        max_val (int): Maximum value
        step (int): Step value
        
    Returns:
        tuple: (value, ok) where value is the entered value and ok is True if OK was clicked
    """
    return QInputDialog.getInt(None, title, label, default, min_val, max_val, step)


def get_double_input(title="Input", label="Enter value:", default=0.0, min_val=-2147483647, max_val=2147483647, decimals=1):
    """
    Show a double input dialog.
    
    Args:
        title (str): Dialog title
        label (str): Input label
        default (float): Default value
        min_val (float): Minimum value
        max_val (float): Maximum value
        decimals (int): Number of decimal places
        
    Returns:
        tuple: (value, ok) where value is the entered value and ok is True if OK was clicked
    """
    return QInputDialog.getDouble(None, title, label, default, min_val, max_val, decimals)


def get_color(initial=None, title="Select Color"):
    """
    Show a color selection dialog.
    
    Args:
        initial (QColor): Initial color
        title (str): Dialog title
        
    Returns:
        QColor: Selected color or invalid color if canceled
    """
    if initial is None:
        initial = QColor(Qt.white)
    return QColorDialog.getColor(initial, None, title)


def get_font(initial=None, title="Select Font"):
    """
    Show a font selection dialog.
    
    Args:
        initial (QFont): Initial font
        title (str): Dialog title
        
    Returns:
        tuple: (font, ok) where font is the selected font and ok is True if OK was clicked
    """
    if initial is None:
        initial = QFont()
    return QFontDialog.getFont(initial, None, title)