from bottle import route, template, run, post, get, request,static_file
import sqlite3 as sqt
import os

####DATA BASE FUNCS START HERE####

conn = sqt.connect("chemicals.db")
c = conn.cursor()
def reinitiateDataBase():
	c.execute("""CREATE TABLE compounds(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	chem_name text,
	chem_weight blob,
	chem_price float,
	chem_retail integer)""")

def insertNewVal(q,r,s,t):
	with conn:	
		c.execute("""INSERT INTO compounds 					VALUES(null,?,?,?,?)""",(q,r,s,t))

def get_chem_name(x):
	c.execute("""SELECT * FROM compounds WHERE chem_name = ?""",(x,))
	return c.fetchone()

def update_chem_name(j,k):
	with conn:
		c.execute("""UPDATE compounds SET 					chem_name = j WHERE serial_num = k """,(j,k))

####DATA BASE FUNCS END HERE ####

##WEB
##SEARCH HOMEPAGE FUNCS START HERE##

@route("/static/<filename>")
def server_static(filename):
    return static_file(filename, root="./static")

@get("/")
def home():
    return template("index.html")
    

@post("/")
def search():
    x = request.forms.get("search")
    y = get_chem_name(x)
    lis = []
    try:
        for z in y:
            lis.append(z)
        if y:
            return template("search.html",ans=lis)
        else:
            return template("error.html")
    except TypeError:
        return template("error.html")

##SEARCH HOMEPAGE FUNCS END HERE##

#####INSERT NEW VALUES START HERE####

@get('/insert')
def insertFrom():
    return template("insert.html")
    
@post("/insert")
def insertRequest():
    #a = request.forms.get("number")
    b = request.forms.get("chemical")
    c = request.forms.get("weight")
    d = request.forms.get("price")
    e = request.forms.get("mrp")
    try:
        insertNewVal(b,c,d,e)
        return "<script>alert('sucess');</script>", template("insert.html")
    except:
        return "<p>error</p>"








#####INSERT NEW VALUES END HERE####


@route('/all')
def list_all():
    c.execute("SELECT * FROM compounds")
    result = c.fetchall()
    print(result)
    op = template('all.html',rows=result)
    return op







#reinitiateDataBase() 
#insertNewVal("Savnol","500ml",200,225)
#print(get_chem_name("Savnol"))

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)

conn.close()
