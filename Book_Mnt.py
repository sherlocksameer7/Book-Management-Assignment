from flask import Flask, request, render_template
import sqlite3

from werkzeug.utils import redirect

Connection = sqlite3.connect("Books_Manage.db", check_same_thread=False)

listoftables1 = Connection.execute("Select * from sqlite_master Where type = 'table' and name = 'MyBook'").fetchall()
listoftables2 = Connection.execute("Select * from sqlite_master Where type = 'table' and name = 'MyUser'").fetchall()

if listoftables1 != []:
    print("Table Already Exists !")
else:
    Connection.execute('''Create Table MyBook(
                       Id Integer Primary Key Autoincrement,
                       Name text,
                       Author text,
                       Category text,
                       Price integer,
                       Publisher text
                       );''')
    print("Table Created Sucessfully ")


if listoftables2 != []:
    print("Table Already Exists !")
else:
    Connection.execute('''Create Table MyUser(
                       Id Integer Primary Key Autoincrement,
                       Name Text,
                       Address Text,
                       Email Text,
                       Phone Integer,
                       Pass Text
                       );''')
    print("Table Created Sucessfully ")


Books = Flask(__name__)


@Books.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        getUsername = request.form["uname"]
        getPassword = request.form["pass"]
        print(getUsername)
        print(getPassword)
        if getUsername == "admin" and getPassword == "9875":
            return redirect('/admindashboard')
        else:
            return redirect('/userlogin')
    return render_template("adminLogin.html")


@Books.route('/admindashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if request.method == 'POST':
        getBookName = request.form["bname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]
        print(getBookName)
        print(getAuthor)
        print(getCategory)
        print(getPrice)
        print(getPublisher)

        try:
            Connection.execute("Insert Into MyBook(Name,Author,Category,Price,Publisher) \
            Values('" + getBookName + "','" + getAuthor + "','" + getCategory + "'," + getPrice + ",'" + getPublisher + "')")
            Connection.commit()
            print("Inserted sucessfully")
            return redirect('/viewall')
        except Exception as error:
            print(error)
    return render_template("adminDash.html")

# @Books.route('/addBooks', methods=['GET', 'POST'])
# def Add_books():

@Books.route('/viewall')
def viewAll():
    cursor = Connection.cursor()
    cursor.execute("Select * from MyBook")
    result = cursor.fetchall()
    return render_template("viewAll.html", book=result)


@Books.route('/search', methods=['GET', 'POST'])
def search():
    cursor = Connection.cursor()
    if request.method == 'POST':
        getBookname = request.form["bname"]
        cursor.execute("Select * from MyBook Where Name= '"+getBookname+"'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exists ")
        else:
            return render_template("search.html", search=result, status=True)
    else:
        return render_template("search.html", search=[], status=False)


@Books.route('/up', methods=['GET', 'POST'])
def update_search():
    global getBookname
    cursor = Connection.cursor()
    if request.method == "POST":
        getBookname = request.form["bname"]
        count = cursor.execute("Select * from MyBook Where Name='"+getBookname+"'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exist")
        else:

            return render_template("update_search.html", search=result, status=True)
    else:

        return render_template("update_search.html", search=[], status=False)

    #     return redirect('/update')
    #
    # return render_template("update_search.html")


@Books.route('/update', methods=['GET', 'POST'])
def updation():
    if request.method == "POST":
        getBookName = request.form["bname"]
        getAuthor = request.form["author"]
        getCategory = request.form["category"]
        getPrice = request.form["price"]
        getPublisher = request.form["publisher"]

        Connection.execute("Update MyBook Set Name='"+getBookName+"', Author='"+getAuthor+"', Category='"+getCategory+"', Price="+getPrice+", Publisher='"+getPublisher+"'")
        Connection.commit()
        print("Updated Successfully.!")

        return redirect('/viewall')

    return render_template("updation.html")


@Books.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == "POST":
        getBookname = request.form["bname"]
        Connection.execute("Delete from MyBook Where Name='" + getBookname + "'")
        Connection.commit()
        print("Deleted Successfully")
        return redirect('/viewall')
    return render_template("delete.html")


@Books.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        getName = request.form["name"]
        getAddress = request.form["add"]
        getEmail = request.form["email"]
        getPhone = request.form["phone"]
        getPassword = request.form["pass"]
        print(getName)
        print(getAddress)
        print(getEmail)
        print(getPhone)
        print(getPassword)

        try:
            Connection.execute("Insert Into MyUser(Name, Address, Email, Phone, Pass) \
            Values('" + getName + "','" + getAddress + "','" + getEmail + "'," + getPhone + ",'" + getPassword + "')")
            Connection.commit()
            print("Inserted Sucessfully.!")
            return redirect('/userlogin')

        except Exception as error:
            print(error)
    return render_template("register.html")


@Books.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        getEmail = request.form["email"]
        getpass = request.form["pass"]
        print(getEmail)
        print(getpass)
        return redirect('/userview')
    return render_template("userLogin.html")


@Books.route('/userview')
def user_view():
    cursor = Connection.cursor()
    cursor.execute("Select * from MyBook")
    result = cursor.fetchall()
    return render_template("userView.html", book=result)


@Books.route('/usersearch', methods=['GET', 'POST'])
def user_search():
    cursor = Connection.cursor()
    if request.method == 'POST':
        getBookname = request.form["bname"]
        cursor.execute("Select * from MyBook Where Name= '" + getBookname + "'")
        result = cursor.fetchall()
        if result is None:
            print("Book Name Not Exists")
        else:
            return render_template("usersearch.html", search=result, status=True)
    else:
        return render_template("userSearch.html", search=[], status=False)


if __name__ == "__main__":
    Books.run()