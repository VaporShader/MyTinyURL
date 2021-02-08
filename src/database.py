import sqlite3
import datetime

sqlite_file = 'url_table.sqlite'  # the name of the sqlite database


# Initialize the SQLite database 
def database_init():
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    # Here we check if there's a table already and if not, we create one 
    cursor.execute("CREATE TABLE IF NOT EXISTS URL(FullURL varchar(32), ShortURL varchar(32), visitCount int)")
    cursor.execute("CREATE TABLE IF NOT EXISTS STATS(FullURL varchar(32), visit_type int, date DATETIME)")
    connection.commit()


# Add a new redirection to the database
# Input - full_URL, short_URL
# Output - None
def add_to_database(full_URL, short_URL):
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM URL WHERE FullURL = ?", (full_URL,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute("INSERT INTO URL ('FullURL', 'ShortURL', 'visitCount') "
                       "VALUES (?, ?, ?)", (full_URL, short_URL, 0))
    connection.commit()


# Gets the redirection from the database
# Input - full_URL, short_URL
# Output - the URL from the database
def get_from_database(long_url, short_URL):
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    if short_URL is None:
        cursor.execute("SELECT ShortURL FROM URL WHERE FullURL = ?", (long_url,))
    else:
        cursor.execute("SELECT FullURL FROM URL WHERE ShortURL = ?", (short_URL,))
    row = cursor.fetchone()
    return False if row is None else row[0]


# Updates each redirection to the statistics database
# Input - full_URL, visit_type
# Output - None
def update_visit(full_URL, visit_type):
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    if visit_type == 1:
        cursor.execute("SELECT * FROM URL WHERE FullURL = ?", (full_URL,))
        visit_count = cursor.fetchone()[2] + 1
        cursor.execute("Update URL set visitCount = ? where FullURL = ?", (visit_count, full_URL,))
    cursor.execute("INSERT INTO STATS ('FullURL', 'visit_type', 'date') "
                   "VALUES (?, ?, ?)", (full_URL, visit_type, datetime.datetime.now()))
    connection.commit()


# Gets the amount of redirections
# Input - None
# Output - String that shows the number of redirections
def get_amount_of_urls():
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM URL")
    row = cursor.fetchone()[0]
    return "There are " + str(row) + " redirections that are registered in the database"


#  Gets the amount of timed redirections
# Input - visit_type (1 for normal 0 for error)
# Output - String that shows the number of redirections
def get_redirection_stats(visit_type):
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    now = datetime.datetime.now()

    delta = now + datetime.timedelta(minutes=-1)
    cursor.execute("SELECT COUNT(*) FROM STATS WHERE visit_type = ? AND "
                   "date BETWEEN ? AND ?", (visit_type, delta, now))
    minute = cursor.fetchone()[0]

    delta = now + datetime.timedelta(hours=-1)
    cursor.execute("SELECT COUNT(*) FROM STATS WHERE visit_type = ? AND "
                   "date BETWEEN ? AND ?", (visit_type, delta, now))
    hour = cursor.fetchone()[0]

    delta = now + datetime.timedelta(days=-1)
    cursor.execute("SELECT COUNT(*) FROM STATS WHERE visit_type = ? AND "
                   "date BETWEEN ? AND ?", (visit_type, delta, now))
    day = cursor.fetchone()[0]

    name = " redirections" if visit_type == 1 else " errors"

    return "There were " + str(minute) + name + " made in the last minute, " + str(hour) + \
           " in the last hour and " + str(day) + " in the last day."
