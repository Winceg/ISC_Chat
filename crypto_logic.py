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


"""
def decodeResponse(message):
    msg = int_to_string(message[6:].decode('utf-8'))
    res = msg.replace('\x00', '')
    return res
"""


def decodeResponse(message):
    msg = message[6:].decode('utf-8')
    res = msg.replace('\x00', '')
    return res


# cipherType:
# 0 = no cipher
# 1 = shift
# 2 = vigénère
# 3 = RSA
"""
def sendMessage(direction, query_type, command="", cipher_type="none", key=0, textLen=15):
    header = "ISC"
    msgLength = len(command)
    print("Command !")
    payload = (" task " + cipherTypeString(cipher_type) + " " + direction + " " + str(textLen)).encode('utf-8')
    message = header.encode('utf-8') + query_type.encode('utf-8') + msgLength.to_bytes(2, byteorder='big') + payload
    print(f"Message :{decodeMessage(message)}")
    return message
"""


def cipherTypeString(cipher_type):
    match cipher_type:
        case 1:
            return "shift"
        case 2:
            return "vigenere"
        # case 3:
        # return "rsa"
        case 0 | _:
            return "none"


def sendQuery(query_type, cipher_type, direction, text_len):
    header = "ISC" + query_type
    command = "task " + cipherTypeString(cipher_type) + " " + direction + " " + str(text_len)
    msg_length = len(command)
    message = header.encode('utf-8') + msg_length.to_bytes(2, byteorder='big') + encrypt(command, 0)
    print(f"Query :    {decodeMessage(message)}")
    return message


def sendReply(query_type, cipher_type, key, msg):
    header = "ISC" + query_type
    payload = encrypt(msg, cipher_type, key)
    print(msg)
    print(len(msg))
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
        # case 3:
        # return RSAEncrypt(command, key)
        case 0 | _:
            return encodeMessage(command)


def shiftEncrypt(msg, key):
    res = bytearray()
    for c in msg:
        res.extend(int.to_bytes(int.from_bytes(c.encode('utf-8')) + int(key), 4))
    return res


##Après :
def vigenereEncrypt(msg, key):
    res = bytearray()  # De type tableau de byte (bytearray), le type qui doit être envoyé au serveur
    j = 0
    for i in range(0, len(msg)):
        mInt = int(msg[i].encode("utf-8").hex(), 16)  # Caractère converti en Int
        kInt = int(key[j].encode("utf-8").hex(), 16)  # Caractère converti en Int
        encryptedInt = (mInt + kInt)  # Résultat en Int
        if (j == len(key) - 1):
            j = 0
        else:
            j += 1
        res.extend(int.to_bytes(encryptedInt,
                                4))  # On ajoute le résultat au tableau de bytes, et on transforme de Int >> Byte, d'une longueur de 4 Bytes
    return res


# def RSAEncrypt(msg, publicKey):
#   return res