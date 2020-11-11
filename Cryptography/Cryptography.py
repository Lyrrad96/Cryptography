from tkinter import *
import random
from time import sleep
root=Tk()
root.geometry("800x800")

ch=StringVar()
message=StringVar()
k=StringVar()
img=StringVar()
nimg=StringVar()
o=StringVar()
fname=StringVar()

from PIL import Image

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

        # list of binary codes
        # of given data
        newd = []

        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1

        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def dat():
    f=open("RSA_encrypted.txt", "r")
    return f.read()
    f.close()


# Encode data into image
def encode():
    im = img.get()#input("Enter image name(with extension) : ")
    image = Image.open(im, 'r')
    #f=open("RSA_encrypted.txt", "r")data=f.read()
    #data = input("Enter data to be encoded : ")
    data=dat()

    #if (len(data) == 0):
       # raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = nimg.get()#input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
    Label(root, text='Steganography Completed', font="bold").grid(row=20, column=0)
    Button(root, text='quit', command=quit).grid(row=30, column=0)


# Decode the data in the image
def decode():
    im = img.get()#input("Enter image name(with extension) : ")
    image = Image.open(im, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

def gcd(a, b):
    """
    Performs the Euclidean algorithm and returns the gcd of a and b
    """
    if (b == 0):
        return a
    else:
        return gcd(b, a % b)

def xgcd(a, b):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a, and coefficient of b
    """
    x, old_x = 0, 1
    y, old_y = 1, 0

    while (b != 0):
        quotient = a // b
        a, b = b, a - quotient * b
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    return a, old_x, old_y

def chooseE(totient):
    """
    Chooses a random number, 1 < e < totient, and checks whether or not it is 
    coprime with the totient, that is, gcd(e, totient) = 1
    """
    while (True):
        e = random.randrange(2, totient)

        if (gcd(e, totient) == 1):
            return e

def chooseKeys():
    """
    Selects two random prime numbers from a list of prime numbers which has 
    values that go up to 100k. It creates a text file and stores the two 
    numbers there where they can be used later. Using the prime numbers, 
    it also computes and stores the public and private keys in two separate 
    files.
    """

    # choose two random numbers within the range of lines where 
    # the prime numbers are not too small and not too big
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    # store the txt file of prime numbers in a python list
    fo = open('primes-to-100k.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    # store our prime numbers in these variables
    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    # compute n, totient, e
    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    # compute d, 1 < d < totient such that ed = 1 (mod totient)
    # e and d are inverses (mod totient)
    gcd, x, y = xgcd(e, totient)

    # make sure d is positive
    if (x < 0):
        d = x + totient
    else:
        d = x

    # write the public keys n and e to a file
    f_public = open('public_keys.txt', 'w')
    f_public.write(str(n) + '\n')
    f_public.write(str(e) + '\n')
    f_public.close()

    f_private = open('private_keys.txt', 'w')
    f_private.write(str(n) + '\n')
    f_private.write(str(d) + '\n')
    f_private.close()
def encrypt(message, file_name = 'public_keys.txt', block_size = 2):
    """
    Encrypts a message (string) by raising each character's ASCII value to the 
    power of e and taking the modulus of n. Returns a string of numbers.
    file_name refers to file where the public key is located. If a file is not 
    provided, it assumes that we are encrypting the message using our own 
    public keys. Otherwise, it can use someone else's public key, which is 
    stored in a different file.
    block_size refers to how many characters make up one group of numbers in 
    each index of encrypted_blocks.
    """

    try:
        fo = open(file_name, 'r')

    # check for the possibility that the user tries to encrypt something
    # using a public key that is not found
    except FileNotFoundError:
        print('That file is not found.')
    else:
        n = int(fo.readline())
        e = int(fo.readline())
        fo.close()

        encrypted_blocks = []
        ciphertext = -1

        if (len(message) > 0):
            # initialize ciphertext to the ASCII of the first character of message
            ciphertext = ord(message[0])

        for i in range(1, len(message)):
            # add ciphertext to the list if the max block size is reached
            # reset ciphertext so we can continue adding ASCII codes
            if (i % block_size == 0):
                encrypted_blocks.append(ciphertext)
                ciphertext = 0

            # multiply by 1000 to shift the digits over to the left by 3 places
            # because ASCII codes are a max of 3 digits in decimal
            ciphertext = ciphertext * 1000 + ord(message[i])

        # add the last block to the list
        encrypted_blocks.append(ciphertext)

        # encrypt all of the numbers by taking it to the power of e
        # and modding it by n
        for i in range(len(encrypted_blocks)):
            encrypted_blocks[i] = str((encrypted_blocks[i]**e) % n)

        # create a string from the numbers
        encrypted_message = " ".join(encrypted_blocks)

        return encrypted_message


def decrypt(blocks, block_size = 2):
    """
    Decrypts a string of numbers by raising each number to the power of d and 
    taking the modulus of n. Returns the message as a string.
    block_size refers to how many characters make up one group of numbers in
    each index of blocks.
    """

    fo = open('private_keys.txt', 'r')
    n = int(fo.readline())
    d = int(fo.readline())
    fo.close()

    # turns the string into a list of ints
    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    # converts each int in the list to block_size number of characters
    # by default, each int represents two characters
    for i in range(len(int_blocks)):
        # decrypt all of the numbers by taking it to the power of d
        # and modding it by n
        int_blocks[i] = (int_blocks[i]**d) % n
        
        tmp = ""
        # take apart each block into its ASCII codes for each character
        # and store it in the message string
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000
        message += tmp

    return message

def new():
    Label(root, text='Enter name of new image').grid(row=11, column=0)
    Entry(root, textvariable=nimg).grid(row=11, column=1)
    Button(root, text='Encrypt', command=encode).grid(row=11, column=3)


def stegenc():
    Label(root, text='Steganography', font=20).grid(row=9, column=0)    
    Label(root, text='Enter name of image').grid(row=10, column=0)
    Entry(root, textvariable=img).grid(row=10, column=1)
    Button(root, text='next', command=new).grid(row=10, column=3)

def stegdec():
    Label(root, text='Text is :').grid(row=7, column=0)
    Label(root, text=decrypt(decode())).grid(row=7, column=1)
    #Label(root, text='Enter image name').grid(row=7, column=0)
    Button(root, text='quit', command=quit).grid(row=30, column=0)

    #Button(root, text='next', command=dec).grid(row=6, column=3)
    
def printenc():
    Label(root, text='Encrypting...').grid(row=7, column=0)

def enc():

    f=open("RSA_encrypted.txt","w")
    g=open(fname.get(), "r")
    f.write(encrypt(g.read()))
    f.close()
    g.close()
    Label(root, text='RSA Completed', font="bold").grid(row=8, column=0)
    Button(root, text='Perform\nsteganography', command=stegenc).grid(row=8, column=3)

def key():
    Label(root, text='Do you want to generate new\n Public and Private Keys').grid(row=6, column=0)
    Radiobutton(root, text='Yes', variable=k, value='y', command=chooseKeys).grid(row=6, column=1)
    Radiobutton(root, text='No', variable=k, value='n').grid(row=6, column=2)
    Button(root, text='Encrypt', command=printenc and enc).grid(row=6, column=3)

def choice():
    if ch.get()=='e':
        Label(root, text='What do you want to encrypt?').grid(row=5, column=0)
        Entry(root, text='Enter filename', textvariable=fname).grid(row=8, column=1, rowspan=2)

        #Entry(root, textvariable=message).grid(row=5, column=1)
        Button(root, text='next', command=key).grid(row=5, column=3)
    else:
        Label(root, text='Enter image name').grid(row=5, column=0)
        Entry(root, textvariable=img).grid(row=5, column=1)
        Button(root, text='decrypt', command=stegdec).grid(row=5, column=3)

Label(root, text='Cryptography', font=("Times", 30)).grid(row=0, column=0, rowspan=2, columnspan=2)
Label(root, text='RSA', font=("MS\ Serif", 20)).grid(row=2, column=0)
Label(root, text='What would you like to do?').grid(row=4, column=0)
Radiobutton(root, text='Encrypt', variable=ch, value='e').grid(row=4, column=1)
Radiobutton(root, text='Decrypt', variable=ch, value='d').grid(row=4, column=2)
Button(root, text='next', command=choice).grid(row=4, column=3)


Button(root, text='quit', command=quit).grid(row=30, column=0)

root.mainloop()
