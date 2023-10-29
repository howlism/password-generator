import os
import random
import string
import pyperclip
from cryptography.fernet import Fernet

# TODO: add GUI (@ some point :>)

accountName = ""


def createAccountList():
    with open('accounts.txt', 'a') as file:
        file.writelines("\n")


def listWebsites(name):
    with open("passwords_" + name + ".txt", "r") as file:
        lines = file.readlines()
        found = False
        for line in lines:
            strip = line.strip()
            split = strip.split("|")
            if len(split) != 3:
                continue
            website = split[0]
            decWebsite = fernet.decrypt(website.encode()).decode()
            print(decWebsite)


def clearFiles():
    dirList = os.listdir()
    for i in dirList:
        if i.endswith(".txt"):
            os.remove(i)
            print(i + " deleted")
            quit()


def newkey():
    with open("secret.key", 'ab') as file:
        file.write(key)


def loadkey():
    with open("secret.key", 'rb') as file:
        keyfromfile = file.read()
    return keyfromfile


def createNewAccount():
    newUserName = input("What is your name? ").strip()
    found = False
    with open("accounts.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            strip = line.strip()
            split = strip.split('|')
            if split[0] == newUserName:
                print("Sorry this account already exists, try logging in.")
                loginToAccount()
        newPassword = input("What do you want your password to be? ").strip()
        with open("accounts.txt", 'a') as file:
            file.writelines(newUserName + "|" + fernet.encrypt(newPassword.encode()).decode() + "\n")
        mode(newUserName)


def loginToAccount():
    accountName = input("Enter your name: ").strip()
    found = False
    with open("accounts.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            strip = line.strip()
            split = strip.split('|')
            if accountName == split[0]:
                counter = 0
                while counter < 3:
                    password = input("Please enter your password: ").strip()
                    decPassword = fernet.decrypt(split[1].encode()).decode()
                    if password == decPassword:
                        file.close()
                        fileName = accountName
                        mode(fileName)
                    else:
                        if counter < 3:
                            print("Incorrect password. You have " + str(2 - counter) + " attempts remaining.")
                            counter += 1
                            continue
                        elif counter == 3:
                            print("Login failed. Please try again.")


def generator(length):
    generatedPassword = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(0, length):
        generatedPassword = generatedPassword + ''.join(random.choice(characters))
    return generatedPassword


def write(name):
    website = input("Please input the website associated with these credentials: ").strip()
    username = input("Please input the username associated with these credentials: ").strip()
    password = input("Please input the password associated with these credentials: ").strip()
    websiteE = fernet.encrypt(website.encode()).decode()
    usernameE = fernet.encrypt(username.encode()).decode()
    passwordE = fernet.encrypt(password.encode()).decode()
    credentials = [websiteE + "|" + usernameE + "|" + passwordE + "\n"]
    with open("passwords_" + name + ".txt", 'a') as file:
        file.writelines(credentials)


def writeGeneratedPassword(password, name):
    website = input("Please input the website associated with this password: ").strip()
    username = input("Please input the username associated with this password: ").strip()
    websiteE = fernet.encrypt(website.encode()).decode()
    usernameE = fernet.encrypt(username.encode()).decode()
    passwordE = fernet.encrypt(password.encode()).decode()
    credentials = [websiteE + "|" + usernameE + "|" + passwordE + "\n"]
    with open("passwords_" + name + ".txt", 'a') as file:
        file.writelines(credentials)


def read(name):
    websiteInput = input(
        "Please enter the website associated with this account: "
    ).casefold().strip()
    with open("passwords_" + name + ".txt", "r") as file:
        lines = file.readlines()
        found = False
        for line in lines:
            strip = line.strip()
            split = strip.split("|")
            if len(split) != 3:
                continue
            website = split[0]
            username = split[1]
            password = split[2]
            decWebsite = fernet.decrypt(website.encode()).decode()
            decUsername = fernet.decrypt(username.encode()).decode()
            decPassword = fernet.decrypt(password.encode()).decode()
            if websiteInput == decWebsite:
                found = True
                print("Website: " + decWebsite)
                print("Username: " + decUsername)
                print("Password: " + decPassword)
        if not found:
            print("Website not found.")


def mode(name):
    while True:
        mode = input(
            "Do you want to (read) or (write) account credentials or (generate) a password or (quit)? ").lower().strip()
        if mode == 'read':
            read(name)
        elif mode == 'write':
            write(name)
        elif mode == 'quit' or mode == 'exit' or mode == 'stop':
            print("Exiting...")
            quit()
        elif mode == 'clear files':
            clearFiles()
            continue
        elif mode == 'list websites':
            listWebsites(name)
            continue
        elif mode == 'generate' or mode == 'generator':
            while True:
                pwordLength = int(input("What would you like the length of your password to be? (8-16) ").strip())
                if pwordLength < 8 or pwordLength > 16:
                    print("Invalid choice. Please try again.")
                    continue
                else:
                    break
            newGeneratedPassword = generator(pwordLength)
            print("Your new password is " + newGeneratedPassword + ".")
            copyornocopy = input("Would you like to copy this to your clipboard? (Y/N) ").lower().strip()
            if copyornocopy == 'yes' or copyornocopy == 'y':
                pyperclip.copy(newGeneratedPassword)
                print("Successfully copied to clipboard!")
                y = input("Would you also like to add this password to the manager? (Y/N) ").lower().strip()
                if y == 'yes' or y == 'y':
                    writeGeneratedPassword(newGeneratedPassword, name)
                elif y == 'no' or y == 'n':
                    continue
                else:
                    print("Invalid choice")
                    quit()
            elif copyornocopy == 'no' or copyornocopy == 'n':
                x = input("Would you like to add this password to the password manager? (Y/N) ").lower().strip()
                if x == 'yes' or x == 'y':
                    writeGeneratedPassword(newGeneratedPassword, name)
                elif x == 'no' or x == 'n':
                    continue
                else:
                    print("Invalid choice")
                    quit()
        else:
            print("Invalid mode. Please try again.")
            continue


while True:
    if not os.path.exists("secret.key"):
        print("Key not found, generating one for you.")
        key = Fernet.generate_key()
        fernet = Fernet(key)
        newkey()
    else:
        key = loadkey()
        fernet = Fernet(key)

        if os.path.exists("accounts.txt"):
            accountMode = input("Do you want to (log in), or (create) a new account? ").lower().strip()
            if accountMode == 'create':
                createNewAccount()
            elif accountMode == 'login' or accountMode == 'log in':
                loginToAccount()
        else:
            print("You do not have any user accounts created.")
            createAccountList()
            createNewAccount()
