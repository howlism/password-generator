import linecache
import base64
from cryptography.fernet import Fernet

# TODO: password generator

with open('secret.key', 'rb') as file:
    key = file.read()
fernet = Fernet(key)
print("Welcome to the password manager.")
masterkey = linecache.getline("password_manager.txt", 1).strip()
if masterkey != "":
    keyInput = input("Please enter master password: ").strip()
    if keyInput == masterkey:
        while True:
            mode = input("Would you like to write or read credentials? ").lower().strip()
            if mode == 'write':
                website = input("Type the website associated with the credentials: ").strip()
                username = input("Type the username: ").strip()
                password = input("Type the password: ").strip()

                encWebsite = base64.urlsafe_b64encode(fernet.encrypt(website.encode('utf-8'))).decode('utf-8')
                encUsername = base64.urlsafe_b64encode(fernet.encrypt(username.encode('utf-8'))).decode('utf-8')
                encPassword = base64.urlsafe_b64encode(fernet.encrypt(password.encode('utf-8'))).decode('utf-8')
                credentials = [encWebsite, ",", encUsername, ",", encPassword, "\n"]

                with open("password_manager.txt", 'a') as file:
                    file.writelines(credentials)
            elif mode == 'read':
                counter = 0
                websiteInput = input("Which website would you like to read the password for?: ").lower()

                with open("password_manager.txt", 'r') as file:
                    lines = file.readlines()
                    found = False
                    for line in lines:
                        strip = line.strip()
                        split = strip.split(',')
                        if len(split) != 3:
                            continue
                        website = split[0]
                        username = split[1]
                        password = split[2]
                        decWebsite = fernet.decrypt(base64.urlsafe_b64decode(website)).decode('utf-8')
                        decUsername = fernet.decrypt(base64.urlsafe_b64decode(username)).decode('utf-8')
                        decPassword = fernet.decrypt(base64.urlsafe_b64decode(password)).decode('utf-8')
                        if websiteInput == decWebsite:
                            found = True
                            print("Website: " + decWebsite)
                            print("Username: " + decUsername)
                            print("Password: " + decPassword)
                    if not found:
                        print("Website not found.")
            elif mode == 'quit' or mode == 'exit' or mode == 'stop':
                print("Exiting.")
                break
            else:
                print("Please try again")
    else:
        print("Wrong Password.")
else:
    newMasterkey = input("Please enter your new master password: ")
    with open("password_manager.txt", 'r') as file:
        wholeFile = file.readlines()
        wholeFile[0] = newMasterkey + "\n"
        # file.writelines(wholeFile)
    with open("password_manager.txt", 'w') as file:
        file.writelines(wholeFile)
