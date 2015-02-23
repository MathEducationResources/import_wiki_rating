import datetime


def obtain_raw(sql_dump):
    '''Rewrites SQL dump to list of votes'''
    with open(sql_dump, 'r') as fin:
        for line in fin:
            if line.startswith("INSERT INTO `w4grb_votes` VALUES"):
                return line.strip().split("VALUES (")[1]


def raw2list_of_tuples(raw):
    list_of_votes = raw.split('),(')
    list_of_votes[-1] = list_of_votes[-1].replace(');', '')
    print('total number of votes: %d' % len(list_of_votes))

    # Re-format to list of lists
    return [quintet.split(',') for quintet in list_of_votes]


if __name__ == '__main__':
    raw = obtain_raw('w4grb.sql')
    list_of_tuples = raw2list_of_tuples(raw)
    with open('rating_pid.csv', 'w') as fout:
        fout.write('userID,pageID,rating,time\n')
        for uid, pid, rating, userIP, raw_time in list_of_tuples:
            fout.write('%s,%s,%s,%s\n' %
                       (uid, pid, rating,
                        datetime.datetime.utcfromtimestamp(float(raw_time))))
