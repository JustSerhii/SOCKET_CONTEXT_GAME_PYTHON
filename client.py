import socket
import logging

HOST = '127.0.0.1'
PORT = 1025 + 10


class Client:

    def __init__(self):
        try:
            sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
            )
            logging.getLogger("Client")
            logging.basicConfig(filename="myClient.log",
                                level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s',
                                filemode='a',
                                )

            logging.info('Client started.')

            sock.connect((HOST, PORT))
            logging.info("Connected to a server.")
            while True:
                data = sock.recv(256).decode('utf-8')
                print(data)
                if data.__contains__("stop the program by using '/EXIT'."):
                    break
            logging.info('Got a welcome message.')
            while True:
                data = input('Send context:\n')
                sock.send(data.encode('utf-8'))
                logging.info('Sent context: ' + data)
                data = sock.recv(256).decode('utf-8')
                logging.info('Received message: ' + data)
                print('Answer:\n', data)
                if "/EXIT" in data:
                    sock.close()
                    logging.info("End of session")
                    break
            print('Connection closed.')
            logging.info('Connection closed.')
        except Exception as e:
            print(f'Happened exception: {e}')
            logging.info('Caught an error. Closing connection.')


def main():
    client = Client()


if __name__ == "__main__":
    main()
