import sqlite3
from pathlib import Path
import os

def add_to_db(dbpath, name, filepath, Type):
    conn = sqlite3.connect(dbpath)

    c = conn.cursor()
    
    c.execute("INSERT INTO Elements VALUES (\""+ name +"\",\""+ filepath +"\",\""+ Type +"\")")

    conn.commit()

    print("added to database")
    conn.close()

def Init_db(sqlpath, dbpath):
    sqlpath = Path(sqlpath)
    sqlitepath = Path(dbpath)
    print(sqlitepath.exists(), sqlpath.exists())

    if sqlpath.exists():
        if not sqlitepath.exists():
            cmd = 'sqlite3 ' + str(sqlitepath) + ' < ' + str(sqlpath)
            os.system(cmd)
            sqlpath.touch()
            print('Database Created')

        elif sqlitepath.stat().st_size == 0 or sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1:
            try:
                sqlitenewpath = Path('elements_new.sqlite')
                cmd = 'sqlite3 ' + str(sqlitenewpath) + ' < ' + str(sqlpath)
                error = os.system(cmd)
                print(error)
                # if error != 0:
                #      raise Exception('SQL to SQLite conversion error 1')
                # if sqlitenewpath.stat().st_size == 0:
                #      raise Exception('SQL to SQLite conversion error 2')
                os.remove(sqlitepath)
                sqlitenewpath.rename(sqlitepath)
                sqlpath.touch()
                print('Database Updated', sqlpath.stat().st_mtime, sqlitepath.stat().st_mtime)
            except Exception as e:
                sqlitenewpath.unlink()
                print('Error: ', e)
        else:
            print("Database Check: Ok")

def query(table, column, column2=None, q1=None):
    results = []
    conn = sqlite3.connect('Resource/elements.sqlite')

    c = conn.cursor()
    if column2 is not None:
        for row in c.execute("SELECT " + column + " FROM " + table + \
                        " WHERE " + column2 + "=\'" + q1 +"\'"):
            results.append(row[0])
    else:
        for row in c.execute("SELECT " + column + " FROM " + table):
            if column == '*':
                results.append(row)
            else:
                results.append(row[0]) 

    conn.close()
    return results

if __name__=='__main__':
    # conn = sqlite3.connect('Resource/elements.sqlite')

    # c = conn.cursor()
    # for row in c.execute("SELECT name FROM Elements WHERE category='Gates'"):
    #     print(row)

    # conn.close()
    print(query('Elements', 'name', 'category', 'Gates'))