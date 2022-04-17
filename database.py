import sqlite3


def write_job(type, uptime, version, performance, exposed_ports, server, job_date) -> str:
    """ Used to create db file and tables """
    try:
        conn = sqlite3.connect('database.db')
        print('Opened database OK')
    except Exception as err:
        print('Error connecting to database: %s',str(err))

    conn.execute('CREATE TABLE IF NOT EXISTS jobs(Type, Server, Date, Uptime, Version, Performance, EX_Ports)')
    conn.execute(f"INSERT INTO jobs(Type, Server, Date, Uptime, Version, Performance, EX_Ports)\
        VALUES(\"{type}\" , \"{server}\" , \"{job_date}\", \"{uptime}\", \"{version}\", \"{performance}\", \"{exposed_ports}\" )")

    conn.commit()
    print('Records saved OK\n')

def fetch_jobs():
    """ Used to fetch jobs from database """
    try:
        conn = sqlite3.connect('database.db')
        print('Opened database OK\n')
    except Exception as err:
        print('Error connecting to database: %s',str(err))

    try:
        results = conn.execute("SELECT * FROM jobs")
        print('Database Results:')
        for row in results:
            print(row)
        conn.close()
    except Exception as err:
        if 'no such table' in str(err):
            print('This is a new database, no previous jobs found.')
