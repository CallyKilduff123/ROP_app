
from flask import url_for, render_template, request, redirect, session
from datetime import datetime, timedelta

from application import app
# instantiate flask
# app = Flask(__name__)


# PAGE 0 - homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/screening')
def screening():
    return render_template('1_screening.html', title='Screening')


# input DOB and GA to calculate PMA and PNA and date of first screen based on criteria
# need to use GET and POST methods
# when someone visits calculator page (either via GET or POST) -->
# use the function calculator() to handle what happens next.
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    # if someone enters DOB using post method (usually info entered via some type of form)
    if request.method == 'POST':
        # the entered date of birth is returned from a submitted form and stored as a string in the variable dob_str.
        dob_str = request.form['dob']
        # return today's date (today is a method in datetime class)
        today = datetime.today()

        # Convert stored DOB string to a datetime object
        # "string parse time," parses the string (ie resolves into component parts)
        # representing the date according to a specified format and returns a datetime object: in this case YYYY-MM-DD.
        # this is stored in the varaible dob in datetime format
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        # validation - ensure DOB is in the past
        if dob > today:
            # return the error html page (not the results) with the error message inserted
            # (so that it can be altered here if needed)
            error_message = "Please provide a valid date of birth. It can not be a future date."
            return render_template('error.html', error_message=error_message)

        # Gestational Age at Birth in Weeks
        # turn entered GA data from request form from string into integer to store
        ga_weeks = int(request.form['ga_weeks'])
        # GA days default to 0 if not entered
        ga_days = int(request.form.get('ga_days', 0))

        # validation for upper value? - may need to extend this so that only babies <1501g >31weeks are screened
        if ga_weeks < 22 or ga_weeks > 42 or ga_days <0 or ga_days > 6:
            error_message = "Please check the provided gestational age."
            return render_template('error.html', error_message=error_message)
            # validation for upper value? - may need to extend this so that only babies <1501g >31weeks are screened

        # Calculate Postnatal Age (PNA) in weeks
        # today and dob are stored as datetime objects so that the difference can be calculated using .days method
        # convert days to weeks (return integer)
        total_ga_days = ga_weeks * 7 +ga_days
        pna_days = (today - dob).days
        pna_weeks = pna_days // 7
        pna_days_remainder = pna_days % 7
        # keep track of remainder days for more precise calculation of screening date

        # Calculate Postmenstrual Age (PMA) in weeks
        total_pma_days = total_ga_days + pna_days
        # pma_weeks = ga_weeks + pna_weeks
        pma_weeks = total_pma_days // 7
        pma_days_remainder = total_pma_days % 7


        # Determine the date for the first ROP screen
        if ga_weeks < 31:
            # First screen at 31 weeks PMA or 4 weeks PNA, whichever is later
            # timedelta method used to calculate a new date by adding or subtracting specific duration from given date.
            # it represents a duration, the difference between two dates or times.
            # here it calculates the difference in weeks between 31 weeks pma and dob using GA at birth (dob)
            # returns the date when the baby will be 31 weeks
            # same with the pna difference b/w 4 weeks pna date and dob and calculates data
            # then chooses the later date (max)
            pma_31_date = dob + timedelta(weeks=(31 - ga_weeks), days=-ga_days)
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = max(pma_31_date, pna_4_date)
        else:
            # First screen at 36 weeks PMA or 4 weeks PNA, whichever is sooner
            pma_36_date = dob + timedelta(weeks=(36 - ga_weeks), days=-ga_days)
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = min(pma_36_date, pna_4_date)
        # return the calculator results table with the above variables entered based on entered data
        # method strftime formats the date object (first_screen_date) into a string according to specified format
        return render_template('2b_calculator_results.html', pma_weeks=pma_weeks,
                               pma_days=pma_days_remainder, pna_weeks=pna_weeks, pna_days=pna_days_remainder,
                               first_screen_date=first_screen_date.strftime('%Y-%m-%d'))
    # return the calculator template so that user can post in the form
    return render_template('2_calculator.html', title='Calculator')


@app.route('/guidance')
def guidance():
    return render_template('3_guidance.html', title='Guidance')


@app.route('/template')
def template():
    return render_template('4_template.html', title='Template')


# @app.route('/login')
# def login():
#     return render_template('5_login.html', title='Healthcare Team Secure Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # app.logger.debug("Start of login")
    if request.method == 'POST':
        session['email'] = request.form['email']
        # app.logger.debug("Username is: " + session['username'])
        session['loggedIn'] = True
        session['role'] = 'Healthcare Team'
        return redirect(url_for('healthcare_homepage'))
    return render_template('5_login.html', title="Healthcare Team Secure Login")


@app.route('/healthcare_homepage')
def healthcare_homepage():
    return render_template('6_healthcare_homepage.html', title='healthcare_homepage')

@app.route('/add_baby')
def add_baby():
    return render_template('7_add_baby.html', title='Add baby to list')

@app.route('/full_list')
def full_list():
    return render_template('8_full_list.html', title='Full list of babies on NICU')

@app.route('/this_weeks_screens')
def this_weeks_screens():
    return render_template('9_this_weeks_screens.html', title='List of babies for screening this week')

@app.route('/screen_baby')
def screen_baby():
    return render_template('10_screen_baby.html', title='Screen Baby Now')
