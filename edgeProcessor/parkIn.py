# https://www.postgresqltutorial.com/postgresql-python/update/
# https://www.geeksforgeeks.org/get-current-timestamp-using-python/ 
import psycopg2
from config import config
import datetime

def park_car(carPlateNum):
    sql = """ UPDATE car_parking
                SET "isParked" = %s,
                    parkin_time = %s
                WHERE license_plate_number = %s"""
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        #print("trying to read configs")
        params = config()
        #print("trying to connect to db")
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        #print("connected to the db")
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (True, str(datetime.datetime.now()), carPlateNum))
        #cur.execute(sql, (False, None, carPlateNum))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows
#park_car("HR26DK8337")
