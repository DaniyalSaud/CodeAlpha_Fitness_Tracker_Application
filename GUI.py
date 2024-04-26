from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QComboBox,QTableWidgetItem,QSpinBox,QDialog,QLineEdit, QDialogButtonBox, QSpacerItem, QSizePolicy,QScrollArea,QWidget,QApplication,QGridLayout
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView,QMainWindow, QMessageBox, QTableWidget ,QInputDialog, QFrame, QPushButton, QHBoxLayout, QVBoxLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
import datetime
import pandas as pd

from const import *
import os

from PyQt5.QtWidgets import QGridLayout

class MainWindow(QMainWindow):
    def __init__(self, today_data,journal_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fitness App")

        # create a grid layout
        self.grid = QGridLayout()
        self.today_data = today_data
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.resize(800,600)
        self.grid.setSpacing(5)
        self.setStyleSheet("background-color: #0d0d0d; color: #fff;")  # set background color to grey
        # create a stats frame at the top
        # self.grid.addWidget(self.stats_frame,1,0)  # add to self.grid at row 0, column 0
        self.stats_frame = StatsFrame(today_data, self)
        self.grid.addWidget(self.stats_frame, 0, 0,alignment=Qt.AlignmentFlag.AlignTop)

        sub_grid = QGridLayout()
        sub_grid.setContentsMargins(10, 1, 10, 10)
        self.fitness_goal_frame = FitnessGoalFrame(journal_data=journal_data, parent=self)
        sub_grid.addWidget(self.fitness_goal_frame, 0,0)  # add to self.grid at row 1, column 0

        self.tday_exercise_list = Today_Exercise_List_Box(self)
        sub_grid.addWidget(self.tday_exercise_list, 1, 0)

        self.tmrw_exercise_list = Tomorrow_Exercise_List_Box(self)
        sub_grid.addWidget(self.tmrw_exercise_list, 2, 0)  

        self.empty_frame = QFrame(self)
        self.empty_frame.setFixedHeight(150)
        self.empty_frame.setStyleSheet("background-color: transparent;")
        sub_grid.addWidget(self.empty_frame, 3, 0)


        # create a widget to hold the self.grid layout
        widget = QWidget()
        widget.setLayout(sub_grid)

        # create a scroll area and set the widget as its child
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
                             QScrollArea{
                             border:none;
                             }
            QScrollBar:vertical {
                border: none;
                background: #2A2A2E;
                width: 10px;
                margin: 15px 0 15px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {   
                background: #5D5D5D;
                min-height: 30px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {   
                background: #909090;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            """)
        self.grid.addWidget(scroll, 1, 0)  # add the scroll area to the self.grid
        main_widget = QWidget()
        main_widget.setLayout(self.grid)
        self.setCentralWidget(main_widget)
        

        self.journal_button = QPushButton("Open Journal", self)
        self.journal_button.setStyleSheet("""QPushButton{
                                          background-color: #0d0d0d; 
                                          color: #fff;
                                          border-radius: 12px;
                                          font-size: 18px;
                                          font-family: Century Gothic;
                                          font-weight: bold;
                                          text-align: center;
                                          }
                                          QPushButton:hover{
                                            background-color: #3b3b3b;
                                          }""")
        self.journal_button.clicked.connect(lambda: JournalTable.open_table(parent = self))
        self.journal_button.resize(140, 50)
        self.plan_button = QPushButton("Set Plan", self)
        self.plan_button.setStyleSheet("""QPushButton{
                                          background-color: #0d0d0d; 
                                          color: #fff;
                                          border-radius: 12px;
                                          font-size: 18px;
                                          font-family: Century Gothic;
                                          font-weight: bold;
                                          text-align: center;
                                          }
                                          QPushButton:hover{
                                            background-color: #3b3b3b;
                                          }""")
        self.plan_button.resize(140, 50)
        self.plan_button.clicked.connect(lambda: Set_Plan_dialog.open_dialog(self, self.tday_exercise_list, self.tmrw_exercise_list))
        self.msre_button = QPushButton("Record Measurement", self)
        self.msre_button.setStyleSheet("""QPushButton{
                                          background-color: #0d0d0d; 
                                          color: #fff;
                                          border-radius: 12px;
                                          font-size: 18px;
                                          font-family: Century Gothic;
                                          font-weight: bold;
                                          text-align: center;
                                          }
                                          QPushButton:hover{
                                            background-color: #3b3b3b;
                                          }""")
        self.msre_button.resize(240, 50)
        self.msre_button.clicked.connect(lambda: Set_measurement_box.open_dialog(today_data, self.stats_frame))
        self.plan_button.resize(140, 50)
        self.openEvent()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if (self.height() > 800):
            self.msre_button.move(self.width()//2 - 120, self.height() - 80)
            self.journal_button.move(self.width() - 180, self.height() - 80)
            self.plan_button.move(self.width() - (self.width()-40), self.height() - 80)
        else:
            self.msre_button.move(self.width()//2 - 120, self.height() - 80)  
            self.journal_button.move(self.width() - 180, self.height() - 80)
            self.plan_button.move(self.width() - (self.width()-40), self.height() - 80)

    def closeEvent(self, event):
        with open('main_data.dn', 'r') as f:
            data = f.readlines()
            goal = data[0].split(':')[-1].strip()
            duration = data[1].split(':')[-1].strip()
            goal_to_reach = data[2].split(':')[-1].strip()
            offset = data[3].split(':')[-1].strip()
            current_day = int(data[4].split(':')[-1].strip())
            start_date = data[5].split(':')[-1].strip()
            last_date = data[6].split(':')[-1].strip()
            exercise = None
            try:
                exercise = data[7].split(':')[-1].strip()
            except:
                pass
            if abs(int(last_date) - datetime.datetime.now().day) > 0:
                current_day += abs(int(last_date) - datetime.datetime.now().day)
                last_date = datetime.datetime.now().day
        with open('main_data.dn', 'w') as f:
            if exercise != None:
                f.write(f"Goal: {goal}\nDuration: {duration}\nGoal to reach: {goal_to_reach}\noffset: {offset}\ncurrent_day: {current_day}\n Start Date: {start_date}\nLast Date: {last_date}\nExercise: {exercise}")
            else:
                f.write(f"Goal: {goal}\nDuration: {duration}\nGoal to reach: {goal_to_reach}\noffset: {offset}\ncurrent_day: {current_day}\n Start Date: {start_date}\nLast Date: {last_date}")
        
        super().closeEvent(event)

    def openEvent(self):
        try:
             with open('today_data.csv', 'w') as f:
                 f.write(f"Day,Height,Weight,BMI\nN/A,N/A,N/A,N/A")
        except:
            print("Could not initialize a new entry! Expect Bugs in Program!")
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                data = f.readlines()
                goal = data[0].split(':')[-1].strip()
                duration = data[1].split(':')[-1].strip()
                goal_to_reach = data[2].split(':')[-1].strip()
                offset = data[3].split(':')[-1].strip()
                current_day = int(data[4].split(':')[-1].strip())
                start_date = data[5].split(':')[-1].strip()
                last_date = data[6].split(':')[-1].strip()
                exercise = None
                try:
                    exercise = data[7].split(':')[-1].strip()
                except:
                    pass
                if abs(int(last_date) - datetime.datetime.now().day) > 0:
                    current_day += abs(int(last_date) - datetime.datetime.now().day)
                    last_date = datetime.datetime.now().day
                
            with open('main_data.dn', 'w') as f:
                if exercise != None:
                    f.write(f"Goal: {goal}\nDuration: {duration}\nGoal to reach: {goal_to_reach}\noffset: {offset}\ncurrent_day: {current_day}\n Start Date: {start_date}\nLast Date: {last_date}\nExercise: {exercise}")
                else:
                    f.write(f"Goal: {goal}\nDuration: {duration}\nGoal to reach: {goal_to_reach}\noffset: {offset}\ncurrent_day: {current_day}\n Start Date: {start_date}\nLast Date: {last_date}")
        

class StatsFrame(QFrame):
    def __init__(self,today_data=None, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.today_data = today_data
        main__layout = QGridLayout()

        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""background-color: #101010;
                           """)

        beauty_frame = QFrame(self);
        beauty_frame.setStyleSheet("""
                background-color: #292929;
                border-radius: 10px;
                                    """)
        
        
        self.Day_label = QLabel(f"Day: {today_data['Day']}", beauty_frame)
        self.Day_label.setFixedSize(100,30)
        self.Day_label.setStyleSheet("""color: #fff; font-size: 18px;
                                    font-family: Century Gothic;
                                     font-weight: bold;
                                     background-color: #222222;
                                    text-align: center;
                                    padding-left: 6px;
                                    """)
        
        self.height_label = QLabel(f"Height: {today_data['Height']}", beauty_frame)
        self.height_label.setFixedSize(150,30)
        self.height_label.setStyleSheet("""color: #fff; font-size: 18px;
                                    font-family: Century Gothic;
                                     font-weight: bold;
                                     background-color: #222222;
                                    padding-left: 4px;
                                    """)    
        
        self.Body_weight_label = QLabel(f"Body Weight: {today_data['Weight']}", beauty_frame)
        self.Body_weight_label.setFixedSize(200,30)
        self.Body_weight_label.setStyleSheet("""color: #fff; font-size: 18px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                     background-color: #222222;
                                        padding-left: 16px;
                                    """)
        
        self.BMI_label = QLabel(f"BMI: {today_data['BMI']}", beauty_frame)
        self.BMI_label.setFixedSize(100,30)
        self.BMI_label.setStyleSheet("""color: #fff; font-size: 18px;
                                    font-family: Century Gothic;
                                     font-weight: bold;
                                     background-color: #222222;
                                    padding-left: 6px;
                                    """)
        
        layout.addWidget(self.Day_label,0,0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.height_label,0,1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Body_weight_label,0,2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.BMI_label,0, 3, alignment=Qt.AlignmentFlag.AlignRight)
        beauty_frame.setLayout(layout)
        main__layout.addWidget(beauty_frame, 0,0)
        self.setLayout(main__layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
    
    def update_data(self):
        self.Day_label.setText(f"Day: {self.today_data['Day']}")
        self.height_label.setText(f"Height: {self.today_data['Height']} cm")
        self.Body_weight_label.setText(f"Body Weight: {self.today_data['Weight']} Kg")
        self.BMI_label.setText(f"BMI: {self.today_data['BMI']}")


class FitnessGoalFrame(QFrame):
    def __init__(self,journal_data, parent=None):
        super().__init__(parent)
        self.resize(700, 100)
        self.setFixedHeight(150)
        self.setStyleSheet("background-color: #15614e;" +
                           "border-radius: 20px;")
        layout = QHBoxLayout()
        self.fitness_label = QLabel("Fitness Goal: N/A", self)
        self.fitness_label.setStyleSheet("""background-color: transparent;
                                    color: #fff;
                                    font-size: 20px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    padding-left: 20px;""")
        pixmap = QPixmap('Dark Blue copy.jpg')
        
        self.goal_label = QLabel("Goal: N/A", self)
        self.goal_label.setStyleSheet("""background-color: transparent;
                                    color: #fff;
                                    font-size: 19px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    padding-top: 10px;
                                    padding-left: 20px;
                                    padding-right: 35px;""")
        
        self.Last_date_label = QLabel("Last Date: N/A", self)
        self.Last_date_label.setStyleSheet("""background-color: transparent;
                                    color: #fff;
                                    font-size: 19px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    padding-left: 20px;
                                     """)  
        # Set goal if previously set and if there is a file holding that previous data
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                data = f.readlines()
                goal = data[0].split(':')[-1].strip()
                duration = data[1].split(':')[-1].strip()
                goal_to_reach = data[2].split(':')[-1].strip()
                self.goal_label.setText(f"Goal: {goal_to_reach}")
                self.Last_date_label.setText(f"Last Date: {(datetime.datetime.now() + datetime.timedelta(days=int(duration))).date().strftime('%d/%m/%Y')}")
                self.fitness_label.setText(f"Fitness Goal: {goal}")

        change_goal = QPushButton("Change Goal", self)
        change_goal.clicked.connect(lambda: change_goal_dialog.get_new_goal(parent=self, journal_data=journal_data))
        change_goal.setFixedSize(160, 30)
        change_goal.setStyleSheet("""
                                  QPushButton{
                                  background-color: #0f0f0f;
                                  color: #0fff00; 
                                  border-radius: 10px;
                                  font-size: 18px;
                                  font-family: Century Gothic;
                                  font-weight: bold;
                                  text-align: center;
                                  }
                                  QPushButton:hover{
                                    background-color: #3b3b3b;
                                   }
                                  QPushButton:pressed{
                                    background-color: #0f0f0f;
                                    color: #00ff00;
                                   }
                                  """)

        layout.addWidget(self.fitness_label, alignment=Qt.AlignmentFlag.AlignLeft)
        sub_layout = QVBoxLayout()
        sub_layout.addWidget(self.goal_label, alignment=Qt.AlignmentFlag.AlignCenter)
        sub_layout.addWidget(self.Last_date_label, alignment=Qt.AlignmentFlag.AlignCenter)
        sub_layout.addWidget(change_goal, alignment=Qt.AlignmentFlag.AlignCenter)
        sub_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addLayout(sub_layout)
        self.setLayout(layout)

    def update_goal(self, goal, duration, goal_to_reach):
        self.goal_label.setText(f"Goal: {goal_to_reach}")
        self.Last_date_label.setText(f"Last Date: {(datetime.datetime.now() + datetime.timedelta(days=int(duration))).date().strftime('%d/%m/%Y')}")
        self.fitness_label.setText(f"Fitness Goal: {goal}")

class Today_Exercise_List_Box(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.exercise_box_list = []
        self.AddOnce = False
        self.resize(700, 250)
        self.addBox = AddExerciseBox(self)
        self.addBox.hide()
        self.sub_layout_ex_box_cnt = 0
        self.setFixedHeight(250)
        self.setStyleSheet("""background-color: #0f141f;
                           border-radius: 20px;
                           """)
        main_layout = QVBoxLayout()
        label = QLabel("Today's Exercise List", self)
        label.setStyleSheet("""background-color: transparent;
                                    color: #fff;
                                    font-size: 22px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    padding-top: 10px;
                                    padding-left: 20px;""")
        main_layout.addWidget(label)
        main_widget = QWidget()
        self.sub_layout = QGridLayout()
       
        self.sub_layout.addWidget(self.addBox, 0, 0)
        
        main_widget.setLayout(self.sub_layout)
        scroll = QScrollArea()  
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
        QScrollBar:horizontal {
            border: none;
            background: #2A2A2E;
            height: 10px;
            margin: 0 15px 0 15px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal {   
            background: #5D5D5D;
            min-width: 30px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal:hover {   
            background: #909090;
        }
        QScrollBar::add-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """)
 
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.openEvent()

    def make_exercise_box(self, boxes_type:list):
        # First, make sure that sub_layout is clear and there is no widget dispayed
        if len(self.exercise_box_list) > 0:
            for widget in self.exercise_box_list:
                try:
                    widget.hide()
                except:
                    pass
                try:
                    self.sub_layout.removeWidget(widget)
                    widget.deleteLater()
                except:
                    pass
            self.exercise_box_list = []

        if self.AddOnce == False:

            self.sub_layout.addWidget(self.addBox, 0, 19)
            self.addBox.show()
            self.AddOnce = True
            self.sub_layout_ex_box_cnt += 1

        # Go through the list and check the type of exercise box to make, then add them to layout and do stuff
        self.sub_layout_ex_box_cnt = 0
        for i in boxes_type:
            exercise_box = ExerciseBox(i.lower(), self)
            self.exercise_box_list.append(exercise_box)
            self.sub_layout.addWidget(exercise_box, 0, self.sub_layout_ex_box_cnt)
            self.sub_layout_ex_box_cnt += 1

            
        endspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sub_layout.addItem(endspacer, 0, 20)

    def update_exercise_box(self, data):
        self.make_exercise_box(data)
    
    def make_extra_box(self, exercise_box_data:dict):
        exercise_box = ExerciseBox(self, data_dict=exercise_box_data)
        self.exercise_box_list.append(exercise_box)
        self.sub_layout.addWidget(exercise_box, 0, self.sub_layout_ex_box_cnt)
        self.sub_layout_ex_box_cnt += 1
        self.sub_layout.removeWidget(self.addBox)   
        self.sub_layout.addWidget(self.addBox, 0, self.sub_layout_ex_box_cnt)
        self.sub_layout_ex_box_cnt += 1
        print("Done")


    def openEvent(self):
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                data = f.readlines()
            if len(data) == 8:  
                ndata = data[7].split(':')[-1].strip()
                ndata = ndata.replace('[', '').replace(']', '').replace('\'', '').split(',')
                ndata = [i.strip() for i in ndata]
                
                # ndata holds all the exercises in a list
                self.make_exercise_box(ndata)
                
            else:
                print("No prior Plan Found!")
                self.sub_layout.addWidget(self.addBox, 0, 9)
                self.exercise_box_list.append(self.addBox)
                self.addBox.show()
                endspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
                self.sub_layout.addItem(endspacer, 0, 10)
        else:
            print("File not found!")

class Tomorrow_Exercise_List_Box(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.exercise_box_list =[]
        self.resize(700, 250)
        self.setFixedHeight(250)
        self.setStyleSheet("""background-color: #131b29;
                           border-radius: 20px;""")
        
        main_layout = QVBoxLayout()
        label = QLabel("Tomorrow's Exercise List", self)
        label.setStyleSheet("""background-color: transparent;
                                    color: #fff;
                                    font-size: 22px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    padding-top: 10px;
                                    padding-left: 20px;""")
    
        main_layout.addWidget(label)
        main_widget = QWidget()
        self.sub_layout = QGridLayout()
    
        main_widget.setLayout(self.sub_layout)
        scroll = QScrollArea()  
        scroll.setWidget(main_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
        QScrollBar:horizontal {
            border: none;
            background: #2A2A2E;
            height: 10px;
            margin: 0 15px 0 15px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal {   
            background: #5D5D5D;
            min-width: 30px;
            border-radius: 5px;
        }
        QScrollBar::handle:horizontal:hover {   
            background: #909090;
        }
        QScrollBar::add-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """)
 
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        self.openEvent()

    def make_exercise_box(self, boxes_type:list):
        # First, make sure that sub_layout is clear and there is no widget dispayed
        if len(self.exercise_box_list) > 0:
            for widget in self.exercise_box_list:
                try:
                    widget.hide()
                except:
                    pass
                try:
                    self.sub_layout.removeWidget(widget)
                    widget.deleteLater()
                except:
                    pass
            self.exercise_box_list = []


        # Go through the list and check the type of exercise box to make, then add them to layout and do stuff
        self.sub_layout_ex_box_cnt = 0
        for i in boxes_type:
            exercise_box = ExerciseBox(i.lower(), self, tmrw_flag=True)
            self.exercise_box_list.append(exercise_box)
            self.sub_layout.addWidget(exercise_box, 0, self.sub_layout_ex_box_cnt)
            self.sub_layout_ex_box_cnt += 1

            
        endspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sub_layout.addItem(endspacer, 0, 20)

    def update_exercise_box(self, data):
        self.make_exercise_box(data)

    def openEvent(self):
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                data = f.readlines()
            if len(data) == 8:
                ndata = data[7].split(':')[-1].strip()
                ndata = ndata.replace('[', '').replace(']', '').replace('\'', '').split(',')
                ndata = [i.strip() for i in ndata]
                
                # ndata holds all the exercises in a list
                self.make_exercise_box(ndata)
                
            else:
                print("Data not found!")
                endspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
                self.sub_layout.addItem(endspacer, 0, 10)
        else:
            print("File not found!")


class ExerciseBox(QFrame):
    def __init__(self, exercise_type, parent=None, tmrw_flag = False, data_dict=None):
        super().__init__(parent)
        self.setFixedHeight(150)
        self.tick_status = False
        self.setFixedWidth(270)
        self.setStyleSheet("""
                           background-color:#000000;
                           border-radius: 20px;"""
                            )

        self.layout = QGridLayout()
        if data_dict == None:
            exercise_name = QLabel(exercise_type.title(), self)

            exercise_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            exercise_name.setStyleSheet("""background-color: transparent;
                                        color: #fff;
                                        font-size: 24px;
                                        font-family: Century Gothic;
                                        font-weight: bold;
                                        """)
            self.layout.addWidget(exercise_name, 0, 0, 1, -1)
            widget_cnt = 1
            # Then make labels of the attributes of exercise
            for i in default.exercise_attr[exercise_type.lower()].keys():
                if i == 'name':
                    continue
                else:
                    # Make Labels of them
                    label = QLabel(f"{i.title()}: {default.exercise_attr[exercise_type.lower()][i]}", self)
                    label.setStyleSheet("""background-color: transparent;
                                        color: #fff;
                                        font-size: 16px;
                                        font-family: Century Gothic;
                                        font-weight: bold;
                                        padding-left: 10px;""")
                    self.layout.addWidget(label, widget_cnt, 0, 1, -1)
                    widget_cnt += 1

        else:

            exercise_name = QLabel(data_dict['name'].title(), self)

            exercise_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
            exercise_name.setStyleSheet("""background-color: transparent;
                                        color: #fff;
                                        font-size: 24px;
                                        font-family: Century Gothic;
                                        font-weight: bold;
                                        """)
            self.layout.addWidget(exercise_name, 0, 0, 1, -1)
            widget_cnt = 1
            # Then make labels of the attributes of exercise
            for i in data_dict.keys():
                if i == 'name':
                    continue
                else:
                    # Make Labels of them
                    label = QLabel(f"{i.title()}: {data_dict[i]}", self)
                    label.setStyleSheet("""background-color: transparent;
                                        color: #fff;
                                        font-size: 16px;
                                        font-family: Century Gothic;
                                        font-weight: bold;
                                        padding-left: 10px;""")
                    self.layout.addWidget(label, widget_cnt, 0, 1, -1)
                    widget_cnt += 1
        
        
        if not tmrw_flag:
            remove_button = QPushButton("Remove", self)
            remove_button.clicked.connect(self.remove_exercise_box)
            remove_button.setStyleSheet("""
                                      QPushButton{
                                        background-color: #0f0f0f;
                                        color: #fff;
                                        border-radius: 9px;
                                        font-size: 16px;
                                        font-family: Century Gothic;
                                        font-weight: bold;
                                        text-align: center;
                                        }
                                        QPushButton:hover{
                                          background-color: #3b3b3b;
                                        }
                                        QPushButton:pressed{
                                          background-color: #0f0f0f;
                                        }""")

            self.layout.addWidget(remove_button, 2, 1)

            mark_button = QPushButton("Mark as Done", self)
            mark_button.setFixedSize(120, 30)
            mark_button.setStyleSheet("""
                                  QPushButton{
                                    background-color: #0f0f0f;
                                    color: #fff;
                                    border-radius: 8px;
                                    font-size: 15px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    text-align: center;
                                    }
                                    QPushButton:hover{
                                      background-color: #3b3b3b;
                                    }
                                    QPushButton:pressed{
                                      background-color: #0f0f0f;
                                    }""")
            mark_button.clicked.connect(self.display_tick)
            self.layout.addWidget(mark_button, 3, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def display_tick(self):
        self.tick_status = True
        tick_frame = QFrame(self)
        tick = QLabel("✓", tick_frame)
        tick_frame.setStyleSheet("""background-color: #5ee340;
                                border-radius: 17px;
                                 """)
        tick_frame.setFixedSize(35, 35)
        tick.setStyleSheet("""color: #fff;
                            font-size: 20px;
                            font-weight: bold;
                           background-color: transparent;
                            padding-left: 3px;
                           padding-top: 4px;""")
        self.layout.addWidget(tick_frame, 0, 1,-1,1,alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignCenter|Qt.AlignmentFlag.AlignRight)

    def remove_exercise_box(self):
        self.deleteLater()

class AddExerciseBox(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                           background-color:#000000;
                           border-radius: 10px;"""
                            )
        self.setFixedSize(150, 150)

        layout = QGridLayout()
        layout.setSpacing(7)
        exercise_name_sketch = QFrame(self)    
        exercise_name_sketch.setStyleSheet("""background-color: rgba(78,78,78, 0.4);
                                             border-radius: 10px;
                                            """)
        exercise_name_sketch.setFixedSize(110,30)
        spacer = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        spacer1 = QSpacerItem(10, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        temp1 = QFrame(self)
        temp1.setFixedSize(100,15)
        temp2 = QFrame(self)
        temp2.setFixedSize(100,15)
        temp3 = QFrame(self)
        temp3.setFixedSize(100,15)
        Add_button = QPushButton("+", self)
        Add_button.setFixedSize(50, 50)

     
        Add_button.setStyleSheet("""QPushButton{
                                          background-color: #0f0f0f; 
                                          color: #fff;
                                          border-radius: 12px;
                                          font-size: 18px;
                                          font-family: Century Gothic;
                                          font-weight: bold;
                                          text-align: center;
                                          }
                                          QPushButton:hover{
                                            background-color: #595959;
                                          }
                                          QPushButton:pressed{
                                            background-color: #1c1c1c;
                                            color: #fff;
                                          }""")
        Add_button.clicked.connect(lambda: add_exercise_diag.open_dialog(self, parent))
        temp1.setStyleSheet("""background-color: rgba(78,78,78, 0.3);
                                border-radius: 6px;
                                    """)
        temp2.setStyleSheet("""background-color: rgba(78,78,78, 0.3);
                                border-radius: 6px;
                                    """)
        temp3.setStyleSheet("""background-color: rgba(78,78,78, 0.3);
                                border-radius: 6px;
                                    """)
        
        layout.addItem(spacer1, 0, 0)
        layout.addWidget(exercise_name_sketch, 1, 0, 1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(spacer, 2, 0)
        layout.addWidget(temp1, 3, 0,1,-1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(spacer1, 4, 0)
        layout.addWidget(temp2, 5, 0,1,-1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(spacer1, 6, 0)
        layout.addWidget(temp3, 7, 0,1,-1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(spacer1, 8, 0)
        layout.addWidget(Add_button, 0, 0,-1,-1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
     

class change_goal_dialog(QDialog):
    def __init__(self, parent=None, journal_data=None):
        super().__init__(parent)
        self.setWindowTitle("Change Goal")
        self.setStyleSheet("background-color: #0d0d0d;")
        layout = QVBoxLayout()
        goal_label = QLabel("Enter your goal", self)
        goal_label.setStyleSheet("""color: #fff;
                            font-size: 14px;
                            font-family: Century Gothic;
                            padding-bottom: 10px;
                            """)
        self.entry = QLineEdit(self)
        self.entry.setStyleSheet("""background-color:#242424;
                                 color: #fff;
                                 font-size: 14px;
                                 font-family: Century Gothic;
                                 border-radius: 4px;
                                 padding-left:10px;""")
        self.entry.setPlaceholderText("Enter your new goal here")
        self.entry.setFixedSize(400,30)
        
        goal_to_reach = QLabel("Enter the goal to reach", self)
        goal_to_reach.setStyleSheet("""color: #fff;
                            font-size: 14px;
                            font-family: Century Gothic;
                            padding-bottom: 10px;
                            """)
        self.entry1 = QLineEdit(self)
        self.entry1.setStyleSheet("""background-color:#242424;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;""")
        self.entry1.setPlaceholderText("Goal to reach..")
        self.entry1.setFixedSize(400,30)

        
        duration_label = QLabel("Duration (in days):   (Range: 1 Day - 6 Months (180 Days))", self)
        duration_label.setStyleSheet("""color: #fff;
                            font-size: 14px;
                            font-family: Century Gothic;
                            padding-bottom: 10px;
                            """)
        
        self.duration = QSpinBox(self)
        self.duration.setFixedSize(150, 30)
        self.duration.setRange(1, 180)  # Set the minimum and maximum values
        
        self.duration.setStyleSheet("""
        QSpinBox {
            background-color: #242424;
            color: #fff;
            font-size: 14px;
            font-family: Century Gothic;
            border-radius: 4px;
            padding-left: 10px;
            }
            """)

        layout.addWidget(goal_label)
        layout.addWidget(self.entry)
        layout.addWidget(goal_to_reach)
        layout.addWidget(self.entry1)
        layout.addWidget(duration_label)
        layout.addWidget(self.duration)
        self.setLayout(layout)
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setStyleSheet("""
                                     background-color: #232323;
                                     color: #fff;
                                     font-size: 16px;
                                     border-radius: 10px;
                                     padding: 8px;
                                     """)
        self.buttonBox.accepted.connect(lambda: self.make_journal_entry(parent))
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)
        

    @staticmethod
    def get_new_goal(journal_data, parent=None):
        dialog = change_goal_dialog(parent, journal_data)
        dialog.exec_()

    def make_journal_entry(self, fitness_parent):
        if self.duration.text() != '' and self.entry.text() != '' and self.entry1.text() != '':
            with open('main_data.dn', 'w') as f:
                day_date_offset = datetime.datetime.now().day
                current_day = 1
                f.write(f"Goal: {self.entry.text()}\nDuration: {self.duration.text()}\nGoal to reach: {self.entry1.text()}\noffset: {day_date_offset-1}\ncurrent_day: {current_day}\nStart Date: {datetime.datetime.now().strftime('%d/%m/%Y')}\nLast Date: {datetime.datetime.now().day}\n")
            fitness_parent.update_goal(self.entry.text(), self.duration.text(), self.entry1.text())
            self.close()

            try:
                if os.path.exists('today_data.csv'):
                    os.remove('today_data.csv')
                if os.path.exists('data.csv'):
                    os.remove('data.csv')
            except:
                print("Could not delete the files! or No Files Found!")
        else:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setText("Please fill in all the fields.")
            msgBox.setStyleSheet("""background-color: #0d0d0d;
                                    color: #fff;
                                    font-size: 14px;
                                    """)
            msgBox.exec_()


class Set_Plan_dialog(QDialog):
    def __init__(self,main_parent, parent, second_parent):
        super().__init__(parent = main_parent)
        self.setWindowTitle("Set Plan")
        self.setStyleSheet("""background-color: #0d0d0d;
                              color : #fff;
                            border: 0px solid #00ff00;
                           border-radius: 6px;
                           
                           """)
        

        self.setFixedSize(400, 440)
        layout = QGridLayout()
        layout.setSpacing(20)
        goal_label = QLabel("Goal: N/A", self)
        goal_label.setStyleSheet("""color: #fff;
                                 font-size: 24px;
                                font-family: Century Gothic;
                                font-weight: bold;""")
        duration_label = QLabel("Duration: N/A", self)
        duration_label.setStyleSheet("""color: #fff;
                                     font-size: 20px;
                                     font-family: Century Gothic;
                                     font-weight: bold;
                                     """)
        
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                file = f.readlines()
                goal = file[0].split(':')[-1].strip()
                duration = file[1].split(':')[-1].strip()
                goal_label.setText(f"Goal: {goal}")
                duration_label.setText(f"Duration: {duration} Days")       
        self.list_boxes = [QComboBox(self) for i in range(6)]

        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addWidget(goal_label, 0, 0,1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(duration_label, 1, 0,1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(QSpacerItem(0, 20), 2, 0)
        for i in range(6):
            self.list_boxes[i].addItem("Select")
            self.list_boxes[i].setFixedWidth(150)
            
            self.list_boxes[i].setStyleSheet("""
                                    background-color: #383838;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;
                                
                                    QComboBox::drop-down {
                                    border: 0px;
                                    background: #383838;
                                    width: 20px;
                                             }
                                             """)
            
            self.list_boxes[i].addItems([f"{j.title()}" for j in default.exercise_list])  # Add items to each QComboBox
            self.list_boxes[i].currentIndexChanged.connect(self.check_duplicates)  # Connect the signal to the slot
            slot_label = QLabel(f"Slot {i+1}", self)
            slot_label.setStyleSheet("""color:#fff;
                                    font-size: 18px;
                                    font-family: Century Gothic;
                                    font-weight: bold;""")
            layout.addWidget(slot_label, i+3, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            layout.addWidget(self.list_boxes[i], i+3, 1, alignment=Qt.AlignmentFlag.AlignRight)
            

        layout.addItem(spacer, 9, 0)
        set_button = QPushButton("Set Plan", self)
        set_button.setFixedSize(100, 30)
        set_button.setStyleSheet("""QPushButton{
                                 background-color: #0f0f0f;
                                color:#fff;
                                font-size: 14px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                border-radius: 10px;
                                 }
                                QPushButton:hover{
                                    background-color:#242424;
                                    }
                                 QPushButton:pressed{
                                    background-color:#0f0f0f;
                                    }""")
        set_button.clicked.connect(lambda: self.save_data_for_exercises(parent, second_parent))
        layout.addWidget(set_button, 10, 0, 1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        spacer1 = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer1, 11, 0)
        self.setLayout(layout)
        
    @staticmethod
    def open_dialog(main_parent=None, parent=None, second_parent=None):
        dialog = Set_Plan_dialog(main_parent, parent, second_parent)
        dialog.exec_()
    
    def check_duplicates(self):
        current_combo = self.sender()  # Get the QComboBox that emitted the signal
        current_index = current_combo.currentIndex()

        if any(combo.currentIndex() == current_index and combo != current_combo for combo in self.list_boxes):
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Duplicate Error")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setText("This item has already been selected.")
            msgBox.setStyleSheet("""
                                 background-color: #0d0d0d;
                                 color: #fff;
                                 font-size: 14px;
                                """)
            msgBox.exec_()
            current_combo.setCurrentIndex(0)  # Reset the selection
    
    def save_data_for_exercises(self, parent, second_parent):
        data = []
        for i in self.list_boxes:
            if i.currentText() != "Select":
                data.append(i.currentText())
        
        if os.path.exists('main_data.dn'):
            with open('main_data.dn', 'r') as f:
                file_data = f.readlines()                
                if len(file_data) == 8:
                    file_data.remove(file_data[-1])

            with open('main_data.dn', 'w') as f:
                f.writelines(file_data)

            with open('main_data.dn', '+a') as f:
                f.write(f"Exercise: {data}")
        
        # Before closing, update the today_exercise frame with new exercise boxes
            parent.update_exercise_box(data)
            second_parent.update_exercise_box(data)
        
        self.close()
            

class Set_measurement_box(QDialog):
    def __init__(self, today_data, stats_ins):
        super().__init__()
        self.setWindowTitle("Set Measurements")
        self.setStyleSheet("background-color: #0d0d0d;")
        self.setFixedSize(400, 200)
        layout = QGridLayout()
        layout.setSpacing(20)
        main_label = QLabel("Today's Measurements", self)
        weight_label = QLabel("Weight: ", self)
        height_label = QLabel("Height: ", self)
        self.weight_entry = QLineEdit(self)
        self.weight_entry.setPlaceholderText("Enter your weight in kg")
        self.weight_entry.setFixedSize(230, 30)
        self.height_entry = QLineEdit(self)
        self.height_entry.setFixedSize(230, 30)
        self.height_entry.setPlaceholderText("Enter your height in cm")
        self.Set_button = QPushButton("Set", self)
        self.Set_button.setFixedSize(100, 30)
        self.Set_button.clicked.connect(lambda: self.save_data(stats_ins=stats_ins, today_data=today_data))
        self.Set_button.setStyleSheet("""QPushButton{
                                    background-color: #0f0f0f;
                                    color:#fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    border-radius: 10px;
                                    }
                                    QPushButton:hover{
                                        background-color:#242424;
                                        }
                                    QPushButton:pressed{
                                        background-color:#0f0f0f;
                                        }""")

        # Set the style for the objects
        main_label.setStyleSheet("""color:#fff;
                                font-size: 24px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                 padding-left: 10px;""")
        weight_label.setStyleSheet("""color:#fff;
                                font-size: 18px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                   padding-left: 10px;""")
        height_label.setStyleSheet("""color:#fff;
                                font-size: 18px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                   padding-left: 10px;""")
        self.weight_entry.setStyleSheet("""background-color:#383838;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;""")
        self.height_entry.setStyleSheet("""background-color:#383838;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;""")
        
        # Extra Right Spacer
        spacerRight = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Placement 
        layout.addWidget(main_label, 0, 0,1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(weight_label, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.weight_entry, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addWidget(height_label, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.height_entry, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addItem(spacerRight, 1, 2)
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addWidget(self.Set_button, 3, 0, 1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(spacer, 3, 0)
        self.setLayout(layout)

    @staticmethod
    def open_dialog(today_data, stats_ins, parent=None):
        dialog = Set_measurement_box(stats_ins=stats_ins, today_data= today_data)
        dialog.exec_()
    
    def save_data(self, today_data, stats_ins):
        weight = self.weight_entry.text()
        height = self.height_entry.text()
        if weight == "" or height == "":
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Error")
            msgBox.setIcon(QMessageBox.Icon.Warning)
            msgBox.setText("Please enter your weight and height.")
            msgBox.setStyleSheet("""
                                 background-color: #0d0d0d;
                                    color: #fff;
                                    font-size: 14px;
                                """)
            msgBox.exec_()
            return
        with open('main_data.dn', 'r') as f:
            data = f.readlines()
            current_day = int(data[4].split(':')[-1].strip())
        
        today_data['Day'] = current_day
        today_data['Weight'] = weight
        today_data['Height'] = height
        today_data['BMI'] = calculate_BMI(int(height), int(weight))
        
        temp_today_data = today_data.copy()
        # Open the today_data.csv and add these measurements to it using pandas library

        # if there is a file Then, i want to add today_data as a whole row to 'data.csv' and also make sure that there is only one row of unique value of 'Day'
        if os.path.exists('data.csv'):
            data = pd.read_csv('data.csv')
            try:
                day_val = int(data['Day'].iloc[-1])
                if day_val == current_day and (today_data['Weight'] != data['Weight'].iloc[-1] or today_data['Height'] != data['Height'].iloc[-1]):
                    data.drop(data.tail(1).index, inplace=True)
                    data = data._append(temp_today_data, ignore_index=True)
                    data.to_csv('data.csv', index=False)
                elif day_val != current_day:
                    data = data._append(temp_today_data, ignore_index=True)
                    data.to_csv('data.csv', index=False)
            except:
                print("Something is wrong! Check Set measurement box! could not find last value in Data file!")
                print('Adding first value to the data file!')
                data = data._append(temp_today_data, ignore_index=True)
                data.to_csv('data.csv', index=False)
        else:
            data = pd.DataFrame(today_data, index=[0])
            data.to_csv('data.csv', index=False)

        today_data = pd.DataFrame(today_data, index=[0])
        today_data.to_csv('today_data.csv', index=False)
        stats_ins.update_data()
        self.close()
        

class add_exercise_diag(QDialog):
    def __init__(self, parent=None, main_parent=None):
        super().__init__(parent)
        self.widget_list = []
        self.main_parent = main_parent
        self.new_exercise_data_dict = dict()
        self.setWindowTitle("Add Exercise")
        self.setStyleSheet("""background-color: #0d0d0d;
                           color: #fff;""")
        self.tmp_entry_boxes = []
        self.resize(400, 200)
        self.layout = QGridLayout()
        self.layout.setSpacing(20)
        main_label = QLabel("Add Exercise", self)
        exercise_label = QLabel("Exercise: ", self)
        self.exercise_entry = QLineEdit(self)
        self.exercise_entry.setPlaceholderText("Enter the exercise name")
        self.exercise_entry.setFixedSize(230, 30)

        exercise_type_label = QLabel("Type: ", self)
        self.exercise_type = QComboBox(self)
        self.exercise_type.addItem("Select")

        for i in default.exercise_list:
            self.exercise_type.addItem(i.title())

        self.add_button = QPushButton("Add", self)
        self.add_button.setFixedSize(100, 30)
        self.add_button.setStyleSheet("""QPushButton{
                                    background-color: #0f0f0f;
                                    color:#fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    border-radius: 10px;
                                    }
                                    QPushButton:hover{
                                        background-color:#242424;
                                        }
                                    QPushButton:pressed{
                                        background-color:#0f0f0f;
                                        }""")
        self.add_button.hide()

        # Set the style for the objects
        main_label.setStyleSheet("""color: #fff;
                                font-size: 24px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                 padding-left: 10px;""")
        exercise_label.setStyleSheet("""color: #fff;
                                font-size: 18px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                   padding-left: 10px;""")
        exercise_type_label.setStyleSheet("""color: #fff;
                                font-size: 18px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                   padding-left: 10px;""")
        self.exercise_entry.setStyleSheet("""background-color: #383838;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;""")
        
        self.exercise_type.setStyleSheet("""background-color: #383838;
                                    color: #fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    border-radius: 4px;
                                    padding-left:10px;""")
        self.exercise_type.currentIndexChanged.connect(lambda: self.make_entry_boxes())
        # Placement
        self.layout.addWidget(main_label, 0, 0,1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
       
        self.layout.addWidget(exercise_label, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.exercise_entry, 1, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(exercise_type_label, 2, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.exercise_type, 2, 1, alignment=Qt.AlignmentFlag.AlignRight)
        
        spacer = QSpacerItem(10, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        spacerHRight = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
    
        self.layout.addItem(spacer, 3, 0)
        self.layout.addItem(spacerHRight, 3, 2)
        self.setLayout(self.layout)
        # Print total number of widgets in the layout

    @staticmethod
    def open_dialog(parent=None, main_parent=None):
        dialog = add_exercise_diag(parent, main_parent)
        dialog.exec_()

    def prep_data_make_entry_box(self, main_parent):
        print("Called Funciton!")
        exercise_name = self.exercise_entry.text()

        for i in self.new_exercise_data_dict.keys():
            self.new_exercise_data_dict[i] = self.tmp_entry_boxes.pop(0).text()

        self.new_exercise_data_dict['name'] = exercise_name
        print("Calling!")
        main_parent.make_extra_box(self.new_exercise_data_dict)
        print("Called!")
        self.close()
    # get the exercise name and all its data from entry boxes
    #then using parent, make the exercise box using methods

    def make_entry_boxes(self):
        widget_cnt = 4
        self.resize(400, 200)
        self.new_exercise_data_dict = dict()
        self.tmp_entry_boxes = []
        if len(self.widget_list) > 0:
            for widget in self.widget_list:
                try:
                    widget.hide()
                except:
                    pass
                try:
                    self.layout.removeWidget(widget)
                    widget.deleteLater()
                except:
                    self.layout.removeItem(widget)
            self.widget_list = []
        exercise_type = self.sender()
        if exercise_type.currentText() == "Select":
            self.add_button.hide()
            return
        exercise_attr = default.exercise_attr[exercise_type.currentText().lower()]
        print("Exercise Type:", exercise_attr)
        for i in exercise_attr.keys():
            if i == "name":
                continue
            label = QLabel(f"{i.title()}: ", self)
            label.setStyleSheet("""color: #fff;
                                font-size: 18px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                padding-left: 10px;""")
            entry = QLineEdit(self)
            entry.setPlaceholderText(f"Enter the {i}")
            entry.setFixedSize(230, 30)
            entry.setStyleSheet("""background-color: #383838;
                                color: #fff;
                                font-size: 14px;
                                font-family: Century Gothic;
                                border-radius: 4px;
                                padding-left:10px;""")
            self.tmp_entry_boxes.append(entry)
            self.new_exercise_data_dict[i] = str()

            self.layout.addWidget(label, widget_cnt, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            self.layout.addWidget(entry, widget_cnt, 1, alignment=Qt.AlignmentFlag.AlignRight)
            self.widget_list.append(label)
            self.widget_list.append(entry)
            widget_cnt += 1
        
        spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        self.layout.addItem(spacer, widget_cnt, 0)
        widget_cnt+=1
        self.widget_list.append(spacer)

        self.add_button = QPushButton("Add", self)
        self.add_button.setFixedSize(100, 30)

        self.add_button.setStyleSheet("""QPushButton{
                                    background-color: #0f0f0f;
                                    color:#fff;
                                    font-size: 14px;
                                    font-family: Century Gothic;
                                    font-weight: bold;
                                    border-radius: 10px;
                                    }
                                    QPushButton:hover{
                                        background-color:#242424;
                                        }
                                    QPushButton:pressed{
                                        background-color:#0f0f0f;
                                        }""")
        self.add_button.hide()
        self.layout.addWidget(self.add_button, widget_cnt, 0, 1, -1, alignment=Qt.AlignmentFlag.AlignCenter)
        widget_cnt+=1
        self.widget_list.append(self.add_button)
        spacer2 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer2, widget_cnt, 0)
        self.add_button.clicked.connect(lambda: self.prep_data_make_entry_box(self.main_parent))
        self.widget_list.append(spacer2)
        self.add_button.show()
        self.adjustSize()        



class JournalTable(QDialog):
    def __init__(self,parent):
        super().__init__(parent)
        self.setWindowTitle('Journal Table')
        self.layout = QVBoxLayout()
        self.label = QLabel("Journal Table", self)
        self.label.setStyleSheet("""color: #fff;
                                font-size: 24px;
                                font-family: Century Gothic;
                                font-weight: bold;
                                padding-left: 10px;""")
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.MSWindowsFixedSizeDialogHint)        
        self.setStyleSheet("""background-color: #0f0f0f;
                           border-radius: 20px;""")
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Day", "Height(cm)", "Weight(kg)", "BMI"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
       
        # Setting stylesheet for them
        self.table.horizontalHeader().setStyleSheet("""
    QHeaderView::section {
        background-color: #0f0f0f;
        color: #fff;
        font-size: 14px;
        font-family: Century Gothic;
        font-weight: bold;
        padding: 4px;
        border: 1px solid #6c6c6c;
        text-align: center;
    }
""")

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.setStyleSheet("""
        QTableWidget {
            background-color: #131b29;
            color: #fff;
            font-size: 14px;
            font-family: Century Gothic;
            font-weight: bold;
            border-radius: 10px;
        }
        QTableWidget::header {
            background-color: #000000;
            color: #fff;
            font-size: 14px;
            font-family: Century Gothic;
            font-weight: bold;
            border-radius: 10px;
        }
        QTableWidget::item {
            border: none;
            padding: 10px;
        }
        QTableWidget::item:selected {
            background-color: #00ff00;
            color: #000;
        }
        QTableWidget::item:hover {
            background-color: #00ff00;
            color: #000;
        }
        QHeaderView::section {
            background-color: #131b29;
            color: #fff;
            font-size: 14px;
            font-family: Century Gothic;
            font-weight: bold;
            border-radius: 10px;
        }
        QScrollBar:vertical {
            border: none;
            background: #131b29;
            width: 10px;
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {
            background: #00ff00;
            min-height: 20px;
        }
        QScrollBar::add-line:vertical {
            background: #00ff00;
            height: 10px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #00ff00;
            height: 10px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        """)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFixedSize(700, 300)

    # Now lets add data from CSV
    
        if os.path.exists('data.csv'):
            data = pd.read_csv('data.csv')
            for i in range(len(data)):
                self.table.insertRow(i)
                for j in range(4):
                    item = QTableWidgetItem(str(data.iloc[i][j]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(i, j, item)
    @staticmethod
    def open_table(parent):
        dialog = JournalTable(parent)
        dialog.exec_()
    