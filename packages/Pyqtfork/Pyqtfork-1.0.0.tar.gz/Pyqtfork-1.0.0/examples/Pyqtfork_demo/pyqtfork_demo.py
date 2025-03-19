#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pyqtfork Demo Application

This example demonstrates the basic features of Pyqtfork (formerly PyQt5)
and shows how to create a simple but functional application.

Author: Pyqtfork Contributors
License: GPL v3
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QLineEdit,
                            QTextEdit, QComboBox, QSlider, QCheckBox, QFileDialog,
                            QMessageBox, QTabWidget, QGroupBox, QRadioButton)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap


class PyqtforkDemo(QMainWindow):
    """Main window for the Pyqtfork demo application"""
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        """Initialize the user interface"""
        
        # Set window properties
        self.setWindowTitle('Pyqtfork Demo Application')
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Create header
        header_label = QLabel('Welcome to Pyqtfork Demo')
        header_label.setAlignment(Qt.AlignCenter)
        header_font = QFont('Arial', 18, QFont.Bold)
        header_label.setFont(header_font)
        main_layout.addWidget(header_label)
        
        # Create description
        desc_label = QLabel('This demo showcases the capabilities of Pyqtfork, an enhanced fork of PyQt5')
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # Create tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)
        
        # Create tabs
        self.create_form_tab(tab_widget)
        self.create_controls_tab(tab_widget)
        self.create_display_tab(tab_widget)
        
        # Create bottom buttons
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)
        
        about_btn = QPushButton('About')
        about_btn.clicked.connect(self.show_about)
        bottom_layout.addWidget(about_btn)
        
        bottom_layout.addStretch()
        
        exit_btn = QPushButton('Exit')
        exit_btn.clicked.connect(self.close)
        bottom_layout.addWidget(exit_btn)
        
    def create_form_tab(self, parent):
        """Create the form tab with input fields"""
        
        tab = QWidget()
        parent.addTab(tab, 'Form Demo')
        
        layout = QVBoxLayout(tab)
        
        # Name input
        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)
        
        name_label = QLabel('Name:')
        name_layout.addWidget(name_label)
        
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        
        # Email input
        email_layout = QHBoxLayout()
        layout.addLayout(email_layout)
        
        email_label = QLabel('Email:')
        email_layout.addWidget(email_label)
        
        self.email_input = QLineEdit()
        email_layout.addWidget(self.email_input)
        
        # Country selection
        country_layout = QHBoxLayout()
        layout.addLayout(country_layout)
        
        country_label = QLabel('Country:')
        country_layout.addWidget(country_label)
        
        self.country_combo = QComboBox()
        self.country_combo.addItems(['USA', 'Canada', 'UK', 'Australia', 'Germany', 'France', 'Japan', 'Other'])
        country_layout.addWidget(self.country_combo)
        
        # Comments
        layout.addWidget(QLabel('Comments:'))
        
        self.comments_text = QTextEdit()
        layout.addWidget(self.comments_text)
        
        # Subscribe checkbox
        self.subscribe_check = QCheckBox('Subscribe to newsletter')
        layout.addWidget(self.subscribe_check)
        
        # Submit button
        submit_btn = QPushButton('Submit Form')
        submit_btn.clicked.connect(self.submit_form)
        layout.addWidget(submit_btn)
        
        layout.addStretch()
        
    def create_controls_tab(self, parent):
        """Create the controls tab with various UI controls"""
        
        tab = QWidget()
        parent.addTab(tab, 'Controls Demo')
        
        layout = QVBoxLayout(tab)
        
        # Slider group
        slider_group = QGroupBox('Slider Controls')
        layout.addWidget(slider_group)
        
        slider_layout = QVBoxLayout(slider_group)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        slider_layout.addWidget(self.slider)
        
        self.slider_label = QLabel('Value: 50')
        self.slider.valueChanged.connect(self.update_slider_label)
        slider_layout.addWidget(self.slider_label)
        
        # Radio button group
        radio_group = QGroupBox('Options')
        layout.addWidget(radio_group)
        
        radio_layout = QVBoxLayout(radio_group)
        
        self.radio1 = QRadioButton('Option 1')
        self.radio2 = QRadioButton('Option 2')
        self.radio3 = QRadioButton('Option 3')
        
        self.radio1.setChecked(True)
        
        radio_layout.addWidget(self.radio1)
        radio_layout.addWidget(self.radio2)
        radio_layout.addWidget(self.radio3)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        reset_btn = QPushButton('Reset Controls')
        reset_btn.clicked.connect(self.reset_controls)
        button_layout.addWidget(reset_btn)
        
        save_btn = QPushButton('Save Settings')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addStretch()
        
    def create_display_tab(self, parent):
        """Create the display tab with output display"""
        
        tab = QWidget()
        parent.addTab(tab, 'Display Demo')
        
        layout = QVBoxLayout(tab)
        
        # Text display
        self.display_text = QTextEdit()
        self.display_text.setReadOnly(True)
        self.display_text.setPlaceholderText('Output will be displayed here')
        layout.addWidget(self.display_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        clear_btn = QPushButton('Clear Display')
        clear_btn.clicked.connect(self.clear_display)
        button_layout.addWidget(clear_btn)
        
        test_btn = QPushButton('Test Display')
        test_btn.clicked.connect(self.test_display)
        button_layout.addWidget(test_btn)
        
    def submit_form(self):
        """Handle form submission"""
        
        name = self.name_input.text()
        email = self.email_input.text()
        country = self.country_combo.currentText()
        comments = self.comments_text.toPlainText()
        subscribed = self.subscribe_check.isChecked()
        
        if not name or not email:
            QMessageBox.warning(self, 'Incomplete Form', 'Please fill in your name and email.')
            return
        
        # Display form data
        output = f"Form Submitted:\n\n"
        output += f"Name: {name}\n"
        output += f"Email: {email}\n"
        output += f"Country: {country}\n"
        output += f"Comments: {comments}\n"
        output += f"Subscribed: {'Yes' if subscribed else 'No'}\n"
        
        self.display_text.setPlainText(output)
        
        # Switch to display tab
        tab_widget = self.centralWidget().findChild(QTabWidget)
        tab_widget.setCurrentIndex(2)  # Switch to Display tab
        
        # Show confirmation
        QMessageBox.information(self, 'Form Submitted', 'Your form has been successfully submitted!')
        
    def update_slider_label(self, value):
        """Update the slider value label"""
        
        self.slider_label.setText(f'Value: {value}')
        
    def reset_controls(self):
        """Reset all controls to default values"""
        
        self.slider.setValue(50)
        self.radio1.setChecked(True)
        self.radio2.setChecked(False)
        self.radio3.setChecked(False)
        
    def save_settings(self):
        """Save the current control settings"""
        
        slider_value = self.slider.value()
        
        selected_option = "Option 1"
        if self.radio2.isChecked():
            selected_option = "Option 2"
        elif self.radio3.isChecked():
            selected_option = "Option 3"
        
        output = f"Settings Saved:\n\n"
        output += f"Slider Value: {slider_value}\n"
        output += f"Selected Option: {selected_option}\n"
        
        self.display_text.setPlainText(output)
        
        # Switch to display tab
        tab_widget = self.centralWidget().findChild(QTabWidget)
        tab_widget.setCurrentIndex(2)  # Switch to Display tab
        
    def clear_display(self):
        """Clear the display text area"""
        
        self.display_text.clear()
        
    def test_display(self):
        """Show test data in the display"""
        
        test_text = "Pyqtfork Demo Application\n\n"
        test_text += "This is a demonstration of the Pyqtfork framework capabilities.\n"
        test_text += "Pyqtfork is an enhanced fork of PyQt5 with improved features and usability.\n\n"
        test_text += "Features demonstrated in this application:\n"
        test_text += "- Form input and validation\n"
        test_text += "- Various UI controls (sliders, radio buttons, etc.)\n"
        test_text += "- Text display and formatting\n"
        test_text += "- Dialog windows and notifications\n"
        test_text += "- Tab-based interface organization\n"
        
        self.display_text.setPlainText(test_text)
        
    def show_about(self):
        """Show the about dialog"""
        
        about_text = "Pyqtfork Demo Application\n\n"
        about_text += "Version 1.0.0\n\n"
        about_text += "Pyqtfork is an enhanced fork of PyQt5, providing improved UI development capabilities for Python.\n\n"
        about_text += "License: GPL v3\n"
        
        QMessageBox.about(self, 'About Pyqtfork Demo', about_text)


def main():
    """Main application entry point"""
    
    app = QApplication(sys.argv)
    window = PyqtforkDemo()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()