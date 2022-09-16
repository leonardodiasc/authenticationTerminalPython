from linecache import getline
from getpass import getpass
import bcrypt
import requests


class User:
    def __init__(self, userName, hpass, isAdmin):
        self.userName = userName
        self.hpass = hpass
        self.isAdmin = isAdmin

    def makeAdmin(self):
        self.isAdmin = True

    def removeAdmin(self):
        self.isAdmin = False

    def amIAdmin (self):
        if (self.isAdmin == False):
            return "false"
        elif(self.isAdmin == True):
            return "true"

    def adminChk(self):
        if (self.isAdmin == False):
            print("\nYou are not Admin.")
        elif(self.isAdmin == True):
            print("\n You are Admin.")
        

def checkIfUserExists(userName, database):
    n = 0
    for user in database:
        if(userName == user.userName):
            n = n + 1
        if(n == 1):
            return user
    if (n == 0):
        return False

def getRandomBibleVerse():
    response = requests.get("https://labs.bible.org/api/?passage=random")
    data = response.text
    return data


def createNewUser(userName, password, hashed, database):
    userName = input("Enter username:")

    while (checkIfUserExists(userName, database) != False):
        userName = input("Username already taken, enter another:")

    password = getpass("Enter password: ").encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    database.append(User(userName, hashed.decode(), False))
    print("User succesfully created.")
    return hashed

def userOptions(user, database):
    print("\nLogin succesful.\n............")
    while(True):
        print("\n(1)Would you like a Bible Verse?\n(2) Check if you are admin.\n(3) Admin options.\n(4) Exit program.")
        opt = input()
        match opt: 
            case '1':
                print("\n" + getRandomBibleVerse())
                print("\n(1)Would you like another Bible Verse?\n(2) Check if you are admin.\n(3) Admin options.\n(4) Exit program.")
            case '2':
                user.adminChk()
                print("\n(1)Would you like a Bible Verse?\n(2) Check if you are admin.\n(3) Admin options.\n(4) Exit program.")
            case '3':
                if(user.isAdmin == False):
                    print("\nIntruder, you are not admin.")
                    break
                elif(user.isAdmin == True):
                    print("\nWould you like to:\n(1)Remove user\n(2)Make user admin.")
                    aopt = input()
                    match aopt:
                        case '1':
                            print("\nType the username you would like to remove:")
                            user_read = input()
                            user_selected = checkIfUserExists(user_read, database)
                            if (user_selected != False):
                                database.remove(user_selected)
                            else:
                                print("\nUser does not exist.")

                        case '2':
                            print("Type the username you would like to make admin.")
                            user_read = input()
                            user_selected = checkIfUserExists(user_read, database)
                            if (user_selected != False):
                                user_selected.makeAdmin()
                            else:
                                print("\nUser does not exist.") 
            case '4':
                break                  


    
def userLogin(database):
    userName = input("Enter your username:")
    while(checkIfUserExists(userName, database) == False):
        userName = input("User does not exist, retype:")
    password = getpass("Enter your password:").encode()
    userlg = checkIfUserExists(userName, database)
    if (bcrypt.checkpw(password, userlg.hpass.encode())):
        userOptions(userlg, database)
        return userlg
    else:
        print("\nLogin failed.")
        return False

def saveDatabase(file, database):
    file = open("passwords.txt", "w")
    for user in database:
            file.write("user: " + user.userName + " " + user.amIAdmin() + "\npassword: " + user.hpass + "\n")
    





database = []
password = ""
nome = ""
hp = ""
userName = ""
hashed = b''
textFile = open("passwords.txt", "a+")
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
        if (nome[2] == "true"):
            database.append(User(nome[1],hp[1], True))

        elif(nome[2] == "false"):
            database.append(User(nome[1],hp[1], False))
        

while (True):
    option = input("Would you like to:\n(1) Create new user\n(2)Login\n(3) Save and leave\n:")
    match option:
        case "1":
            createNewUser(userName, password, hashed, database)
            saveDatabase(textFile, database)
        case "2":
            userLogin(database)
            saveDatabase(textFile, database)
        case "3":
            saveDatabase(textFile, database)
            break

