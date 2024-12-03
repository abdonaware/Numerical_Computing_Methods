from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from GUI.steps import StepsDisplay
from GUI.matrix_screen import clear_layout


class Solve(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.steps = ""
        main_layout = QVBoxLayout()
        
        container_layout = QVBoxLayout()

        self.method_label = QLabel("Method:")
        self.method_label.setStyleSheet("color:black;")
        self.method_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.method_label)
        container_layout.addWidget(QLabel(" "))

        execution_time_layout = QHBoxLayout()
        self.execution_time_unit = QLabel("ms")
        self.execution_time_unit.setStyleSheet("color:black;")
        self.execution_time_label = QLabel("Execution Time in ms:")
        self.execution_time_label.setStyleSheet("color:black;")
        self.execution_time_field = QLineEdit()
        self.execution_time_field.setReadOnly(True)
        self.execution_time_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.execution_time_field.setStyleSheet("color:black;")
        
        

        execution_time_layout.addWidget(self.execution_time_label)
        execution_time_layout.addWidget(self.execution_time_field)
        execution_time_layout.addWidget(self.execution_time_unit)
        
        font_metrics = QFontMetrics(self.execution_time_field.font())
        text_width = font_metrics.horizontalAdvance(self.execution_time_field.text()) + 30  
        self.execution_time_field.setFixedWidth(text_width)
        
        container_layout.addLayout(execution_time_layout)
        container_layout.addWidget(QLabel(" "))

        iterations_layout = QHBoxLayout()
        self.iterations_label = QLabel('Number of Iterations:')
        self.iterations_field = QLineEdit()
        self.iterations_field.setReadOnly(True)
        self.iterations_field.setAlignment(Qt.AlignmentFlag.AlignCenter)

        iterations_layout.addWidget(self.iterations_label)
        iterations_layout.addWidget(self.iterations_field)
        font_metrics = QFontMetrics(self.iterations_field.font())
        text_width = font_metrics.horizontalAdvance(self.iterations_field.text()) + 30
        self.iterations_field.setFixedWidth(text_width)
        container_layout.addLayout(iterations_layout)
        self.iterations_space=QLabel("")
        container_layout.addWidget(self.iterations_space)

        self.solve_label = QLabel('Solution is:')
        self.solve_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(self.solve_label)
        container_layout.addWidget(QLabel(" "))
        
        self.solution_layout=QHBoxLayout()
        self.solution_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addLayout(self.solution_layout)
        

        container_widget = QWidget()
        container_widget.setLayout(container_layout)


        main_layout.addWidget(container_widget, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.steps_button=QPushButton("Show Steps")
        self.steps_button.clicked.connect(self.show_steps)
        main_layout.addWidget(self.steps_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        
        
        self.error_message=QLabel("")
        self.error_message.setStyleSheet("""
                max-width: 650px;
                height: 50px;
                background-color: #439A97;
                color: #F3F7EC;
                border-radius: 5px;
                padding: 10px;
                margin: 15px 0;
                font-size: 30px;
        """)
        self.error_message.setVisible(False)
        main_layout.addWidget(self.error_message,alignment=Qt.AlignmentFlag.AlignCenter)

        
        main_layout.addStretch()

        self.Home_button = QPushButton('Home screen')
        self.Home_button.clicked.connect(self.home)
        main_layout.addWidget(self.Home_button, alignment=Qt.AlignmentFlag.AlignHCenter)


        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget{
                font-size: 20px;
                font-family: Arial, sans-serif;
            }
            QLabel{
                font-weight: bold;
                color: #333;
            }
            QLineEdit{
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                min-width: fit-content;
            }
            QPushButton{
                background-color: #439A97;
                color: #F3F7EC;
                border-radius: 5px;
                padding: 10px;
                margin: 15px 0;
                font-size: 20px;
            }
            QPushButton:hover{
                background-color: #62B6B7;
            }
        """)


    def setSolution(self, solution):
        if(len(solution)==4 and (solution[0]=="Doolittle" or solution[0]=="Crout" or solution[0]=="Cholesky" or solution[0]=="Gauss" or solution[0]=="Gauss Jordan")):
            self.steps=solution[3]
        elif(len(solution)==5 and (solution[0]=="Jacobi" or solution[0]=="Gauss Seidel")):
            self.steps=solution[4]
        
        clear_layout(self.solution_layout)
        if solution == "There Is No Unique Solution":
            self.error_message.setText("There Is No Unique Solution")
            self.error_message.setVisible(True)
            self.method_label.setVisible(False)
            self.execution_time_field.setVisible(False)
            self.execution_time_label.setVisible(False)
            self.iterations_field.setVisible(False)
            self.iterations_label.setVisible(False)
            self.iterations_space.setVisible(False)
            self.solve_label.setVisible(False)
            self.steps_button.setVisible(False)
            self.execution_time_unit.setVisible(False)
            return
        
        elif solution=="The Matrix is Not Diagonally Dominant":
            self.error_message.setText("The Matrix is Not Diagonally Dominant")
            self.error_message.setVisible(True)
            self.method_label.setVisible(False)
            self.execution_time_field.setVisible(False)
            self.execution_time_label.setVisible(False)
            self.execution_time_unit.setVisible(False)
            self.iterations_field.setVisible(False)
            self.iterations_label.setVisible(False)
            self.iterations_space.setVisible(False)
            self.solve_label.setVisible(False)
            self.steps_button.setVisible(False)
            self.execution_time_unit.setVisible(False)
            return
        elif solution=="The Matrix is Not Symmetric":
            self.error_message.setText("The Matrix is Not Symmetric")
            self.error_message.setVisible(True)
            self.method_label.setVisible(False)
            self.execution_time_field.setVisible(False)
            self.execution_time_label.setVisible(False)
            self.execution_time_unit.setVisible(False)
            self.iterations_field.setVisible(False)
            self.iterations_label.setVisible(False)
            self.iterations_space.setVisible(False)
            self.solve_label.setVisible(False)
            self.steps_button.setVisible(False)
            self.execution_time_unit.setVisible(False)
            return
        elif solution=="The Matrix is Not Positive Definit":
            self.error_message.setText("The Matrix is Not Positive Definit")
            self.error_message.setVisible(True)
            self.method_label.setVisible(False)
            self.execution_time_field.setVisible(False)
            self.execution_time_label.setVisible(False)
            self.execution_time_unit.setVisible(False)
            self.iterations_field.setVisible(False)
            self.iterations_label.setVisible(False)
            self.iterations_space.setVisible(False)
            self.solve_label.setVisible(False)
            self.steps_button.setVisible(False)
            self.execution_time_unit.setVisible(False)
            return
        else:
            self.error_message.setVisible(False)
            self.method_label.setVisible(True)
            self.execution_time_field.setVisible(True)
            self.execution_time_label.setVisible(True)
            self.execution_time_unit.setVisible(True)
            self.iterations_field.setVisible(True)
            self.iterations_label.setVisible(True)
            self.iterations_space.setVisible(True)
            self.solve_label.setVisible(True)
            self.steps_button.setVisible(True)
            self.execution_time_unit.setVisible(True)
        
        self.execution_time_field.setText(f"{solution[2]/1000000}")
        font_metrics = QFontMetrics(self.execution_time_field.font())
        text_width = font_metrics.horizontalAdvance(f"{round(solution[2], 9)}") + 30 
        self.execution_time_field.setFixedWidth(text_width)
        
        self.method_label.setText(f"Selected method : {solution[0]}")
        if(len(solution)>3):
            self.iterations_field.setText(f"{solution[3]}")
            self.iterations_field.setStyleSheet("color:black;")
        
        sol = solution[1]
        for i in range(len(sol)):
            temp = QVBoxLayout()
            temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            temp2 = QLabel(f"X{i+1}")
            temp2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            temp2.setStyleSheet("font-size:14px;")
            temp.addWidget(temp2)
            res = QLineEdit(f"{sol[i]}")
            res.setReadOnly(True)
            res.setStyleSheet("""
                QLineEdit {
                    background-color: #fff;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    padding: 5px;
                    min-width: fit-content;
                    color:black;
                }
            """)

            res.setFixedWidth(150)
            

            temp.addWidget(res)
            self.solution_layout.addLayout(temp)
            if (solution[0] == "Jacobi" or solution[0] == "Gauss Seidel" ):
                self.iterations_label.setVisible(True)
                self.iterations_field.setVisible(True)
                self.iterations_field.setFixedWidth(70)
                self.iterations_space.setVisible(True)
            else:
                self.iterations_label.setVisible(False)
                self.iterations_field.setVisible(False)
                self.iterations_space.setVisible(False)


    def home(self):
        self.stacked_widget.setCurrentIndex(0)
        
    def show_steps(self):
        step_dialog = StepsDisplay(self.steps)
        step_dialog.exec()
