import socket
import logging
import re

with open('textfile.txt', 'r') as f:
    lines = f.read()
    lines_l = lines.lower()
    lines = re.split('[.!?]', lines)
    lines_l = re.split('[.!?]', lines_l)

class Server:
    def __init__(self):

        try:

            HOST = '127.0.0.1'
            PORT = 1025 + 10
            utf = 'utf-8'

            logging.getLogger("Server")
            logging.basicConfig(filename="myServer.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info("Server started")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                sock.bind((HOST, PORT))
            except OSError:
                print("Host is used.")
                logging.warning("HOST IS USED. ")
                exit()
            sock.listen(1)
            connection, client_address = sock.accept()

            print("Connected:", client_address)
            logging.info("Connected to a client. ")

            for sentence in self.welcome_message():
                connection.send(sentence.encode(utf))
            logging.info("Sent a welcome message.")

            print("Listening")
            logging.info('Listening to a client.')

            try:
                while True:
                    data = connection.recv(256).decode(utf)
                    logging.info(f'Received message: {data}')
                    print(data)
                    if not data:
                        break

                    if "/EXIT" in data:
                        connection.send("/EXIT".encode(utf))
                        print("Connection stopped.")
                        sock.close()
                        break

                    if data == "/WHO":
                        connection.send(self.whoami().encode(utf))
                        logging.info("Sent a whoami message.")
                    else:
                        results = self.search(data)

                        connection.send(results.encode(utf))
                        logging.info("Sent message: " + results)
            except:
                print("ERROR.")
                sock.send("STOP".encode(utf))
                logging.error("Caught en error. Closing connection.")
        finally:
            try:
                sock.close()
            except Exception as e:
                print(f' !Exception {e}')
                logging.warning(f'{e}')
            print("Connection closed.")

    def search(self, data: str):
        try:
            result = "" ""
            counter = 0
            for i, line in enumerate(lines_l):
                if data.lower() in line:
                    result += '(' + str(i + 1) + ')' + lines[i] + '.\n'
                    counter += 1
            if counter == 0:
                result += "Warning: no such context!\n"
            return result
        except Exception as e:
            return f"={e}"

    def welcome_message(self):
        welcome = [
            "Hello! Within this lab you can send a context to the server and then receive the message.",
            "In case the program finds the context within the text file, you will get the ",
            "lines with the context in it.",
            "If the context won't be found you will get the warning message.",
            "Either way you can always stop the program by using '/EXIT'."
        ]
        return welcome

    def whoami(self):
        who = "K26 student Zhelezniak Serhii. Variant - 10.\n"
        return who


def main():
    root = Server()


if __name__ == "__main__":
    main()
