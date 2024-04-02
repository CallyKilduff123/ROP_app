import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  # password="",
  database="ROP_baby_db"
)


def get_db_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        # password="password",
        database="ROP_baby_db"
    )

    return mydb


def add_baby_to_db(fname, lname, gender, dob, ga_weeks, ga_days, bw):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = ("INSERT INTO baby (firstname, lastname, gender, date_of_birth, gestational_age_at_birth_weeks, "
           "gestational_age_at_birth_days, birthweight_grams) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    val = (fname, lname, gender, dob, ga_weeks, ga_days, bw)
    cursor.execute(sql, val)

    conn.commit()


def get_babies():
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = ("Select baby_id, firstname, lastname, date_of_birth, gender, gestational_age_at_birth_weeks, "
           "gestational_age_at_birth_days, birthweight_grams from baby")
    cursor.execute(sql)

    result_set = cursor.fetchall()
    baby_list = []
    for baby in result_set:
        baby_list.append({'ID': baby[0], 'Firstname': baby[1], 'Lastname': baby[2], 'Gender': baby[3],
                          'Date of Birth': baby[4], 'Gestational Age at Birth (weeks)': baby[5],
                          'Gestational Age at Birth (days)': baby[6], 'Birthweight (grams)': baby[7]})
    print(baby_list)
    return baby_list


def get_baby(baby_id):
    conn = get_db_connection()
    # creates a cursor object from the connection. The cursor is used to execute commands in the database.
    # The dictionary=True argument means that the results from the cursor will be returned as dictionaries,
    # where each dictionary represents a row from the database, with column names as keys.
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM baby WHERE baby_id = %s", (baby_id,))
    # fetchone = fetch only selected baby (compared to fetchall - fetch all in table)
    baby = cursor.fetchone()
    return baby


# def remove_baby_by_id(baby_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     sql = "DELETE FROM baby WHERE baby_id = %s"
#     cursor.execute(sql, (baby_id,))
#     conn.commit()


def get_this_weeks_screens():
    conn = get_db_connection()
    # creates a cursor object from the connection. The cursor is used to execute commands in the database.
    # The dictionary=True argument means that the results from the cursor will be returned as dictionaries,
    # where each dictionary represents a row from the database, with column names as keys.
    cursor = conn.cursor(dictionary=True)
    # executes the stored procedure
    cursor.callproc('CalculatePMAandPNAandFirstScreenDate')

    # Initialise empty list for babies
    babies = []
    # Fetch the results of the stored procedure
    # initializes an empty list named babies.
    # Then iterates over the results of the stored procedure
    # For each result set returned by the stored procedure, it fetches all rows
    # This list contains dictionaries representing the babies fetched from the database,
    # with each dictionary containing baby's details
    for result in cursor.stored_results():
        babies = result.fetchall()
    # Filter babies by screen date between 1st and 8th April 2024
    # need to alter this code to select the upcoming week depending on today's date
    start_date = datetime.strptime('2024-04-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2024-04-08', '%Y-%m-%d').date()
    # for loop: list is created by filtering the babies list.
    # This is done with a list comprehension, which iterates through each baby in babies and checks if the first_screen_date
    # of each baby is within the desired date range.
    filtered_babies = [baby for baby in babies if start_date <= baby['first_screen_date'] <= end_date]
    # filtered_babies = [baby for baby in babies if start_date <= datetime.strptime(baby['first_screen_date'], '%Y-%m-%d').date() <= end_date]
    return filtered_babies

# if __name__ == "__main__":
#     main()
