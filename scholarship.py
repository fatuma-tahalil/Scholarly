from flask import Flask, render_template, request, redirect

# Flask acts as our "back-end", storing data and login information 
"""TO DO LIST"""
# TODO:Add a login feature
# TODO: Implement slicing or indexing
# TODO: Add 3 other methods to the scholarship class
# TODO: Add one other of the 5 following for the mark
# TODO: Add CSS and pretty it up
# TODO: Make helpfull meaningfull comments
# TODO: Add extra features if I want

"""Functionality Goals"""
# Add the ability to edit scholarships
# Add the ability to mark scholarships as complete
# Add a nav bar to toggle sign out, finished scholarships and resources
# Create the seperate html page to display finished scholarships


app = Flask(__name__)

# These global variables are necessary because functions 
# that control routes CAN'T have parameters
scholarship_list = [] # Holds all of our scholarship objects in the order they were inputted
num = 0 # Helps in creating a unique ID for the scholarship
edit_scholarship_name = '' # The name of the scholarship we are trying to edit

class Scholarships:
    def __init__(self, identifier, name, amount, date_closed, category, date_open, link, priority, difficulty, notes):
        self.id = identifier
        self.name = name
        self.amount = amount
        self.date_closed = date_closed
        self.category = category
        self.date_open = date_open
        self.link = link
        self.priority = priority
        self.difficulty = difficulty
        self.notes = notes

    # Method that updates the scholarships attributes 
    def update(self, new_name, new_amount, new_date):
        self.name = new_name
        self.amount = new_amount
        self.date = new_date


# Creates a unique identifier for each scholarship
def create_identifier():
    global num
    num+=1
    return("scholarship" + str(num))

# Connecting this method to our index.html file
@app.route("/", methods=["GET", "POST"])
def add_scholarship():
    global scholarship_list
    # Checks if information from the html form was sent to browser
    # In flask this method is called post
    if request.method == "POST":
        name = str(request.form["name"])
        amount = float(request.form["amount"])
        due_date = str(request.form["due_date"])

        unique_identifier = create_identifier()

        scholarship_object = Scholarships(
            identifier = unique_identifier,
            name = name,
            amount = amount,
            date_closed = due_date,
            category="",
            date_open="",
            link="",
            priority="",
            difficulty="",
            notes=""
        )
        # Adds the scholarship object to our list
        scholarship_list.append(scholarship_object)
        # Tells the browser to make a new GET request
        # Avoids getting duplicate submissions by clearing the entered forms
        return redirect("/")
    # Updating the html file with the scholarship list
    return render_template("index.html", scholarships_list = scholarship_list)

# Stores the unqiue name of the scholarship being eddited
@app.route("/get_name", methods=["GET", "POST"])
def get_edit_scholarship_name():
    global scholarship_list
    global edit_scholarship_name
    if request.method == "POST":
        # Stores the name of the scholarship
        # This tells update_scholarship which scholarship box to allow editing in
        edit_scholarship_name = request.form["edit_scholarship_name"]
        # The HTML is then updated to become a form
        # TODO: Ensure only specific scholarship become a form
        return render_template(
            "index.html", 
            scholarships_list = scholarship_list,
            edit_scholarship_name = edit_scholarship_name 
        )

# Takes in the information from the changed form
@app.route("/edit", methods=["GET", "POST"])
def update_scholarship():
    global edit_scholarship_name
    global scholarship_list
    name = str(request.form["new_name"])
    amount = float(request.form["new_amount"])
    due_date = str(request.form["new_due_date"])

    scholarship_index = scholarship_list.index(edit_scholarship_name) # Finds the index that the
    print(scholarship_index)
    Scholarships.update_scholarship_object(scholarship_index, name, amount, due_date)
    # We change the attributes of the scholarship
    for scholarships in scholarship_list:
        # If this scholarship is the one we want to edit
        if scholarships.name == edit_scholarship_name:
            # We edit the attributes of this object with the new ones
            scholarships.update(name, amount, due_date)
            edit_scholarship_name = '' # Empty this variable because we "edited" the scholarship
            break # We no longer need to loop through the list
    return redirect("/")

# Allows for automatic updates on the flask browser while debugging
if __name__ == "__main__":
    app.run(debug=True)