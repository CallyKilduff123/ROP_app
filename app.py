
from flask import Flask, url_for, render_template, request, redirect
from datetime import datetime, timedelta
# instantiate flask
app = Flask(__name__)


# PAGE 0 - homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/screening')
def screening():
    return render_template('1_screening.html', title='Screening')


# @app.route('/calculator')
# def calculator():
#     return render_template('2_calculator.html', title='Calculator')


@app.route('/guidance')
def guidance():
    return render_template('3_guidance.html', title='Guidance')


@app.route('/template')
def template():
    return render_template('4_template.html', title='Template')


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
        # validation for upper value? - may need to extend this so that only babies <1501g >31weeks are screened
        if ga_weeks < 22 or ga_weeks > 42:
            error_message = "Please check the provided gestational age."
            return render_template('error.html', error_message=error_message)
            # validation for upper value? - may need to extend this so that only babies <1501g >31weeks are screened

        # Calculate Postnatal Age (PNA) in weeks
        # today and dob are stored as datetime objects so that the difference can be calculated using .days method
        # convert days to weeks (return integer)
        pna_days = (today - dob).days
        pna_weeks = pna_days // 7

        # Calculate Postmenstrual Age (PMA) in weeks
        pma_weeks = ga_weeks + pna_weeks

        # Determine the date for the first ROP screen
        if ga_weeks < 31:
            # First screen at 31 weeks PMA or 4 weeks PNA, whichever is later
            # timedelta method used to calculate a new date by adding or subtracting specific duration from given date.
            # it represents a duration, the difference between two dates or times.
            # here it calculates the difference in weeks between 31 weeks pma and dob using GA at birth (dob)
            # returns the date when the baby will be 31 weeks
            # same with the pna difference b/w 4 weeks pna date and dob and calculates data
            # then chooses the later date (max)
            pma_31_date = dob + timedelta(weeks=(31 - ga_weeks))
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = max(pma_31_date, pna_4_date)
        else:
            # First screen at 36 weeks PMA or 4 weeks PNA, whichever is sooner
            pma_36_date = dob + timedelta(weeks=(36 - ga_weeks))
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = min(pma_36_date, pna_4_date)
        # return the calculator results table with the above variables entered based on entered data
        # method strftime formats the date object (first_screen_date) into a string according to specified format
        return render_template('2b_calculator_results.html', pma_weeks=pma_weeks, pna_weeks=pna_weeks,
                               first_screen_date=first_screen_date.strftime('%Y-%m-%d'))
    # return the calculator template so that user can post in the form
    return render_template('2_calculator.html', title='Calculator')




# use main-trick to run
if __name__ == "__main__":
    app.run(debug=True)