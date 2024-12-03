from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pathlib import Path
from PyQt6.QtGui import QDoubleValidator,QIcon,QPixmap
from PyQt6.QtGui import QIntValidator
from logic.calling_method import callingMethod


class Matrix(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.method = ""
        self.stacked_widget = stacked_widget
        self.setStyleSheet("padding: 10px;margin: 0px 0px;font-size: 40px;color:black;")
        # Main layout for the entire widget
        self.main_layout = QVBoxLayout()
        self.is_scaling_enabled = False
        self.is_diagonaldominate_enabled=False

        # Top layout for the back button
        self.methodName_layout = QHBoxLayout()
        self.backButton_latout = QHBoxLayout()

        pixmap = QPixmap(str(Path("Numerical_lab/images/back_icon.png").resolve())).scaled(24, 24)  # Resize to 24x24 pixels
        icon = QIcon(pixmap)

        back_button = QPushButton(self)
        back_button.setIcon(icon)  # Set the icon
        back_button.setIconSize(back_button.sizeHint())  # Adjust icon size if needed
        back_button.setFixedSize(30, 30)
        back_button.setStyleSheet("border:none")
        back_button.clicked.connect(self.go_back_to_methods)
        self.backButton_latout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addLayout(self.backButton_latout)
        # Label for the selected method
        self.label = QLabel(self)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: black;
                margin-left: 20px;
                color:black;
            }
        """)
        self.methodName_layout.addWidget(self.label,alignment=Qt.AlignmentFlag.AlignCenter)

        # Add top layout to main layout
        self.main_layout.addLayout(self.methodName_layout)
        self.input_layout = QHBoxLayout()
        

        
        # Input for matrix size
        self.size_label = QLabel("Enter the size of the matrix (n x n):", self)
        self.size_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
                color:black;
            }
        """)
        self.input_layout.addWidget(self.size_label)

        self.size_input = QSpinBox(self)
        self.size_input.setMinimum(0)
        self.size_input.setMaximum(10)
        self.size_input.valueChanged.connect(self.generate_matrix)
        self.size_input.valueChanged.connect(self.generate_intial_guess)
        self.size_input.setStyleSheet("""
            QSpinBox {
                font-size: 16px;
                background-color:white;
                color:black;
            }
        """)
        self.input_layout.addWidget(self.size_input)
        
        # Input for number of significant figures
        self.sfigures_label = QLabel("Number of Significant Figures:", self)
        self.sfigures_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                margin-bottom: 5px;
                color:black;
            }
        """)
        self.input_layout.addWidget(self.sfigures_label)

        self.sfigures_input = QSpinBox(self)
        self.sfigures_input.setMinimum(1)
        self.sfigures_input.setMaximum(15)
        self.sfigures_input.setValue(1)
        self.sfigures_input.setStyleSheet("""
            QSpinBox {
                font-size: 16px;
                background-color:white;
                color:black;
            }
        """)
        self.input_layout.addWidget(self.sfigures_input)


        # Add the horizontal layout to the main layout
        self.main_layout.addLayout(self.input_layout)

        # Layout for the additional text fields with checkboxes

        # Create a QScrollArea for the matrix grid
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

        # Placeholder for the matrix grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setHorizontalSpacing(0) 
        self.scroll_area.setWidget(self.grid_widget)

        # Add the scroll area to the main layout
        self.main_layout.addWidget(self.scroll_area)
        
        self.intial_guess_layout=QHBoxLayout()
        self.intial_guess_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addLayout(self.intial_guess_layout)
        
        self.text_fields_layout = QHBoxLayout()
        # Second text field with checkbox
        # Second text field with checkbox
        self.checkbox_2 = QCheckBox("Number of iterations", self)
        self.checkbox_2.setStyleSheet("font-size:14px;color:black;")
        self.checkbox_2.stateChanged.connect(self.toggle_field_2)
        self.text_field_2 = QLineEdit(self)
        self.text_field_2.setStyleSheet("height:15px;font-size:14px;padding:7px 2px;background-color:white;color:black;")
        # Integer validator for text_field_2
        integer_validator = QIntValidator(self)
        integer_validator.setBottom(0)  # Optionally set a lower limit if necessary
        self.text_field_2.setValidator(integer_validator)
        self.text_fields_layout.addWidget(self.checkbox_2)
        self.text_fields_layout.addWidget(self.text_field_2)

        # Third text field with checkbox
        self.checkbox_3 = QCheckBox("Abselute Relative Error", self)
        self.checkbox_3.setStyleSheet("font-size:14px;color:black;")
        self.checkbox_3.stateChanged.connect(self.toggle_field_3)
        self.text_field_3 = QLineEdit(self)
        self.text_field_3.setStyleSheet("height:15px;font-size:14px;padding:7px 2px;background-color:white;color:black;")
        # Double validator for text_field_3
        double_validator = QDoubleValidator(self)
        double_validator.setBottom(0)  # No lower limit
        self.text_field_3.setValidator(double_validator)
        self.text_fields_layout.addWidget(self.checkbox_3)
        self.text_fields_layout.addWidget(self.text_field_3)
        
        self.main_layout.addLayout(self.text_fields_layout)
        
        
        

        # Add the text fields layout to the main layout, above the solve button
        
        
        
        # Solve Button
        self.solve_button = QPushButton("Solve", self)
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
        self.solve_button.clicked.connect(self.solve_matrix)
        self.solve_button.setFixedWidth(200)

        # Center the solve button
        self.solve_layout = QHBoxLayout()
        self.solve_layout.addStretch()
        self.solve_layout.addWidget(self.solve_button)
        
        self.scalling_checkBox=QCheckBox("Scalling",self)
        self.scalling_checkBox.setStyleSheet("font-size:14px;color:black;")
        self.scalling_checkBox.stateChanged.connect(self.update_scaling_status)  # Connect to the new method
        self.solve_layout.addWidget(self.scalling_checkBox)
        self.solve_layout.addStretch()
        self.main_layout.addLayout(self.solve_layout)




        self.digonal_checkBox=QCheckBox("convert it to diagonal dominate (if it possible)",self)
        self.digonal_checkBox.setStyleSheet("font-size:14px;color:black;")
        self.digonal_checkBox.stateChanged.connect(self.update_diagonal_status)
        self.solve_layout.addWidget(self.digonal_checkBox)
        self.solve_layout.addStretch()
        self.main_layout.addLayout(self.solve_layout)

        # Set the main layout for the widget
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generate_matrix()
        self.generate_intial_guess()
        
    
    def update_scaling_status(self):
        self.is_scaling_enabled = self.scalling_checkBox.isChecked()

    def update_diagonal_status(self):
        self.is_diagonaldominate_enabled = self.digonal_checkBox.isChecked()
    

    def generate_intial_guess(self):
        
        clear_layout(self.intial_guess_layout)
        
        if(not self.text_field_2.isVisible()):
            return
        matrix_size = self.size_input.value()
        self.initial_Guess=[]
        
        for i in range(matrix_size):
            temp=QVBoxLayout()
            temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            temp2=QLabel(f"X{i+1}")
            temp2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            temp2.setStyleSheet("font-size:14px")
            temp.addWidget(temp2)
            input_field = QLineEdit("0.0", self)
            input_field.setStyleSheet("""
                QLineEdit {
                    font-size: 14px;
                    border: 1px solid #ccc;
                    padding: 5;
                    margin: 0;
                    border-radius: 5px;
                    max-width:60px;
                    background-color:white;
                    color:black;
                }
            """)
            validator = QDoubleValidator(self)
            validator.setBottom(-float('inf'))
            validator.setTop(float('inf'))
            input_field.setValidator(validator)
            temp.addWidget(input_field)
            self.initial_Guess.append(input_field.text())
            self.intial_guess_layout.addLayout(temp)
            

    def display_method(self, method):
        self.method = method
        self.checkbox_2.setChecked(True)
        self.size_input.setValue(0)
        self.sfigures_input.setValue(3)
        self.label.setText(f"Selected Method: {method}")
        if(method=="Gauss" or method=="Gauss Jordan"):
            self.scalling_checkBox.setVisible(True)
        else:
            self.scalling_checkBox.setVisible(False)
            
        if((method=="Jacobi" or method=="Gauss Seidel")):
            self.checkbox_2.setVisible(True)
            self.checkbox_3.setVisible(True)
            self.text_field_2.setVisible(True)
            self.text_field_3.setVisible(True)
            self.digonal_checkBox.setVisible(True)
        else:
            self.checkbox_2.setVisible(False)
            self.checkbox_3.setVisible(False)
            self.text_field_2.setVisible(False)
            self.text_field_3.setVisible(False)
            self.digonal_checkBox.setVisible(False)
        

    def go_back_to_methods(self):
        self.is_scaling_enabled=False
        self.scalling_checkBox.setChecked(False)
        self.stacked_widget.setCurrentIndex(0)

    def generate_matrix(self):
        # Clear any existing input fields
        clear_layout(self.grid_layout)

        matrix_size = self.size_input.value()

        # Dynamically create input fields for the matrix
        self.matrix_inputs = []
        for i in range(matrix_size):
            row_inputs = []
            for j in range(matrix_size + 1):
                temp = QHBoxLayout()
                input_field = QLineEdit("0.0", self)
                input_field.setStyleSheet("""
                    QLineEdit {
                        font-size: 14px;
                        border: 1px solid #ccc;
                        padding: 5;
                        margin: 0;
                        border-radius: 5px;
                        background-color:white;
                        color:black;
                    }
                """)
                validator = QDoubleValidator(self)
                validator.setBottom(-float('inf'))
                validator.setTop(float('inf'))
                input_field.setValidator(validator)

                temp.addWidget(input_field)

                if j == matrix_size:
                    temp2 = QLabel("")
                elif j == matrix_size - 1:
                    temp2 = QLabel(f"X{j + 1} = ")
                else:
                    temp2 = QLabel(f"X{j + 1} + ")

                temp2.setStyleSheet("font-size: 12px; font-weight: bold;margin: 0; padding: 0; color:black;")
                temp.addWidget(temp2)
                temp.setSpacing(0)
                self.grid_layout.addLayout(temp, i, j)
                row_inputs.append(input_field)
            self.matrix_inputs.append(row_inputs)

    def solve_matrix(self):
    # Check if both text_field_2 and text_field_3 are empty when they are enabled
        if self.size_input.value()==0:
            self.show_error_message("Size of matrix cannot be zero")
        elif self.checkbox_2.isVisible() and self.checkbox_2.isChecked() and not self.text_field_2.text():
            self.show_error_message("Please fill in the number of iterations.")
            return
        elif self.checkbox_3.isVisible() and self.checkbox_3.isChecked() and not self.text_field_3.text():
            self.show_error_message("Please fill in the absolute relative error.")
            return
        

        if len(self.matrix_inputs) >= 1:
            if(self.method=="Jacobi" or self.method=="Gauss Seidel"):
                if(self.text_field_2.text()==""):
                    solution=callingMethod(arr=self.matrix_inputs, method=self.method, numberEquations=len(self.matrix_inputs), significantFigures=self.sfigures_input.value(),initialGuess=self.initial_Guess,AbseluteRelativeError=float(self.text_field_3.text()) ,diagonalDominanceEnabled= self.is_diagonaldominate_enabled )
                else:
                    solution=callingMethod(arr=self.matrix_inputs, method=self.method, numberEquations=len(self.matrix_inputs), significantFigures=self.sfigures_input.value(),initialGuess=self.initial_Guess,NumberOfIterations=int(self.text_field_2.text()),diagonalDominanceEnabled= self.is_diagonaldominate_enabled )
            else:
                solution=callingMethod(arr=self.matrix_inputs, method=self.method, numberEquations=len(self.matrix_inputs), significantFigures=self.sfigures_input.value(), scalling=self.is_scaling_enabled)
            self.stacked_widget.setCurrentIndex(3)
            self.stacked_widget.currentWidget().setSolution(solution)
        
        
        
    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Input Error")
        error_dialog.setStyleSheet("font-size:16px;background-color:white;color:black;")
        error_dialog.exec()
    
    def toggle_field_2(self):
        # Enable or disable text_field_2 based on checkbox_2 state
        self.text_field_2.setEnabled(self.checkbox_2.isChecked())
        self.text_field_3.setDisabled(self.checkbox_2.isChecked())
        if(self.checkbox_2.isChecked()):
            self.checkbox_3.setChecked(False)
            self.text_field_3.setText("")
        else:
            self.checkbox_3.setChecked(True)
        
    def toggle_field_3(self):
        # Enable or disable text_field_2 based on checkbox_2 state
        self.text_field_3.setEnabled(self.checkbox_3.isChecked())
        self.text_field_2.setDisabled(self.checkbox_3.isChecked())
        if(self.checkbox_3.isChecked()):
            self.checkbox_2.setChecked(False)
            self.text_field_2.setText("")
        else:
            self.checkbox_2.setChecked(True)

def clear_layout(layout: QLayout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            # If the item is a widget, delete it
            item.widget().deleteLater()
        elif item.layout():
            # If the item is a layout, recursively clear it
            clear_layout(item.layout())

