import os
import random
import string
import pyperclip
from cryptography.fernet import Fernet

# TODO: make user accounts read different files (classes)
# TODO: add GUI (@ some point :>)

accountName = ""


def createFiles():
    with open('accounts.txt', 'a') as file:
        file.close()
    with open('passwords.txt', 'a') as file:
        file.close()


def newkey():
    with open("secret.key", 'ab') as file:
        file.write(key)


def loadkey():
    with open("secret.key", 'rb') as file:
        keyfromfile = file.read()
    return keyfromfile


def createNewAccount():
    newUserName = input("What is your name? ")
    found = False
    with open("accounts.txt", 'r') as file:
        lines = file.readlines()
        if lines:
            for line in lines:
                strip = line.strip()
                split = strip.split('|')
                if split[0] == newUserName:
                    print("Sorry this account already exists, try logging in.")
                else:
                    newPassword = input("What do you want your password to be? ")
                    with open("accounts.txt", 'a') as file:
                        file.writelines(newUserName + "|" + fernet.encrypt(newPassword.encode()).decode() + "\n")
        else:
            newPassword = input("What do you want your password to be? ")
            with open("accounts.txt", 'a') as file:
                file.writelines(newUserName + "|" + fernet.encrypt(newPassword.encode()).decode() + "\n")


def loginToAccount():
    accountName = input("Enter your name: ")
    found = False
    with open("accounts.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            strip = line.strip()
            split = strip.split('|')
            if accountName == split[0]:
                print("Username found")
                password = input("Please enter your password: ")
                decPassword = fernet.decrypt(split[1].encode()).decode()
                if password == decPassword:
                    mode()
                else:
                    print("Incorrect password.")
                    quit()


def generator(length):
    generatedPassword = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(0, length):
        generatedPassword = generatedPassword + ''.join(random.choice(characters))
    return generatedPassword


def write():
    website = input("Please input the website associated with these credentials: ")
    username = input("Please input the username associated with these credentials: ")
    password = input("Please input the password associated with these credentials: ")
    websiteE = fernet.encrypt(website.encode()).decode()
    usernameE = fernet.encrypt(username.encode()).decode()
    passwordE = fernet.encrypt(password.encode()).decode()
    credentials = [websiteE + "|" + usernameE + "|" + passwordE + "\n"]
    with open("passwords.txt", 'a') as file:
        file.writelines(credentials)


def writeGeneratedPassword(password):
    website = input("Please input the website associated with this password: ")
    username = input("Please input the username associated with this password: ")
    websiteE = fernet.encrypt(website.encode()).decode()
    usernameE = fernet.encrypt(username.encode()).decode()
    passwordE = fernet.encrypt(password.encode()).decode()
    credentials = [websiteE + "|" + usernameE + "|" + passwordE + "\n"]
    with open("passwords.txt", 'a') as file:
        file.writelines(credentials)


def read():
    websiteInput = input(
        "Please enter the website associated with this account: "
    ).casefold()
    with open("passwords.txt", "r") as file:
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


def mode():
    while True:
        mode = input("Do you want to read or write account credentials or generate a password or quit? ").lower()
        if mode == 'read':
            read()
        elif mode == 'write':
            write()
        elif mode == 'quit' or mode == 'exit' or mode == 'stop':
            print("Exiting...")
            quit()
        elif mode == 'generate' or mode == 'generator':
            pwordLength = int(input("What would you like the length of your password to be? (8-16) "))
            while True:
                if pwordLength < 8 or pwordLength > 16:
                    print("Invalid choice. Please try again.")
                    continue
                else:
                    break
            newGeneratedPassword = generator(pwordLength)
            print("Your new password is " + newGeneratedPassword + ".")
            copyornocopy = input("Would you like to copy this to your clipboard? ").lower()
            if copyornocopy == 'yes' or copyornocopy == 'y':
                pyperclip.copy(newGeneratedPassword)
                print("Successfully copied to clipboard!")
                y = input("Would you also like to add this password to the manager? ").lower()
                if y == 'yes' or y == 'y':
                    writeGeneratedPassword(newGeneratedPassword)
                elif y == 'no' or y == 'n':
                    continue
                else:
                    print("Invalid choice")
                    quit()
            elif copyornocopy == 'no' or copyornocopy == 'n':
                x = input("Would you like to add this password to the password manager? ").lower()
                if x == 'yes' or x == 'y':
                    writeGeneratedPassword(newGeneratedPassword)
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
            accountMode = input("Do you want to log in, or create a new account? ").lower()
            if accountMode == 'create':
                createNewAccount()
            elif accountMode == 'login' or accountMode == 'log in':
                loginToAccount()
        else:
            print("You do not have any user accounts created.")
            createFiles()
            createNewAccount()
