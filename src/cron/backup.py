import requests
import logging


def do_backup():
    response = requests.post(
        f"http://persistence:5000/backup",
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        })
    response.raise_for_status()
    logging.info(f"Response: {response}")


if __name__ == '__main__':
    do_backup()