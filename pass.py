from linecache import getline
from cryptography.fernet import Fernet
from getpass import getpass
from datetime import datetime
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
        
## CHAT ##

def showChat(key):
    file = open("chat.txt", "r")
    while(True):
        msg = file.readline()
        if (msg == ""):
            break
        msg = msg.split()
        fernet = Fernet(key)
        decMessage = fernet.decrypt(msg[0]).decode()
        print("user: " + decMessage + " ")
        decMessage = fernet.decrypt(msg[1]).decode()
        print("at: " + decMessage + " ")
        decMessage = fernet.decrypt(msg[2]).decode()
        print("said: " + decMessage + "\n")

def addChatMessage(key, user):
    file = open("chat.txt", "a")
    print("\nEnter your message: ")
    message = input()
    fernet = Fernet(key)
    decMessage = fernet.encrypt(message.encode())
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    decDate = fernet.encrypt(date.encode())
    decUser = fernet.encrypt(user.userName.encode())
    file.write(decUser.decode() + " " + decDate.decode() + " " + decMessage.decode() + "\n")


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

def userOptions(user, database, key):
    while(True):
        print("\n(1)Would you like a Bible Verse?\n(2) Check if you are admin.\n(3) Admin options.\n(4) Enter chat.\n(5) Exit program.")
        opt = input()
        match opt: 
            case '1':
                print("\n" + getRandomBibleVerse())
            case '2':
                user.adminChk()
            case '3':
                if(user.isAdmin == False):
                    print("\nIntruder, you are not admin.")
                    break
                elif(user.isAdmin == True):
                    print("\nWould you like to:\n(1)Remove user\n(2)Make user admin. \n(3) Deny admin rights to user\n(4) Return to previous menu\n:")
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
                        case '3':
                            print("Type the username you would like to deny admin priviledges:")
                            user_read = input()
                            user_selected = checkIfUserExists(user_read, database)
                            if (user_selected != False):
                                user_selected.removeAdmin()
                            else:
                                print("\nUser does not exist.") 
                        case '4':
                            continue

            case '4':
                print("Would you like to:\n(1) See chat.\n(2) Add message to chat.\n:")
                optchat = input()
                match optchat:
                    case '1':
                        showChat(key)
                    case '2':
                        addChatMessage(key, user)
            case '5':
                break



    
def userLogin(database, key):
    userName = input("Enter your username:")
    while(checkIfUserExists(userName, database) == False):
        userName = input("User does not exist, retype:")
    password = getpass("Enter your password:").encode()
    userlg = checkIfUserExists(userName, database)
    if (bcrypt.checkpw(password, userlg.hpass.encode())):
        print("\nLogin succesful.\n............")
        userOptions(userlg, database, key)
        return userlg
    else:
        print("\nLogin failed.")
        return False

def saveDatabase(database):
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
fkey = open("key.txt", "r")
key = fkey.readline().encode('utf-8')
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
    option = input("Would you like to:\n(1)Create new user\n(2)Login\n(3)Save and leave\n:")
    match option:
        case "1":
            createNewUser(userName, password, hashed, database)
            saveDatabase(database)
        case "2":
            userLogin(database, key)
            saveDatabase(database)
        case "3":
            saveDatabase(database)
            break

