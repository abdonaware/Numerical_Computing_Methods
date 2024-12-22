from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtGui import QIcon, QPixmap, QFont, QIntValidator, QDoubleValidator
import matplotlib.pyplot as plt
import numpy as np
from plot.plotter import Plotter

class NonLinearInput(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.method = ""
        self.stacked_widget = stacked_widget
        self.setStyleSheet("padding: 10px;margin: 0px 0px;font-size: 40px;color:black;")

        # Main layout for the entire widget
        self.main_layout = QVBoxLayout()

        # Top layout for the back button
        self.methodName_layout = QHBoxLayout()
        self.backButton_layout = QHBoxLayout()

        pixmap = QPixmap(str(Path("Numerical_lab/images/back_icon.png").resolve())).scaled(16, 16)  # Resize to 16x16 pixels
        icon = QIcon(pixmap)

        back_button = QPushButton(self)
        back_button.setIcon(icon)  # Set the icon
        back_button.setIconSize(back_button.sizeHint())  # Adjust icon size if needed
        back_button.setFixedSize(20, 20)
        back_button.setStyleSheet(""" 
            QPushButton {
                border: none;
                background-color: transparent;
                min-width: 30px;
                min-height: 30px;
                padding: 0;
                margin: 0;
            }
            QPushButton:hover {
                background-color: #E0F7FA;
            }
        """)
        back_button.clicked.connect(self.go_back)
        self.backButton_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addLayout(self.backButton_layout)

        # Label for the selected method
        self.label = QLabel(self.method)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
                margin-left: 20px;
                color:black;
            }
        """)
        self.methodName_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.methodName_layout)

        # Upper and lower input fields for "x" in the same line
        self.lay_x = QHBoxLayout()
        self.x_upper_label = QLabel("Upper x:", self)
        self.x_upper_label.setStyleSheet(""" QLabel { font-size: 16px; margin-bottom: 5px; color:black; } """)
        
        self.x_upper_input = QLineEdit(self)
        self.x_upper_input.setText("0")  # Set initial value for upper x
        self.x_upper_input.setStyleSheet(""" QLineEdit { font-size: 16px; background-color:white; color:black; } """)
        
        # Set a validator to allow any numeric input (including decimals)
        validator = QDoubleValidator(self)
        validator.setBottom(-float('inf'))  # Allow negative numbers
        validator.setTop(float('inf'))  # Allow large numbers
        self.x_upper_input.setValidator(validator)
        
        self.x_lower_label = QLabel("Lower x:", self)
        self.x_lower_label.setStyleSheet(""" QLabel { font-size: 16px; margin-bottom: 5px; color:black; } """)
        
        self.x_lower_input = QLineEdit(self)
        self.x_lower_input.setText("0")  # Set initial value for lower x
        self.x_lower_input.setStyleSheet(""" QLineEdit { font-size: 16px; background-color:white; color:black; } """)
        
        self.x_lower_input.setValidator(validator)  # Using the same validator for lower x

        self.lay_x.addWidget(self.x_upper_label)
        self.lay_x.addWidget(self.x_upper_input)
        self.lay_x.addWidget(self.x_lower_label)
        self.lay_x.addWidget(self.x_lower_input)

        # Layout for significant figures input (on a separate line)
        self.lay_sfigures = QHBoxLayout()
        self.sfigures_label = QLabel("Number of Significant Figures:", self)
        self.sfigures_label.setStyleSheet(""" QLabel { font-size: 16px; margin-bottom: 5px; color:black; } """)
        
        self.sfigures_input = QSpinBox(self)
        self.sfigures_input.setMinimum(1)
        self.sfigures_input.setMaximum(15)
        self.sfigures_input.setValue(1)
        self.sfigures_input.setStyleSheet(""" QSpinBox { font-size: 16px; background-color:white; color:black; } """)
        
        self.lay_sfigures.addWidget(self.sfigures_label)
        self.lay_sfigures.addWidget(self.sfigures_input)
        self.main_layout.addLayout(self.lay_sfigures)

        # Relative error input (on a separate line)
        self.lay_relative_error = QHBoxLayout()
        self.relativeError_label = QLabel("Relative Error:", self)
        self.relativeError_label.setStyleSheet(""" QLabel { font-size: 16px; margin-bottom: 5px; color:black; } """)
        
        self.relativeError_input = QLineEdit(self)
        self.relativeError_input.setText("1")  # Set initial value
        self.relativeError_input.setStyleSheet(""" QLineEdit { font-size: 16px; background-color:white; color:black; } """)
        
        # Set a validator to allow any numeric input (including decimals)
        validator = QDoubleValidator(self)
        validator.setBottom(-float('inf'))  # Allow negative numbers
        validator.setTop(float('inf'))  # Allow large numbers
        self.relativeError_input.setValidator(validator)

        self.lay_relative_error.addWidget(self.relativeError_label)
        self.lay_relative_error.addWidget(self.relativeError_input)
        self.main_layout.addLayout(self.lay_relative_error)

        # Layout for number of iterations input (on a separate line)
        self.lay_iterations = QHBoxLayout()
        self.iterations_label = QLabel("Number of Iterations:", self)
        self.iterations_label.setStyleSheet(""" QLabel { font-size: 16px; margin-bottom: 5px; color:black; } """)
        
        self.iterations_input = QSpinBox(self)
        self.iterations_input.setMinimum(1)
        self.iterations_input.setMaximum(1000)
        self.iterations_input.setValue(10)  # Default value for iterations
        self.iterations_input.setStyleSheet(""" QSpinBox { font-size: 16px; background-color:white; color:black; } """)
        
        self.lay_iterations.addWidget(self.iterations_label)
        self.lay_iterations.addWidget(self.iterations_input)
        self.main_layout.addLayout(self.lay_iterations)
        self.main_layout.addLayout(self.lay_x)

        # Equation input layout
        self.lay_equation = QVBoxLayout()
        
        # Equation display field
        self.equation_input = QLineEdit(self)
        self.equation_input.setStyleSheet(""" QLineEdit { font-size: 16px; background-color:white; color:black; } """)
        self.equation_input.setPlaceholderText("Enter your equation here")
        
        # Create the Plot button beside the equation input field
        self.plot_button = QPushButton("Plot", self)
        self.plot_button.setStyleSheet(""" QPushButton { font-size: 16px; background-color: #439A97; color:white; } """)
        self.plot_button.clicked.connect(self.plot_equation)

        self.equation_input_layout = QHBoxLayout()
        self.equation_input_layout.addWidget(self.equation_input)
        self.equation_input_layout.addWidget(self.plot_button)

        self.lay_equation.addLayout(self.equation_input_layout)
        
        # Create button layout for numbers and operations
        self.lay_buttons = QGridLayout()

        buttons = [
            ("x", 0, 0), ("sin(", 0, 1), ("cos(", 0, 2),("^", 0, 3), 
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("e", 4, 2), ("+", 4, 3),
            ("(", 5, 0), (")", 5, 1),("delete", 5, 3)  # Clear button
        ]

        for text, row, col in buttons:
            button = QPushButton(text, self)
            button.setStyleSheet(""" QPushButton { font-size: 16px; background-color: #439A97; } """)
            if text == "delete":
                button.clicked.connect(self.delete_last_character)  # Clear last character
            else:
                button.clicked.connect(self.append_to_equation)
            self.lay_buttons.addWidget(button, row, col)
        
        

        self.lay_equation.addLayout(self.lay_buttons)
        self.main_layout.addLayout(self.lay_equation)

        self.solve_button = QPushButton("Solve")
        self.solve_button.setStyleSheet(""" 
            QPushButton {
                background-color: #439A97;
                color: white;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #62B6B7;
            }
        """)
        self.solve_button.clicked.connect(self.solve)  # Fix the connection here
        self.solve_button.setFixedWidth(200)

        # Center the solve button
        self.solve_layout = QHBoxLayout()
        self.solve_layout.addWidget(self.solve_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addLayout(self.solve_layout)


        self.setLayout(self.main_layout)

    def append_to_equation(self):
        button = self.sender()
        current_text = self.equation_input.text()
        new_text = current_text + button.text()
        self.equation_input.setText(new_text)

    def delete_last_character(self):
        current_text = self.equation_input.text()
        if current_text:
            # Check if the last characters form "sin(" or "cos("
            if current_text.endswith("sin(") or current_text.endswith("cos("):
                new_text = current_text[:-4]  # Remove the entire "sin(" or "cos("
            else:
                new_text = current_text[:-1]  # Remove the last character
            self.equation_input.setText(new_text)

    def plot_equation(self):
        plotter1 = Plotter(self.equation_input.text())
        try:
            plotter1.plot_equation()
        except :
            QMessageBox.critical(self, "Error", f"Failed to plot the equation")

    def display_method(self, method):
        self.method = method
        self.label.setText(method)

    def go_back(self):
        self.stacked_widget.setCurrentIndex(2)

    def solve(self):
        print("solve")
        pass





