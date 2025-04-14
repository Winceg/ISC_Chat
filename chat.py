import sys  # For system-level operations and command line arguments
import socket  # For network communication
import threading  # For concurrent execution
from PySide6.QtWidgets import QApplication, QWidget  # Core PySide6 widgets
from PySide6.QtUiTools import QUiLoader  # For loading UI files created with Qt Designer
import crypto_logic as logic


class ChatClient(QWidget):
    """
    A PySide6-based chat client that connects to a server and allows
    sending/receiving messages through a graphical interface.
    """
    host = ""
    port = 0
    key = ""
    msg = ""

    def get_key(self):
        self.key = self.ui.keyField.text()
        return self.key

    def get_msg(self):
        self.msg = self.ui.messageField.text()
        return self.msg

    def __init__(self, host='localhost', port=12345):
        """
        Initialize the chat client with server connection details.

        Args:
            host (str): Server hostname or IP address (default: localhost)
            port (int): Server port number (default: 12345)
        """
        self.host = host
        self.port = port
        super(ChatClient, self).__init__()  # Initialize parent QWidget class
        loader = QUiLoader()  # Create a QUiLoader instance
        self.ui = loader.load('./src/views/chat_gui2-Bruno.ui', self)  # Load the UI design from file
        self.setWindowTitle('103.2 - Simple chat GUI')  # Set window title
        self.ui.text_LenField.setText("30")
        self.ui.sendButton.clicked.connect(self.send_message)  # Connect button click to send_message method
        self.ui.replyButton.clicked.connect(self.send_reply)  # Connect button click to send_reply method
        self.ui.clearButton.clicked.connect(self.clear)  # Connect button click to clear method
        self.socket = socket.socket()  # Create a new socket object for server communication
        self.connect_to_server(self.host, self.port)  # Establish connection to the server
        print(f"Connected to: {self.host} on port {self.port}")

    def connect_to_server(self, host, port):
        """
        Attempt to connect to the chat server.

        Args:
            host (str): Server hostname or IP address
            port (int): Server port number
        """
        try:
            self.socket.connect((host, port))  # Connect to server using provided host and port
        except socket.error as e:
            print(f"Error connecting to server: {e}")  # Print error message if connection fails
            self.close()  # Close the application window

    def get_direction(self):
        if self.ui.encodeRadioButton.isChecked():
            return "encode"
        elif self.ui.decodeRadioButton.isChecked():
            return "decode"

    def get_type(self):
        if self.ui.textRadioButton.isChecked():
            return "t"
        elif self.ui.serverRadioButton.isChecked():
            return "s"
        elif self.ui.imageRadioButton.isChecked():
            return "i"

    def get_cipher(self):
        if self.ui.shiftRadioButton.isChecked():
            return 1
        elif self.ui.vigenereRadioButton.isChecked():
            return 2
        elif self.ui.rsaRadioButton.isChecked():
            return 3
        elif self.ui.hashRadioButton.isChecked():
            return 4
        elif self.ui.hashVerifyRadioButton.isChecked():
            return 5
        elif self.ui.dhRadioButton.isChecked():
            return 6
        else:
            return 0

    def send_message(self):
        """
        Send the message entered by the user to the server and prepare to receive a response.
        """
        text_len = self.ui.text_LenField.text()
        message = self.get_msg()
        if text_len and self.get_type() == "s":  # Only proceed if text_len is not empty
            message_to_send = logic.sendQuery(self.get_type(), self.get_cipher(), self.get_direction(), text_len)
            self.ui.sendandrec.append(
                f'You:\t{logic.decodeMessage(message_to_send)}')  # Display user's message in the chat area
            self.socket.sendall(message_to_send)
            threading.Thread(
                target=self.receive_message).start()  # Start a new thread to receive response
        elif message and self.get_type() == "t":
            message_to_send = logic.sendQuery(self.get_type(), self.get_cipher(), self.get_direction(), text_len,
                                              self.get_msg())
            self.ui.sendandrec.append(
                f'You:\t{logic.decodeMessage(message_to_send)}')  # Display user's message in the chat area
            self.socket.sendall(message_to_send)
            threading.Thread(
                target=self.receive_message).start()  # Start a new thread to receive response

    def send_reply(self):
        """
        Send the message entered by the user to the server and prepare to receive a response.
        """
        if self.get_key() or self.get_cipher() == 4 or self.get_cipher() == 5:  # Only proceed if key is not empty or sending hash
            message_to_send = logic.sendReply(self.get_type(), self.get_cipher(), self.get_key(), self.get_msg())
            self.ui.sendandrec.append(
                f'You:\t{logic.decodeMessage(message_to_send)}')  # Display user's message in the chat area
            self.socket.sendall(message_to_send)
            threading.Thread(
                target=self.receive_result).start()  # Start a new thread to receive response

    def receive_message(self):
        """
        Receive and display the server's response message.
        """
        try:
            response = self.socket.recv(1024)  # Receive up to 1024 bytes and decode from UTF-8
            response = logic.decodeResponse(response)
            if response[1] == "s":
                if "key " in response[0]:
                    self.key = response[0].split("key ", 1)[1]
                    self.ui.keyField.setText(self.key)
                self.ui.sendandrec.append(f'Server:\t{response[0]}')  # Display the received message in the chat area

                server_response = False
                while not server_response:
                    response2 = self.socket.recv(1024)  # Receive up to 1024 bytes and decode from UTF-8
                    if response2:
                        response2 = logic.decodeResponse(response2)
                        if response2[1] == "s":
                            self.msg = response2[0]
                            if self.get_cipher() == 5:
                                self.msg = logic.hashVerify(self.msg.split("ISCs@")[0], self.msg.split("ISCs@")[1])
                            self.ui.messageField.setText(self.msg)
                            self.ui.sendandrec.append(
                                f'Server:\t{response2[0]}')  # Display the received message in the chat
                            server_response = True
                        elif response2[1] == "t":
                            self.ui.sendandrec.append(
                                f'Message:\t{response2[0]}')  # Display the received message in the chat

            elif response[1] == "t":
                self.ui.sendandrec.append(f'Message:\t{response[0]}')  # Display the received message in the chat

        except socket.error as e:
            print(f"Error receiving message: {e}")  # Print error message if receiving fails

    def receive_result(self):
        """
        Receive and display the server's response message.
        """
        server_response = False
        try:
            while not server_response:
                result = self.socket.recv(1024)  # Receive up to 1024 bytes and decode from UTF-8
                result = logic.decodeResponse(result)
                if result[1] == "s":
                    self.ui.sendandrec.append(f'Server:\t{result[0]}')  # Display the received message in the chat area
                    server_response = True
                elif result[1] == "t":
                    self.ui.sendandrec.append(f'Message:\t{result[0]}')  # Display the received message in the chat area
        except socket.error as e:
            print(f"Error receiving message: {e}")  # Print error message if receiving fails

    def clear(self):
        self.ui.messageField.setText("")
        self.ui.keyField.setText("")
        self.ui.text_LenField.setText("30")
        self.ui.sendandrec.setText("")
        self.socket = socket.socket()  # Create a new socket object for server communication
        self.connect_to_server(self.host, self.port)  # Establish connection to the server
        print(f"Connected to: {self.host} on port {self.port}")

    def close_event(self, event):
        """
        Handle the window close event by properly closing the socket connection.

        Args:
            event: The close event object
            :param event:
            :type self: object
        """
        self.socket.close()  # Close the socket connection
        event.accept()  # Accept the close event


def main():
    """
    Main function to initialize and run the chat client application.
    """
    app = QApplication(sys.argv)  # Create a new PySide6 application
    client = ChatClient()  # Create an instance of the chat client
    client.show()  # Display the client window
    sys.exit(app.exec())  # Start the application event loop


if __name__ == "__main__":
    main()  # Run the main function when script is executed directly

