import mysql.connector
conn=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Passw0rd12#",
    db="major_project"
)   
#creating connection
cursor= conn.cursor()

def existingAcc(name,pwd):
    try:
        cursor.execute("select * from register where username='"+name+"' and pwd='"+pwd+"' ") #inserting values in our table and passing a value i.e. data
        return cursor.fetchall()
    except Exception as e:  
        print(e)
        return []

def insertregister(data):
    try:
        cursor.execute("insert into register(username,email,phone,gender,pwd) values(%s,%s,%s,%s,%s)",data) #inserting values in our table and passing a value i.e. data
        conn.commit()
        return True
    except Exception as e:  #if there is any error it will print the error nd returns false
        print(e)
        return False
    
def insertlogin(data):
    try:
        cursor.execute("insert into login(username,pwd) values(%s,%s)",data) #inserting values in our table and passing a value i.e. data
        conn.commit()
        return True
    except Exception as e:  #if there is any error it will print the error nd returns false
        print(e)
        return False
