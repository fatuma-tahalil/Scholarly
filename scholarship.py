
# Flask acts as our "back-end", storing data and login information 
from flask import Flask, render_template, request, redirect
from datetime import datetime, date

"""TO DO LIST"""
# TODO: Add 3 other methods to the scholarship class
# TODO: Add CSS and pretty it up
# TODO: Make helpfull meaningfull commenssts
# TODO:Add a login feature that saves users scholarship information

app = Flask(__name__)

# These global variables are necessary because functions 
# that control routes CAN'T have parameters
num = 0 # Helps in creating a unique ID for the scholarship
scholarship_list = [] # Holds all of our scholarship objects in the order they were inputted
edit_scholarship_id = '' # The unique identifier of the scholarship we are trying to edit
completed_scholarship_list = [] # The list of scholarships that have been completed

class Scholarships:
    def __init__(self, identification, is_completed, name, amount, date_closed, date_reminder, category, date_open, link, priority, difficulty, notes):
        self.id = identification
        self.completed = is_completed
        self.name = name
        self.amount = amount
        self.date_closed = date_closed
        self.reminder = date_reminder
        self.category = category
        self.date_open = date_open
        self.link = link
        self.priority = priority
        self.difficulty = difficulty
        self.notes = notes

    # Method that updates the scholarships name, amount and date attributes
    def update(self, new_name, new_amount, new_date):
        self.name = new_name
        self.amount = new_amount
        self.date_closed = new_date

        self.is_due_soon()

    # Method that updates if the scholarship is completed or not
    def mark_completed(self):
        self.completed = True
        
    def is_due_soon(self):
        todays_date = date.today()
        due_date = self.date_closed
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

        if todays_date > due_date:
            self.reminder = "OVERDUE"
        elif todays_date == due_date:
            self.reminder = "DUE TODAY" # Changes the reminder attribute to a string we print on the div
        else:
            self.reminder = None # We preemptively set the reminder to be None meaning the difference is greater than 7

            difference = str(due_date - todays_date)
            # This for loop turns the difference string 
            # into just an integer of the number of days between each dates
            for i in range(len(difference)):
                if difference[i] == " ":
                    difference = difference[:i]
                    break
            # Notifies the user that this scholarship is nearly due
            if int(difference)<=7:
                return_string = "DUE IN: " + str(difference) + " days"
                self.reminder = return_string # Changes the reminder attribute to a string we print on the div
                


def create_identifier():
    global num
    num+=1
    return("scholarship" + str(num))

# Connecting this method to our index.html file
@app.route("/", methods=["GET", "POST"])
def add_scholarship():
    global scholarship_list
    global date_reminder
    # Checks if information from the html form was sent to browser
    # In flask this method is called post
    if request.method == "POST":
        name = str(request.form["name"])
        amount = float(request.form["amount"])
        due_date = str(request.form["due_date"])

        unique_identifier = create_identifier()

        scholarship_object = Scholarships(
            identification = unique_identifier,
            is_completed = False,
            name = name,
            amount = amount,
            date_closed = due_date,
            date_reminder = None,
            category="",
            date_open="",
            link="",
            priority="",
            difficulty="",
            notes=""
        )
        # Gives the scholarship object an attribute to state when it's due
        scholarship_object.is_due_soon()
        
        scholarship_list.append(scholarship_object)
        # Tells the browser to make a new GET request
        # Avoids getting duplicate submissions by clearing the entered forms
        return redirect("/")
    # Updating the html file with the scholarship list
    return render_template("index.html", 
        scholarship_list = scholarship_list
    )

# Stores the name of the scholarships ID that is finished. 
# Prevents it from being in the beginning list
# Stores it in the completed scholarship list to be prinetd on a seperate page

# Checks to see if a scholarship on the list has been marked as completed
@app.route("/is_finished", methods=["GET", "POST"])
def is_finished():
    global scholarship_list
    global completed_scholarship_list

    if request.method == "POST":
        completed_scholarship_id = request.form["completed_scholarship_id"]
        scholarship = find_scholarship(scholarship_list, completed_scholarship_id)
        # The scholarship is marked as completed in its attributes
        scholarship.mark_completed() 
        completed_scholarship_list.append(scholarship) # Adds the completed scholarships to the completed list
        return redirect("/")

# Stores the memory at which this scholarship we want to edit is stored 
# We use this strategy because it is how we can identify the scholarship in the list
@app.route("/get_name", methods=["GET", "POST"])
def get_scholarship():
    global scholarship_list
    global edit_scholarship_id

    if request.method == "POST":
        # This tells update_scholarship function which scholarship box to allow editing in
        # Each scholarship box has a unique id to identify them by
        edit_scholarship_id = request.form["edit_scholarship_id"]
        # The HTML is then updated to become a form
        return render_template(
            "index.html", 
            scholarship_list = scholarship_list,
            edit_scholarship_id = edit_scholarship_id
        )

# Takes in the information from the changed form
# Updates the form with the given information
@app.route("/edit", methods=["GET", "POST"])
def update_scholarship():
    global edit_scholarship_id
    global scholarship_list

    name = str(request.form["new_name"])
    amount = float(request.form["new_amount"])
    due_date = str(request.form["new_due_date"])

    # Finds the index that the object belongs to
    # The id of each scholarships last character tells the position it is in the list
    # We subtract it by one because lists start from 0 but counting starts at 1
    scholarship_index = int(edit_scholarship_id[-1])-1
    scholarship = scholarship_list[scholarship_index]

    scholarship.update(name, amount, due_date)
    edit_scholarship_id = '' # Empty this variable because we "edited" the scholarship
    return redirect("/")

# Prints out the completed scholarships
@app.route("/print_completed", methods=["GET", "POST"])
def print_completed_scholarship():
    global completed_scholarship_list
    return render_template(
    "completed.html", 
    completed_scholarship_list = completed_scholarship_list,
    )

# Looks for the scholarship in the list by the ID then returns the object
def find_scholarship(scholarship_list, scholarship_id):
    for scholarships in scholarship_list:
        if scholarship_id == scholarships.id:
            return(scholarships)

# Allows for automatic updates on the flask browser while debugging
if __name__ == "__main__":
    app.run(debug=True)