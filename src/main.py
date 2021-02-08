from flask import *
import string
import random
from database import *

app = Flask(__name__)

host_name = "localhost"
port_number = 5000


# This Function creates a random 7 char length url address for the short url
# Input - None
# Output - a string that contains the short url
def make_short_url():
    random_char = string.ascii_uppercase + string.ascii_lowercase + string.digits
    while get_from_database(None, random_char) is not False:
        random_char = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choices(random_char, k=7))


# For the main page of the server we send to the user the index.html file
# Which is the front end for the user
# Input - None
# Output - index.html the front end
@app.route('/')
def index():
    return render_template('index.html')


# For each short url we make we can redirect it to the original url
# For that to happen we must get the short url as a parameter
# Then we check if there's already made redirection
# if there is we pull out the database and send
# if its an invalid or a non excising one then send a  404 error to the user
# Input - short_url: the url to work with
# Output - a redirect to the original url OR a 404 error
@app.route('/<short_url>')
def fetch_long_url(short_url):
    long_url = get_from_database(None, str(short_url))
    if long_url is not False:
        update_visit(long_url, 1)  # also for the bonus we update the visit count
        return redirect(long_url)
    else:
        update_visit("NULL", 0)
        return abort(404)

# With this function we receive the data that the front end sent
# Then we return to the user the short url
# Input - None
# Output - the shorten url
@app.route("/receive/", methods=["POST"])
def receive_from_user():
    long_url = request.get_json()
    short_url = get_from_database(long_url, None)
    if short_url is False:
        short_url = make_short_url()
        add_to_database(request.get_json(), short_url)
    return "http://" + host_name + ":" + str(port_number) + "/" + short_url

# Bonus 1 , we send in the stats about the number of redirections
# number of successful and unsuccessful redirections in last day hour and minute
# Input - None
# Output - a html file with the stats
@app.route('/stats')
def stats():
    count = get_amount_of_urls()
    red = get_redirection_stats(1)
    err = get_redirection_stats(0)
    return render_template('stats.html', amount=count, redirections=red, errors=err)


if __name__ == '__main__':
    database_init()
    app.run(host=host_name, port=port_number)
