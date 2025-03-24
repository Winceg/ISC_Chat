import socket
import crypto_logic as logic
import run_chat_client as chat

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    HOST = "vlbelintrocrypto.hevs.ch"
    PORT = 6000

    chat.start_client(HOST, PORT)

    """

    query_type = "s"
    cipher = 2
    direction = "encode"
    text_len = 20

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(logic.sendQuery(query_type, cipher, direction, text_len))

    data1 = s.recv(1024)
    data2 = s.recv(1024)
    print(f"Received : {logic.decodeMessage(data1)}")
    print(f"Received : {logic.decodeMessage(data2)}")

    s.sendall(logic.sendReply(query_type, cipher, input("Enter key : "), logic.decodeResponse(data2)))
    print(f"Received : {logic.decodeMessage(s.recv(1024))}")
    print(f"Received : {logic.decodeMessage(s.recv(1024))}")

"""

    """
    s.sendall(sendMessage(type, decodeResponse(data2), 1, input("Enter shift key: ")))
    #command = "task shift encode 10"
    command = "task vigenere encode 10"
    #s.sendall(logic.sendMessage(query_type, command, cipher, text_len))
    # s.sendall(logic.sendMessage(type, command))
    """
