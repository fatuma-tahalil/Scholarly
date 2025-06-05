from flask import Flask, render_template, request, redirect

"""TO DO LIST"""
# TODO: Turn tables into little div cards

app = Flask(__name__)

# List of scholarships each index is a scholarshop "object"
scholarship_list = []

class Scholarships:
    def __init__(self, name, amount, date_closed, category, date_open, link, priority, difficulty, notes):
        self.name = name
        self.amount = amount
        self.date_closed = date_closed
        self.category = category
        self.date_open = date_open
        self.link = link
        self.priority = priority
        self.difficulty = difficulty
        self.notes = notes

# Maybe have a child class of parent class scholarship
"""class Completed_Scholarships(Scholarships):"""
    
# Connecting this method to our index.html file
@app.route("/", methods=["GET", "POST"])
def add_scholarship():
    global scholarship_list
    # Checks if information from the html form was sent to browser
    # In flask this method is called post
    if request.method == "POST":
        name = str(request.form["name"])
        amount = float(request.form["amount"])
        due_date = request.form["due_date"]

        scholarship_object = Scholarships(
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
        scholarship_list.append(scholarship_object)
        # Tells the browser to make a new GET request
        # Avoids getting duplicate submissions by clearing the entered forms
        return redirect("/")
    # Updating the html file with the scholarship list
    return render_template("index.html", scholarships_list = scholarship_list)

# Allows for automatic updates on the flask browser while debugging
if __name__ == "__main__":
    app.run(debug=True)