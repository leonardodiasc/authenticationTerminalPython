from linecache import getline
from getpass import getpass
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
        return user
    else:
        return False

def createNewUser(userName, password, hashed, database, textFile):
    userName = input("Enter username:")

    while (checkIfUserExists(userName, database) != False):
        userName = input("Username already taken, enter another:")

    password = getpass("Enter password: ").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    textFile.write("\nuser: " + userName + "\n" + "password: " + hashed.decode())
    database.append(User(userName, hashed.decode()))
    print("User succesfully created.")
    return hashed
    
def userLogin(database):
    userName = input("Enter your username:")
    while(checkIfUserExists(userName, database) == False):
        userName = input("User does not exist, retype:")
    password = getpass("Enter your password:").encode()
    userlg = checkIfUserExists(userName, database)
    if (bcrypt.checkpw(password, userlg.hpass.encode())):
        print("\nLogin succesful.")
        return userlg
    else:
        print("\nLogin failed.")
        return False

    


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

while (True):
    option = input("Would you like to:\n1-Create new user\n2-Login\n:")
    match option:
        case "1":
            createNewUser(userName, password, hashed, database, textFile)
        case "2":
            userLogin(database)

