from linecache import getline
import bcrypt

class User:
    def __init__(self, userName, hpass):
        self.userName = userName
        self.hpass = hpass

database = []
password = input("Enter pass:").encode()
nome = ""
hp = ""
userName = input("Enter username:").encode()
 # Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# Check that an unhashed password matches one that has previously been
 # hashed
database.append(User(userName, hashed))

# Opens passwords and users and stores data into the variable 'database' an array of objects
with open("passwords.txt", "r") as fileDb:
    while(True):
        nome = fileDb.readline()
        if (nome == ""):
            break
        nome = nome.split()
        hp = fileDb.readline()
        hp = hp.split()
        database.append(User(nome,hp))

        
textFile = open("passwords.txt", "a")
hashedWrite = hashed.decode()

textFile.write("user: " + userName.encode() + "\n" + "password: " + hashedWrite.encode())
passtest = input("Enter your password again:").encode()
print (database[0].userName.encode() + " " + database[0].hpass.encode())

if bcrypt.checkpw(passtest, hashed):
     print("It Matches!")
else:
     print("It Does not Match :(")