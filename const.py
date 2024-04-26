class default():
    exercise_list = ['pushups', 'situps', 'pullups', 'squats', 'running', 'plank', 'chest stretch',
                     'straight lunges', 'dumbells', 'dumbells rows']
    
    pushup_attr = {'name': 'Pushups', 'reps': 10, 'sets': 3}
    situp_attr = {'name': 'Situps', 'reps': 10, 'sets': 3}
    pullup_attr = {'name': 'Pullups', 'reps': 10, 'sets': 3}
    squat_attr = {'name': 'Squats', 'reps': 10, 'sets': 3}  
    running_attr = {'name': 'Running', 'time': '20 minutes','distance': '2 Km'}
    plank_attr = {'name': 'Plank', 'time': '20 seconds'}
    chest_stretch_attr = {'name': 'Chest Stretch', 'time': '30 seconds'}
    straight_lunges_attr = {'name': 'Straight Lunges', 'reps': 10, 'sets': 3}
    dumbells_attr = {'name': 'Dumbells', 'reps': 10, 'sets': 3, 'weight': '10 Kg'}
    dumbells_rows_attr = {'name': 'Dumbells Rows', 'reps': 10, 'sets': 3, 'weight': '10 Kg'}

    exercise_attr = {'pushups': pushup_attr, 'situps': situp_attr, 'pullups': pullup_attr, 'squats': squat_attr,
                        'running': running_attr, 'plank': plank_attr, 'chest stretch': chest_stretch_attr,
                        'straight lunges': straight_lunges_attr, 'dumbells': dumbells_attr, 'dumbells rows': dumbells_rows_attr}
    



def calculate_BMI(height, weight):
    return float("{:.2f}".format((float(weight) / (int(height)/100)**2)))
