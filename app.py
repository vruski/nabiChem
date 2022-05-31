import sqlite3 as sqt

conn = sqt.connect("hazChem.db")
c = conn.cursor()
def reinitiateDataBase():
	c.execute("""CREATE TABLE compounds(
	serial_num integer,
	chem_name text,
	chem_form blob,
	chem_desc text)""")

def insertNewVal(p,q,r,s):	
	c.execute("""INSERT INTO compounds 					VALUES(??,?,?)""",(p,q,r,s))

conn.commit()
conn.close()