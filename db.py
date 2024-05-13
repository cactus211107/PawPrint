import sqlite3,json,re

_db = ''
def initDB(database):
    global _db
    _db = database
    print(f'Initialized database "{_db}"')
class DBOBJECT:
    def __init__(self,o:object):self.o=o
    def fetchone(self)->tuple|None:
        try:return self.o[0]
        except:return None
    def fetchmany(self,size=1)->list[tuple]:
        try:return self.o[:size]
        except:return None
    def fetchall(self)->list[tuple]:return self.o


def execute(sql,params = None):
    global _db
    with sqlite3.connect(_db) as conn:
        r=None #return value
        db=conn.cursor()
        if not _db: # check if database exists
            raise Exception('Database not initialized.')
        try:
            if params:
                r=db.execute(sql,params).fetchall()
            else:
                r=db.execute(sql).fetchall()
            r=DBOBJECT(r)
        except sqlite3.Error as e:
            print(f"Error executing statement: {sql}")
            print(e)
            return -1
        conn.commit()
    return r
def executeFile(path):
    with open(path, 'r') as sql_file:
        sql_statements = sql_file.read()
    statements = re.sub(r'--.*','',sql_statements)
    statements=statements.split(';')
    for statement in statements:
        statement = statement.strip()  # Remove leading/trailing whitespace
        if statement:  # Skip empty statements
            try:
                execute(statement,None)
            except sqlite3.Error as e:
                print(f"Error executing statement: {statement}")
                raise e
def parseResponseAsJSON(response:str)->dict|list|tuple:
    return json.loads(response.replace('(','[').replace(')',']').replace("'",'"'))