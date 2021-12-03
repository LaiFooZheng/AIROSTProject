import db
import faceRecognitionProject as fr
import otp
import random

current_user = 0
current_id = 0


# functions


def uid_generator():
    global current_user, current_id
    uid = random.randint(1000, 10000)
    for eid in range(len(db.acc)):
        if uid == db.acc[eid].value:
            current_id = eid
            current_user = uid
    print("Account ID Generated: ", uid)
    return uid


# replaced with uid generator function
def exist(uid):
    # Check if the user id exist in database
    global current_user, current_id
    for eid in range(len(db.acc)):
        if uid == db.acc[eid].value:
            current_id = eid
            current_user = uid
            return True
    return False


def match(upw):
    # Check if the user id match its password in database
    if upw == db.pwd[current_id].value:
        return True
    else:
        return False


def withdraw(i):
    # withdraw money
    db.backup()
    db.balance[current_id].value = db.balance[current_id].value - i
    db.save_2()
    print("RM", i, "have been withdrawn")


def deposit(i):
    # deposit
    db.backup()
    db.balance[current_id].value = db.balance[current_id].value + i
    db.save_2()
    print("RM", i, "have been deposited")


def user_action():
    print("")
    print("Welcome, ", db.nam[current_id].value)
    print("Choose an action:")
    print("1 - Check Balance")
    print("2 - Withdraw")
    print("3 - Deposit")
    print("4 - Exit")
    ac = int(input(""))
    if ac == 1:
        print("Your current balance is ", db.balance[current_id].value)
        user_action()
    elif ac == 2:
        amount = int(input("Input the amount to be withdrawn: RM"))
        user_code = input("Enter OTP: ")
        if otp.otp_check(db.secret_key[current_id].value, user_code):
            withdraw(amount)
            user_action()
        else:
            print("OTP is wrong. Please try again.")
            user_action()
    elif ac == 3:
        amount = int(input("Input the amount to be deposited: RM"))
        user_code = input("Enter OTP: ")
        if otp.otp_check(db.secret_key[current_id].value, user_code):
            deposit(amount)
            user_action()
        else:
            print("OTP is wrong. Please try again.")
            user_action()
    elif ac == 4:
        print("Thanks for using XXX services.")
    else:
        print("Invalid action, please try again.")
        user_action()


# main ATM
def login():
    print("")
    u_id = int(input("Enter your acc number: "))
    if exist(u_id):
        print("Choose a login option: ")
        print("1 - Login with password")
        print("2 - Login with FaceID")
        print("3 - Cancel")
        u_c = int(input())
        if u_c == 1:
            u_p = int(input("Enter your acc pin: "))
            if match(u_p):
                user_code = input("Enter OTP: ")
                if otp.otp_check(db.secret_key[current_id].value, user_code):
                    print("Access Granted")
                    user_action()
                else:
                    print("OTP is wrong. Please try again")
                    login()
            else:
                print("Sorry, you account id or password are wrong.")
                main()
        elif u_c == 2: # face recog
            print("Press Q to cancel verification.")
            if fr.verifi(current_id):
                user_action()
            else:
                print("Verification failed, please try again.")
                main()
        elif u_c == 3:
            main()
        else:
            print("Invalid action, please try again")
            main()
    else:
        print("Sorry, you account id or password are wrong.")
        main()


def register():
    print("")
    u_i1 = uid_generator()
    u_p1 = int(input("Please enter password: "))
    u_n1 = input("Please input account name: ")
    u_e1 = input("Please enter your email address: ")
    u_h1 = input("Please enter your hand phone number: ")
    print("Press Q when your face is boxed to capture your face id.")
    u_face = fr.registerEncodings()
    db.registration(u_i1, u_n1, u_p1, u_e1, u_h1, u_face)
    print("Register success!")
    main()


def main():
    print("")
    print("Welcome to XXX.")
    print("Please choose an option:")
    print("1 - Login")
    print("2 - Register")
    u_c = int(input())
    if u_c == 1:
        login()
    elif u_c == 2:
        register()
    else:
        print("Invalid action, please try again")
        main()


try:
    main()
except:
    print('Something went wrong, proceed to exit.')
