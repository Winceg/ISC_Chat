import socket
import crypto_logic as logic
import run_chat_client as chat

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    HOST = "vlbelintrocrypto.hevs.ch"
    PORT = 6000

    chat.start_client(HOST, PORT)