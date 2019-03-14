#!/usr/bin/env python
import subprocess
import random

def randomevenint():
    while True:
        num = int(str(randomints())[:2])
        if (num % 2) == 0:
            return num

def randomints():
    return random.randint(0, 255)

def call(command):
    subprocess.call(command, shell=True)

def randomMAC():
    return ("%02x:%02x:%02x:%02x:%02x:%02x" % (
        randomevenint(),
        randomints(),
        randomints(),
        randomints(),
        randomints(),
        randomints())
        )


if __name__ == "__main__":
    rando = randomMAC()
    print("Your new MAC is %s" %rando)
    call("ifconfig eth0 down")
    call("ifconfig eth0 hw ether " + rando)
    call("ifconfig eth0 up")