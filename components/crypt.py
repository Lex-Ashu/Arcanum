from pathlib import Path
import gnupg, random, string

#IMPORTANT ADD A RANDOM DEFINED LENGTH TEXT AT THE END OF THE ENCRYPTION DATA AND REMOVE IT AT DECRYPTION!
#SORTS OUT THE PROBLEM, THAT SAME DATA STUFF IS NOT THE SAME IN TH DB!
#Decide if the password for encryption should be hashed and if the hash should be used for encryption.

class Encryption:
    password = ""
    def __init__(self):
        global gpg
        gpg = gnupg.GPG(gnupghome = str(Path.home()))
        gpg.encoding = 'utf-8'
    
    def generateKey(self, typeOfKey="RSA", length=8192):
        print("generating keys")
        inputData = gpg.gen_key_input(key_type=typeOfKey, key_length=length, name_real="ArcanumKey")
        key = gpg.gen_key(inputData)
        return key

    def encrypt(self, theData, recipients=None):
        encrypted = str(gpg.encrypt(data=theData, recipients=recipients, passphrase=Encryption.password, symmetric=True))
        return encrypted
    
    def decrypt(self, theData):
        decrypted = gpg.decrypt(message=theData, passphrase=Encryption.password)
        return str(decrypted), decrypted.ok, decrypted.status

    def encryptFile(self, theData, recipients=None):
        encrypted = str(gpg.encrypt_file(data=theData, recipients=recipients, passphrase=Encryption.password, symmetric=True))
        return encrypted
    
    def decryptFile(self, theData):
        decrypted = str(gpg.decrypt_file(message=theData, passphrase=Encryption.password))
        return decrypted

    def genPassword(self, letters=False, digits=False, symbols=False, safeSymbols=False,length=16, ):
        if length > 0:
            if letters or digits or symbols or safeSymbols:
                print("Cannot create password due to invalid conditions!")
            else:
                charlist = None
                if letters: charlist = charlist + string.ascii_letters
                if digits: charlist = charlist + string.digits
                if symbols: charlist = charlist + string.punctuation
                if safeSymbols: charlist = charlist + "!#$%*+-=?@^_|äöüèéà"
                return ''.join(random.choice(charlist) for i in range(length))