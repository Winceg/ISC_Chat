import RSA
import DH
import hashlib  # Provides access to cryptographic hash functions like SHA-256


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
        case 6:
            return "DH half key"
        case 0 | _:
            return "none"


def sendQuery(query_type, cipher_type, direction, text_len, msg=""):
    header = "ISC" + query_type
    if query_type == "s":
        match cipher_type:
            case 4:
                command = "task hash hash"
            case 5:
                command = "task hash verify"
            case 6:
                command = "task DifHel"
            case _:
                command = "task " + cipherTypeString(cipher_type) + " " + direction + " " + str(text_len)
        message = header.encode('utf-8') + len(command).to_bytes(2, byteorder='big') + encrypt(command, 0)
        print(f"Query :    {decodeMessage(message)}")
    elif query_type == "t":
        message = header.encode('utf-8') + len(msg).to_bytes(2, byteorder='big') + encrypt(msg, 0)
    return message


def sendReply(query_type, cipher_type, key, msg):
    header = "ISC" + query_type
    payload = encrypt(msg, cipher_type, key)
    match cipher_type:
        case 4:
            msg_length = int(len(payload) / 4)
        case 5:
            msg_length = len(msg)
            payload = encodeMessage(msg)
        case 6:
            msg_length = len(payload.decode('utf-8'))
        case _:
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
        case 5:
            return encodeMessage("hash_verify")
        case 6:
            dh = DH.DifHel()
            if not command:
                return dh.dh_half_key(key)
            else:
                return dh.dh_encrypt(command)
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
    print(f"e= {public_key[0]} || n={public_key[1]}")
    rsa = RSA.RSA()

    encrypted = bytearray()
    for c in msg:
        encrypted_int = rsa.RSAEncrypt(int.from_bytes(c.encode('utf-8')), public_key)
        encrypted_byte = int.to_bytes(encrypted_int, 4)
        encrypted.extend(encrypted_byte)
        print(f"e= {public_key[0]} || n={public_key[1]} || c= {c} || encrypted c= {encrypted_int}")
    return encrypted


def hashEncrypt(command):
    combined = command.encode()
    hashed = hashlib.sha256(combined).hexdigest()
    hashed = encodeMessage(hashed)
    return hashed

def hashVerify(text, hash):
    c_hash = f"{decodeResponse(hashEncrypt(text))[1]}{decodeResponse(hashEncrypt(text))[0]}"
    print(f"received text:   {text}")
    print(f"received hash:   {hash}")
    print(f"calculated hash: {c_hash}")
    if c_hash == hash:
        return "True"
    else:
        return "False"