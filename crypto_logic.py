import RSA
import hashlib  # Provides access to cryptographic hash functions like SHA-256
import os       # Used to generate secure random bytes (e.g., for the salt)


# SNIPPET1
def int_to_bytes_BE(intv):
    b = []
    while intv != 0:
        b.append(intv % 256)
        intv = intv // 256
    return b[::-1]


# SNIPPET2
def int_to_string(msg):
    lisible = ""
    for c in msg:
        try:
            lisible += bytes(int_to_bytes_BE(c)).decode("utf-8")
        except Exception as e:
            lisible += "*"
    return lisible


def encodeMessage(message):
    res = b''
    for c in message:
        cByte = c.encode('utf-8')
        byteLen = 4 - len(cByte)
        for i in range(byteLen):
            cByte = b'\x00' + cByte
        res += cByte
    return res


# Encode direction:
# 0 = encode
# 1 = decode
def decodeMessage(message):
    # msg = message[6:].decode('utf-8')
    msg = int_to_string(message[6:])
    res = msg.replace('\x00', '')
    return "Header: " + message[:4].decode('utf-8') + " - Message length: " + str(
        int.from_bytes(message[4:6], "big")) + " - Message: " + res


def decodeResponse(message):
    res = []
    msg = message.decode('utf-8')
    res.append(msg[6:].replace('\x00', ''))
    res.append(msg[3:4])
    return res

"""def decodeResponse(message):
    msg = message[6:].decode('utf-8')
    res = msg.replace('\x00', '')
    return res
"""

# cipherType:
# 0 = no cipher
# 1 = shift
# 2 = vigénère
# 3 = RSA
def cipherTypeString(cipher_type):
    match cipher_type:
        case 1:
            return "shift"
        case 2:
            return "vigenere"
        case 3:
            return "RSA"
        case 4:
            return "Hash"
        case 5:
            return "Hash - verify"
        case 0 | _:
            return "none"


def sendQuery(query_type, cipher_type, direction, text_len, msg = ""):
    header = "ISC" + query_type
    if query_type == "s":
        if cipher_type == 4:
            command = "task hash hash"
        elif cipher_type == 5:
            command = "task hash verify"
        else:
            command = "task " + cipherTypeString(cipher_type) + " " + direction + " " + str(text_len)
        message = header.encode('utf-8') + len(command).to_bytes(2, byteorder='big') + encrypt(command, 0)
        print(f"Query :    {decodeMessage(message)}")
    elif query_type == "t":
        message = header.encode('utf-8') + len(msg).to_bytes(2, byteorder='big') + encrypt(msg, 0)
    return message


def sendReply(query_type, cipher_type, key, msg):
    header = "ISC" + query_type
    payload = encrypt(msg, cipher_type, key)
    print(msg)
    print(len(msg))
    if cipher_type == 4:
        msg_length = len(payload)
    else:
        msg_length = len(msg)
    message = header.encode('utf-8') + msg_length.to_bytes(2, byteorder='big') + payload
    print(f"Sending :  {decodeMessage(message)}")
    return message


def encrypt(command, cipher_type=0, key=0):
    match cipher_type:
        case 1:
            return shiftEncrypt(command, key)
        case 2:
            return vigenereEncrypt(command, key)
        case 3:
            return RSAEncrypt(command, key)
        case 4:
            return hashEncrypt(command)
        case 0 | _:
            return encodeMessage(command)


def shiftEncrypt(msg, key):
    encrypted = bytearray()
    for c in msg:
        encrypted.extend(int.to_bytes(int.from_bytes(c.encode('utf-8')) + int(key), 4))
    return encrypted


def vigenereEncrypt(msg, key):
    encrypted = bytearray()  # De type tableau de byte (bytearray), le type qui doit être envoyé au serveur
    j = 0
    for i in range(0, len(msg)):
        mInt = int(msg[i].encode("utf-8").hex(), 16)  # Caractère converti en Int
        kInt = int(key[j].encode("utf-8").hex(), 16)  # Caractère converti en Int
        encryptedInt = (mInt + kInt)  # Résultat en Int
        if (j == len(key) - 1):
            j = 0
        else:
            j += 1
        encrypted.extend(int.to_bytes(encryptedInt,
                                      4))  # On ajoute le résultat au tableau de bytes, et on transforme de Int >> Byte, d'une longueur de 4 Bytes
    return encrypted


def RSAEncrypt(msg, key):
    n = int(key.split(",")[0].split("n=")[1])
    e = int(key.split(",")[1].split("e=")[1])
    public_key = [e, n]
    print(f"e= {public_key[0]} - {type(public_key[0])} || n={public_key[1]} - {type(public_key[1])}")
    rsa = RSA.RSA()

    encrypted = bytearray()
    for c in msg:
        encrypted_int = rsa.RSAEncrypt(int.from_bytes(c.encode('utf-8')), public_key)
        print(f"Char = {c} - Int = {int.from_bytes(c.encode('utf-8'))} - Encrypted = {encrypted_int}")
        encrypted_byte = int.to_bytes(encrypted_int, 4)
        encrypted.extend(encrypted_byte)

    return encrypted

def hashEncrypt(command):
    salt = os.urandom(16)
    #combined = salt + command.encode()
    combined = command.encode()
    hashed = hashlib.sha256(combined).hexdigest()
    print(hashed)
    hashed = encodeMessage(hashed)
    print(hashed)
    return hashed