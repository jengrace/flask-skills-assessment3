from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import locale  # does currency formatting

app = Flask(__name__)

locale.setlocale(locale.LC_ALL, '')

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


def is_number(salary):
    """ Checks if user entered a number for salary requirement. """

    if salary.isdigit():
        return True
    else:
        return False


# YOUR ROUTES GO HERE
@app.route("/")
def home_page():
    """ Show homepage. """

    return render_template("index.html")


@app.route("/application-form", methods=["GET"])
def application_form():
    """ Fill in job application. """

    POSSIBLE_JOBS = ['Software Engineer', 'QA Engineer', 'Product Manager']

    return render_template("application-form.html",
                           possiblejobs=POSSIBLE_JOBS)


@app.route("/application-success", methods=["POST"])
def application_response():
    """ Displays a response that acknowledges user's application. """

    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    salary_req = request.form.get("salaryreq")
    job_title = request.form.get("jobtitle")

    if first_name == '' or last_name == '' or salary_req == '':
        flash("Please fill out all questions!")
        return redirect("/application-form")

    if not is_number(salary_req):
        flash("Please enter numbers only for your salary requirement!")
        return redirect("/application-form")

    salary_req = int(salary_req)
    salary_req = locale.currency(salary_req, grouping=True)

    first_name = first_name.title()
    last_name = last_name.title()

    return render_template("application-response.html",
                            firstname = first_name,
                            lastname = last_name,
                            salaryreq = salary_req,
                            jobtitle = job_title)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
