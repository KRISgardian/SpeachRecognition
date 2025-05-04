import time 
import random








def getRandomHashName():
    salt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    currentTime = int(time.time())
    
    random.shuffle(salt)

    salt = salt[:8] + list(str(currentTime).replace('', ' ').split())

    random.shuffle(salt)

    return str(salt).replace('[', '').replace(']', '').replace(',', '').replace('\'', '').replace(' ', '')