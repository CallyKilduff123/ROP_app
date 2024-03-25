
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


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        dob_str = request.form['dob']  # Date of Birth
        today = datetime.today()

        # Convert DOB to a datetime object
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        # validation
        if dob > today:
            error_message = "Please provide a valid DOB. Date of birth can not be a future date."
            return render_template('error.html', error_message=error_message)

        ga_weeks = int(request.form['ga_weeks'])  # Gestational Age at Birth in Weeks
        # validation for lower or upper value?

        # Calculate Postnatal Age (PNA) in weeks
        pna_days = (today - dob).days
        pna_weeks = pna_days // 7

        # Calculate Postmenstrual Age (PMA) in weeks
        pma_weeks = ga_weeks + pna_weeks

        # Determine the date for the first ROP screen
        if ga_weeks < 31:
            # First screen at 31 weeks PMA or 4 weeks PNA, whichever is later
            pma_31_date = dob + timedelta(weeks=(31 - ga_weeks))
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = max(pma_31_date, pna_4_date)
        else:
            # First screen at 36 weeks PMA or 4 weeks PNA, whichever is sooner
            pma_36_date = dob + timedelta(weeks=(36 - ga_weeks))
            pna_4_date = dob + timedelta(weeks=4)
            first_screen_date = min(pma_36_date, pna_4_date)

        return render_template('2b_calculator_results.html', pma_weeks=pma_weeks, pna_weeks=pna_weeks,
                               first_screen_date=first_screen_date.strftime('%Y-%m-%d'))

    return render_template('2_calculator.html', title='Calculator')

# @app.route('/ROP/<name>')
# def simple_html_page(name):
#     home_url = url_for('hello_from_flask')
#     return f"""













# use main-trick to run
if __name__ == "__main__":
    app.run(debug=True)