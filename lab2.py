import os, sys, fileinput, base64, hashlib
from Crypto.Cipher import AES
from tkinter import *

# Hash Function
def encrypt_string(hash_string):
   sha_signature = \
       hashlib.sha256(hash_string.encode()).hexdigest()
   return sha_signature

# Encryption Function
def encrypt(plaintext):
   global cipher
   data = base64.b16decode(plaintext)
   return cipher.encrypt(data)

# Decryption Function
def decrypt(ciphertext):
    global cipher
    decryption = base64.b16decode(cipher.decrypt(ciphertext))
    return decryption

# Decrypts amount from bank using key from my student ID
def bank_dep(text):
    kwallet = encrypt_string('1941191')
    key = base64.b16decode(kwallet.upper())
    aes = AES.new(key, AES.MODE_ECB)
    encryptor = base64.b16decode(text)
    decryptor = base64.b16encode(aes.decrypt(encryptor))
    decryptor = str(int(decryptor.decode('utf-8')))
    add_balance(decryptor)
    return(decryptor)

# Prints an encrypted token using the bank key
def final_encrypt(text):
    key = base64.b16decode('F25D58A0E3E4436EC646B58B1C194C6B505AB1CB6B9DE66C894599222F07B893')
    aes = AES.new(key, AES.MODE_ECB)
    data = base64.b16decode(text)
    encryptor = aes.encrypt(data)
    encryptorString = base64.b16encode(encryptor)
    print()
    print("Token: "+str(encryptorString)[2:34])

# Decrypts token
def final_decrypt(text):
    key = base64.b16decode('F25D58A0E3E4436EC646B58B1C194C6B505AB1CB6B9DE66C894599222F07B893')
    aes = AES.new(key, AES.MODE_ECB)
    data = base64.b16decode(text)
    decryptor = base64.b16encode(aes.decrypt(data))
    return decryptor.decode('utf-8')

# add zeros to numbers inputed for each input for encrypting token
def add_zeros(text):
    length = ''
    for x in range(8-len(text)):
        length = length + '0'
    text = (length+text)
    return text

# takes in and concatenates your ID, destination ID, amount
# and calls exist function
def encrypt_token(sync):
    # oact = '1941191'
    print('input origin account number')
    oact = input()
    oact = add_zeros(oact)
    print()
    print('input recipient account number')
    ract = input()
    ract = add_zeros(ract)
    print()
    if sync == True:
        if exist(ract) == False :
            final_encrypt(oact+ract+'00000000'+'00000000')
        else:
            print('Accounts already synced')
    else:
        if (exist(ract) == True):
            print('input amount')
            amt = input()
            amt = add_zeros(amt)
            subtract_balance(str(int(amt)))
            final_encrypt(oact + ract + amt + update_counter(ract))
        else:
            print('Accounts not previously synced')

# exists the "database" to see if the account passed in exists
# and either starts the counter or increments it
def exist(text):
    exists = True
    if text not in open('data.txt').read():
        exists = False
        appfile = open('data.txt', 'a+')
        new_act = text+' '+'00000000'
        appfile.write( new_act+'\n' )
        appfile.close()
    return exists

# updates account counter if already synced
def update_counter(text):
    s = open("data.txt").read()
    with fileinput.FileInput('data.txt', inplace=True, backup='.bak') as file:
        for line in file:
            if text in line:
                num = text + ' ' + line[9:17]
                count = str(int(line[9:17])+1)
                count = add_zeros(count)
                s = s.replace(num, text +' ' +count)
                f = open("data.txt", 'w')
                f.write(s)
                f.close()
    return count


def recieve(text):
    plain = final_decrypt(text)
    receiver = plain[0:8]
    sender = plain[8:16]
    amount = int(plain[16:24])
    counter = plain[24:32]
    # if receiver != '01941191'
    #     print('Unathorized account')
    #     return
    with open("data.txt") as f:
        for line in f:
            if sender in line:
                if line[9:17] == counter:
                    print('Accepted')
                    print('amount deposited: '+ str(amount))
                    add_balance(amount)
                    update_counter(sender)
                else :
                    print('Unauthorized')

# adds desired amount to account
def add_balance(amt):
    text = 'Balance:'
    s = open("data.txt").read()
    with fileinput.FileInput('data.txt', inplace=True, backup='.bak') as file:
        for line in file:
            if text in line:
                balance = str(int(line[9:20]) + int(amt))
                num = text + ' ' + line[9:17]
                s = s.replace(line, text +' '+ balance+'\n' )
                f = open("data.txt", 'w')
                f.write(s)
                f.close()

# subtracts desired amount from account
def subtract_balance(amt):
    text = 'Balance:'
    s = open("data.txt").read()
    with fileinput.FileInput('data.txt', inplace=True, backup='.bak') as file:
        for line in file:
            if text in line:
                balance = str(int(line[9:20]) - int(amt))
                num = text + ' ' + line[9:17]
                s = s.replace(line, text +' '+ balance+'\n' )
                f = open("data.txt", 'w')
                f.write(s)
                f.close()

# displays account balance
def balance():
    text = 'Balance:'
    for line in fileinput.input( 'data.txt' ):
        if text in line :
            fileinput.close()
            return line[9:1000]

# clears console window
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

option =''
while option != '5':
    print('Current Balance: '+balance())

    print('Options:')
    print('1) Receiving funds from the bank')
    print('2) Synchronize two wallets')
    print('3) Send Funds')
    print('4) Receiving Funds from account')
    print('5) Exit')
    print()
    option = input("Please enter choice: ")

    if (option == '1'):
        print('input cypher text')
        text = input()
        print()
        try:
            print(bank_dep(text), 'added to account')
            print('Current Balance: '+balance())
        except:
            print('Unauthorized')

    elif (option == '2'):
        cls()
        encrypt_token(True)

    elif (option == '3'):
        encrypt_token(False)
        print()

    elif (option == '4'):
        print('Enter your token')
        token = input()
        cls()
        recieve(token)

    elif (option == '5'):
        cls()
        print('Goodbye')
        print()
    else:
        cls()
        print('Please choose again')
        print()

# message = 'DFF663AFB11C4E8450033D1E90DC8F18' # this one
# message = '9DC4B037A1772850022EBA2C45648F2F' # Tim's
