import mysql.connector

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

    sql = ("Select baby_id, firstname, lastname, date_of_birth, gestational_age_at_birth_in_weeks, "
           "gestational_age_at_birth_in_days and birthweight_grams from baby")
    cursor.execute(sql)

    result_set = cursor.fetchall()
    baby_list = []
    for baby in result_set:
        baby_list.append({'ID': baby[0], 'Firstname': baby[1], 'Lastname': baby[2], 'Gender': baby[3],
                          'Date of Birth': baby[4], 'Gestational Age (weeks)': baby[5],
                          'Gestational Age (days)': baby[6], 'Birthweight (grams)': baby[7]})
    return baby_list


# if __name__ == "__main__":
#     main()
