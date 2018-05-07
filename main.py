from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
import sqlite3
import csv





conn = sqlite3.connect('Participants.db')
c = conn.cursor()
def create_table():
    c.execute("CREATE TABLE if not exists example(Student_Name)")
    conn.commit()
create_table()
class StudentListButton(ListItemButton):
    pass


class StudentDB(BoxLayout):
    # Connects the value in the TextInput widget to these
    # fields
    first_name_text_input = ObjectProperty()
    last_name_text_input = ObjectProperty()
    student_list = ObjectProperty()

    def submit_student(self):
        pass
 
        # Get the student name from the TextInputs
        student_name = (self.last_name_text_input.text
                        + ", " + self.first_name_text_input.text
                        + ": " + self.school_name_text_input.text
                        + ", " + self.subject_name_text_input.text)
 
        # Add the student to the ListView
        self.student_list.adapter.data.extend([student_name])
 
        # Reset the ListView
        self.student_list._trigger_reset_populate()

        c.execute("INSERT INTO example (Student_Name) VALUES (?)", (student_name,))
        conn.commit()

    def spinner_clicked(self, value):
        print("Spinner Value " + value)
        school_name_text_input = value
        return school_name_text_input

    def spinner_clicked2(self, value):
        print("Spinner Value " + value)
        subject_name_text_input = value
        return subject_name_text_input





    def delete_student(self, *args):
 
        # If a list item is selected
        if self.student_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text
 
            # Remove the matching item
            self.student_list.adapter.data.remove(selection)
 
            # Reset the ListView
            self.student_list._trigger_reset_populate()

            print(selection + " Will be deleted")

            conn.execute("DELETE FROM example WHERE (Student_Name) = (?)", (selection,))
            conn.commit()

            



 
    def replace_student(self, *args):
 
        # If a list item is selected
        if self.student_list.adapter.selection:
 
            # Get the text from the item selected
            selection = self.student_list.adapter.selection[0].text
 
            # Remove the matching item
            self.student_list.adapter.data.remove(selection)

            print(selection + " Will be Replaced")

            conn.execute("DELETE FROM example WHERE (Student_Name) = (?)", (selection,))
            conn.commit()

            # Get the student name from the TextInputs
            student_name = (self.last_name_text_input.text
                            + ", " + self.first_name_text_input.text
                            + ": " + self.school_name_text_input.text
                            + ", " + self.subject_name_text_input.text)
 
            # Add the updated data to the list
            self.student_list.adapter.data.extend([student_name])

            print(selection + " Will be Replaced By "+student_name)

            c.execute("INSERT INTO example (Student_Name) VALUES (?)", (student_name,))
            conn.commit()

            # Reset the ListView
            self.student_list._trigger_reset_populate()
    def load_students(self, *args):
        sql = "SELECT * FROM example"
        for row in c.execute(sql):
            print(row)
            student_name = (row[0])
            self.student_list.adapter.data.extend([student_name])

            self.student_list._trigger_reset_populate()
    def print_csv(self, *args):
        sql = "SELECT * FROM example"
        with open('Participants.csv', 'w') as file:
            csv_writer = csv.writer(file)
            for row in c.execute(sql):
                csv_writer.writerow(row)
                







 
class StudentDBApp(App):
    def build(self):
        return StudentDB()
 
 
dbApp = StudentDBApp()

dbApp.run()
