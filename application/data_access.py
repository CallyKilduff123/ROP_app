import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  # password="",
  database="ROP_baby_db"
)


# def main():
#     print(mydb)
#
#     cursor = mydb.cursor()
#
#     sql = ("INSERT INTO baby (firstname, lastname, gender, date_of_birth, gestational_age_at_birth_weeks, "
#            "gestational_age_at_birth_days, birthweight_grams) VALUES (%s, %s, %s, %s, %s, %s, %s)")
#     val = ("Fred", "Flint", 'male', '2024-03-29', 23, 6, 959)
#     cursor.execute(sql, val)
#
#     mydb.commit()
#
#     print(cursor.rowcount, "record inserted.")


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


def remove_baby_by_id(baby_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM baby WHERE baby_id = %s"
    cursor.execute(sql, (baby_id,))
    conn.commit()


def get_this_weeks_screens():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)  # Use `dictionary=True` for results as dictionaries
    cursor.callproc('CalculatePMAandPNAandFirstScreenDate')

    # Initialize an empty list for babies
    babies = []

    # Fetch the results of the stored procedure
    for result in cursor.stored_results():
        babies = result.fetchall()

    # cursor.close()
    # conn.close()

    # Filter babies by screen date between 1st and 8th April 2024
    start_date = datetime.strptime('2024-04-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2024-04-08', '%Y-%m-%d').date()

    filtered_babies = [baby for baby in babies if start_date <= baby['first_screen_date'] <= end_date]
    # filtered_babies = [baby for baby in babies if start_date <= datetime.strptime(baby['first_screen_date'], '%Y-%m-%d').date() <= end_date]

    return filtered_babies

# if __name__ == "__main__":
#     main()
