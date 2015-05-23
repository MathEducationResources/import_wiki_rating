from pymongo import MongoClient, DESCENDING
from pymongo.errors import DuplicateKeyError
import datetime


def get_merdb(prod=False):
    if prod:
        print("Loading production database")
        filename = "prod.env"
    else:
        print("Loading local database")
        filename = ".env"
    with open(filename, "r") as f:
        for line in f:
            if "MONGODB_URI" in line:
                MONGODB_URI = line.split('=')[1].strip()
            if prod and "MONGOLAB_DB" in line:
                MONGODB_DB = line.split('=')[1].strip()
    if not prod:
        # Adjust db name to your local name
        MONGODB_DB = "merdb"

    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    return db


def url2questionID(url):
    ''' Returns unique questionID from UBC wiki URL.
    Hence currently only works for UBC.
    '''
    url = url.strip()
    course, exam, question = url.split('/')[-3:]
    return "UBC+%s+%s+%s" % (course, exam, question.replace("Question_", ""))


if __name__ == '__main__':
    db = get_merdb(prod=False)
    print("Available collections: %s" % db.collection_names())
    votes = db.votes
    # index prevents duplicate entries if userID, questionID, time are all same
    # if you want to overwrite anyway you can use the flag below
    overwrite = False
    if overwrite:
        votes.remove(multi=True)  # will be replaced by delete_many() in 3.0
    votes.create_index([("userID", DESCENDING),
                        ("questionID", DESCENDING),
                        ("time", DESCENDING)],
                       unique=True)
    with open("rating_pid_url.csv", "r") as f:
        next(f)
        for line in f:
            userID, pageID, rating_100, time, q_url = line.split(',')
            rating_100 = int(rating_100)
            rating_5 = (rating_100 - 1) / 20 + 1  # 1-20 -> 1, 81-100 -> 5
            questionID = url2questionID(q_url)
            vote = {"userID": userID,
                    "rating": rating_5,
                    "time": datetime.datetime.fromtimestamp(int(time)),
                    "questionID": questionID
                    }
            try:
                votes.insert(vote)
            except DuplicateKeyError:
                print("Duplicate entry found - skipping.")
                # break

    print("Total number of votes: %d" % votes.count())
