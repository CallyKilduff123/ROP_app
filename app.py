
from flask import Flask, url_for, render_template
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



# @app.route('/ROP/<name>')
# def simple_html_page(name):
#     home_url = url_for('hello_from_flask')
#     return f"""


















# use main-trick to run
if __name__ == "__main__":
    app.run(debug=True)