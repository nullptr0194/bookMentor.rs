import psycopg2
import csv
import time

"""
Python script to import all data from Courses csv file. CSV file was made completely manually, and is available
in this repo.

"""


def getTopics(topicsString):
    ret = topicsString.split(',')
    if ret[-1] == "":
        return ret[:-1]
    else:
        return ret


def getFields(row):
    fields = []
    fields.append(row['\ufeffID'])
    fields.append(row['Kurs'])
    fields.append(row['o/i'])
    fields.append(row['ER'] if row['ER'] != "" else None)
    fields.append(row['SIMinGod'] if row['SIMinGod'] != "" else None)
    fields.append(row['IRMinGod'] if row['IRMinGod'] != "" else None)
    fields.append(row['OSMinGod'] if row['OSMinGod'] != "" else None)
    fields.append(row['OTMinGod'] if row['OTMinGod'] != "" else None)
    fields.append(row['OGMinGod'] if row['OGMinGod'] != "" else None)
    fields.append(row['OFMinGod'] if row['OFMinGod'] != "" else None)
    fields.append(row['OEMinGod'] if row['OEMinGod'] != "" else None)
    fields.append(getTopics(row['Tagovi']))
    return fields


start_time = time.time()
conn = None
print('Testing connection...')
try:  # enter db credentials
    conn = psycopg2.connect(
        host='',
        database='',
        user='',
        password=''
    )

    cur = conn.cursor()
    csv_file = open('CoursesProbaCSVa.csv')  # set the right name for the file
    reader = csv.DictReader(csv_file)
    for row in reader:
        fields = getFields(row)
        cur.execute(
            "INSERT INTO \"Courses\" (\"id\",\"Kurs\",\"o/i\",\"ER\",\"SIMinGod\",\"IRMinGod\",\"OSMinGod\",\"OTMinGod\",\"OGMinGod\",\"OFMinGod\",\"OEMinGod\",\"Topics\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)",
            (fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7], fields[8],
             fields[9], fields[10], fields[11]))
    conn.commit()
    cur.close()
    csv_file.close()
except Exception as error:
    print('Error:')
    print(error)
finally:
    if conn is not None:
        conn.close()
        print('Successfully disconnected. It took ' + str(time.time() - start_time) + 'seconds')
