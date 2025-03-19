#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pyqtfork Enhanced Widgets Demo

This example demonstrates the enhanced widgets provided by Pyqtfork.

Author: Pyqtfork Contributors
License: GPL v3
"""

import sys
import os

# Add the parent directory to the path so we can import pyqtfork
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

# Import Pyqtfork enhanced widgets
from pyqtfork.widgets import StyledButton, Card, SearchBox, FormLayout
from pyqtfork.utils import show_message, confirm
from pyqtfork.helpers import center_window, get_text_input, get_color


class EnhancedWidgetsDemo(QMainWindow):
    """Demo application for Pyqtfork enhanced widgets"""
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        
        # Set window properties
        self.setWindowTitle('Pyqtfork Enhanced Widgets Demo')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header_label = QLabel('Pyqtfork Enhanced Widgets')
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(header_label)
        
        # Create a card with styled buttons
        buttons_card = Card("Styled Buttons")
        main_layout.addWidget(buttons_card)
        
        # Add buttons to the card
        button_layout = QVBoxLayout()
        buttons_card.add_layout(button_layout)
        
        # Primary button
        primary_btn = StyledButton("Primary Button", primary=True)
        primary_btn.clicked.connect(lambda: show_message("Button Clicked", "You clicked the primary button"))
        button_layout.addWidget(primary_btn)
        
        # Success button
        success_btn = StyledButton("Success Button", success=True)
        success_btn.clicked.connect(lambda: show_message("Button Clicked", "You clicked the success button"))
        button_layout.addWidget(success_btn)
        
        # Danger button
        danger_btn = StyledButton("Danger Button", danger=True)
        danger_btn.clicked.connect(self.confirm_action)
        button_layout.addWidget(danger_btn)
        
        # Create a card with search box
        search_card = Card("Search Box")
        main_layout.addWidget(search_card)
        
        # Add search box to the card
        search_box = SearchBox(placeholder="Search for something...")
        search_box.search_triggered.connect(self.handle_search)
        search_card.add_widget(search_box)
        
        # Create a card with form layout
        form_card = Card("Form Layout")
        main_layout.addWidget(form_card)
        
        # Create form layout
        form_layout = FormLayout()
        form_card.add_layout(form_layout)
        
        # Add form fields
        self.name_input = form_layout.add_row("Name:", QLabel("John Doe"))
        self.email_input = form_layout.add_row("Email:", QLabel("john@example.com"))
        self.phone_input = form_layout.add_row("Phone:", QLabel("555-123-4567"))
        
        # Add action buttons to the form card
        edit_btn = StyledButton("Edit Information", primary=True)
        edit_btn.clicked.connect(self.edit_info)
        form_card.add_action(edit_btn)
        
        # Center the window on the screen
        center_window(self)
        
    def handle_search(self, query):
        """Handle search queries"""
        if query:
            show_message("Search", f"Searching for: {query}")
        
    def confirm_action(self):
        """Show a confirmation dialog"""
        if confirm("Are you sure you want to perform this dangerous action?", "Confirm Action"):
            show_message("Action Confirmed", "The dangerous action was confirmed", 
                        icon=QApplication.style().standardIcon(QApplication.style().SP_MessageBoxWarning))
        
    def edit_info(self):
        """Edit the information in the form"""
        # Get the current text
        current_name = self.name_input.text()
        
        # Show input dialog
        name, ok = get_text_input("Edit Name", "Enter new name:", current_name)
        if ok and name:
            self.name_input.setText(name)
            show_message("Information Updated", "Your information has been updated successfully")


def main():
    """Main application entry point"""
    
    app = QApplication(sys.argv)
    window = EnhancedWidgetsDemo()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()