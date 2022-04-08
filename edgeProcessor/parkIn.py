# https://www.postgresqltutorial.com/postgresql-python/connect/
# https://www.postgresqltutorial.com/postgresql-python/update/
# https://www.postgresqltutorial.com/postgresql-python/insert/
# https://www.geeksforgeeks.org/get-current-timestamp-using-python/
# https://www.postgresqltutorial.com/postgresql-python/transaction/
import psycopg2
from config import config
import datetime

def park_car(carPlateNum, plAddr):
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
        
        cur.execute(f"SELECT parking_logic_refined('{carPlateNum}', '{plAddr}')")
        # get the number of updated rows
        updated_rows = cur.rowcount
        
        # get result for the parking
        result = cur.fetchone()[0]

        # close the communication with the PostgreSQL
        cur.close()
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        return result
    finally:
        if conn is not None:
            conn.close()

    #return result


def get_free_spots(plAddr):
    conn = None
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
        
        cur.execute(f"SELECT free_spots FROM administrators_parkinglot WHERE street_address = '{plAddr}';")
        
        # get result for the parking
        result = cur.fetchone()[0]

        # close the communication with the PostgreSQL
        cur.close()
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        return result
    finally:
        if conn is not None:
            conn.close()

    #return result;
#print(park_car("HR26DK8337"))
#print(get_free_spots("UCC"))
def get_admin_contactInfo(plAddr):
    conn = None
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
        
        cur.execute(f"SELECT phone FROM administrators_parkinglot WHERE street_address = '{plAddr}';")
        
        # get result for the parking
        result = cur.fetchone()[0]

        # close the communication with the PostgreSQL
        cur.close()
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        return result
    finally:
        if conn is not None:
            conn.close()

def get_fee_info(plAddr):
    conn = None
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
        
        cur.execute(f"SELECT fee_per_hour FROM administrators_parkinglot WHERE street_address = '{plAddr}';")
        
        # get result for the parking
        result = cur.fetchone()[0]

        # close the communication with the PostgreSQL
        cur.close()
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        return result
    finally:
        if conn is not None:
            conn.close()
            
def get_overdue_info(plAddr):
    conn = None
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
        
        cur.execute(f"SELECT max_overdue FROM administrators_parkinglot WHERE street_address = '{plAddr}';")
        
        # get result for the parking
        result = cur.fetchone()[0]

        # close the communication with the PostgreSQL
        cur.close()
        # Commit the changes to the database
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        return result
    finally:
        if conn is not None:
            conn.close()
#print(get_fee_info('UCC'))
            
if __name__ == '__main__':
    print(get_fee_info('OLC 100 R'))
    print(get_free_spots('OLC 100 R'))
    print(get_overdue_info('OLC 100 R'))
    print(park_car('HR26DK8337', 'OLC 100 R'))