"""
PYUI Enhanced Widgets

This module provides enhanced widgets that extend the functionality of PyQt5 widgets.
"""

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLineEdit, QTextEdit, QLabel, 
    QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QFrame, QGroupBox, QTabWidget, QComboBox, QCheckBox,
    QRadioButton, QSlider, QProgressBar, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon


class StyledButton(QPushButton):
    """
    An enhanced button with built-in styling options.
    """
    
    def __init__(self, text="", icon=None, parent=None, primary=False, danger=False, success=False):
        """
        Initialize a styled button.
        
        Args:
            text (str): The button text
            icon (QIcon): Optional icon for the button
            parent (QWidget): The parent widget
            primary (bool): Whether this is a primary action button
            danger (bool): Whether this is a dangerous action button
            success (bool): Whether this is a success action button
        """
        super().__init__(text, parent)
        
        if icon:
            self.setIcon(icon)
        
        # Apply styling based on button type
        if primary:
            self.setProperty("class", "primary")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1c6ea4;
                }
            """)
        elif danger:
            self.setProperty("class", "danger")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
                QPushButton:pressed {
                    background-color: #a93226;
                }
            """)
        elif success:
            self.setProperty("class", "success")
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2ecc71;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
                QPushButton:pressed {
                    background-color: #1e8449;
                }
            """)


class SearchBox(QLineEdit):
    """
    A line edit with built-in search functionality.
    """
    
    search_triggered = pyqtSignal(str)
    
    def __init__(self, parent=None, placeholder="Search...", auto_search=True):
        """
        Initialize a search box.
        
        Args:
            parent (QWidget): The parent widget
            placeholder (str): Placeholder text
            auto_search (bool): Whether to emit search_triggered on text change
        """
        super().__init__(parent)
        
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
        
        # Add search icon
        self.addAction(QIcon.fromTheme("edit-find"), QLineEdit.LeadingPosition)
        
        # Connect signals
        if auto_search:
            self.textChanged.connect(self.search_triggered)
        self.returnPressed.connect(self._on_return_pressed)
    
    def _on_return_pressed(self):
        """Handle return key press"""
        self.search_triggered.emit(self.text())


class FormLayout(QFormLayout):
    """
    An enhanced form layout with better spacing and alignment.
    """
    
    def __init__(self, parent=None):
        """
        Initialize an enhanced form layout.
        
        Args:
            parent (QWidget): The parent widget
        """
        super().__init__(parent)
        
        self.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setSpacing(10)
        self.setContentsMargins(10, 10, 10, 10)
        
    def add_row(self, label_text, widget):
        """
        Add a row with a label and widget.
        
        Args:
            label_text (str): The label text
            widget (QWidget): The widget to add
            
        Returns:
            QWidget: The added widget
        """
        self.addRow(label_text, widget)
        return widget


class Card(QFrame):
    """
    A card widget with a title, content, and optional actions.
    """
    
    def __init__(self, title="", parent=None):
        """
        Initialize a card widget.
        
        Args:
            title (str): The card title
            parent (QWidget): The parent widget
        """
        super().__init__(parent)
        
        # Set up styling
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            Card {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
        """)
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Add title if provided
        if title:
            self.title_label = QLabel(title)
            self.title_label.setStyleSheet("font-weight: bold; font-size: 16px;")
            self.layout.addWidget(self.title_label)
            
            # Add separator
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            separator.setStyleSheet("background-color: #ddd;")
            self.layout.addWidget(separator)
        
        # Content widget
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 10, 0, 10)
        self.layout.addWidget(self.content)
        
        # Actions widget
        self.actions = QWidget()
        self.actions_layout = QHBoxLayout(self.actions)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setAlignment(Qt.AlignRight)
        self.layout.addWidget(self.actions)
        self.actions.setVisible(False)
    
    def add_widget(self, widget):
        """
        Add a widget to the card content.
        
        Args:
            widget (QWidget): The widget to add
            
        Returns:
            QWidget: The added widget
        """
        self.content_layout.addWidget(widget)
        return widget
    
    def add_layout(self, layout):
        """
        Add a layout to the card content.
        
        Args:
            layout (QLayout): The layout to add
            
        Returns:
            QLayout: The added layout
        """
        self.content_layout.addLayout(layout)
        return layout
    
    def add_action(self, button):
        """
        Add an action button to the card.
        
        Args:
            button (QPushButton): The button to add
            
        Returns:
            QPushButton: The added button
        """
        self.actions_layout.addWidget(button)
        self.actions.setVisible(True)
        return button