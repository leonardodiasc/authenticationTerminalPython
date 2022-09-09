from linecache import getline
import bcrypt

class User:
    def __init__(self, userName, hpass):
        self.userName = userName
        self.hpass = hpass

def checkIfUserExists(userName, database):
    n = 0
    for user in database:
        if(userName == user.userName):
            n = n + 1
    if(n == 1):
        return True
    else:
        return False

def createNewUser(userName, password, hashed, database, textFile):
    userName = input("Enter username:")

    while (checkIfUserExists(userName, database) == True):
        userName = input("Username already taken, enter another:")

    password = input("Enter password: ").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    textFile.write("\nuser: " + userName + "\n" + "password: " + hashed.decode())
    database.append(User(userName, hashed.decode()))
    return hashed
    

database = []
password = ""
nome = ""
hp = ""
userName = ""
hashed = b''
textFile = open("passwords.txt", "a")
 # Hash a password for the first time, with a randomly-generated salt
# Check that an unhashed password matches one that has previously been
 # hashed

# Opens passwords and users and stores data into the variable 'database' an array of objects
#Initiates and loads the data
with open("passwords.txt", "r") as fileDb:
    while(True):
        nome = fileDb.readline()
        if (nome == ""):
            break
        nome = nome.split()
        hp = fileDb.readline()
        hp = hp.split()
        database.append(User(nome[1],hp[1]))


hashed = createNewUser(userName, password, hashed, database, textFile)
passtest = input("Enter your password again:").encode('utf-8')

if bcrypt.checkpw(passtest, hashed):
     print("It Matches!")
else:
     print("It Does not Match :(")