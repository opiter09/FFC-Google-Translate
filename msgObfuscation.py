import translateOEA
import os
import time
import glob
import subprocess

startTime = time.time()
controlCodes = [ "$c0", "$c1", "$c2", "$c3", "$c4", "$a90", "$p", "$f", "â€œ", "â€", "$w0", "$t120", "$e\n", "$l1", "$r6", "$tc4", "%" ]

left = open("leftOff.txt", "rt")
leftOff = int(left.read())
left.close()

def obfuscateMsg(fileName):
    path = "./msg/bin/" + fileName + "/"
    zero = open(path + "0.bin", "rb")
    reading = zero.read()
    zero.close()
    
    pointers = []
    index = 12
    number = 0
    while (number != 8):
        number = int.from_bytes(reading[index:(index + 4)], "little")
        pointers.append(number)
        index = index + 4
    pointers[-2] = os.stat(path + "0.bin").st_size
    pointers.pop(-1)
    
    for i in range(len(pointers) - 1):
        new = open(path + "part_" + str(i) + ".bin", "wb")
        text = reading[(pointers[i] + 8):pointers[i + 1]].decode("UTF-8", errors = "backslashreplace")
        for j in controlCodes:
            text = text.replace(j, " " + j + " ")        
        new.write(text.encode("UTF-8", errors = "backslashreplace"))
        new.close()
        translateOEA.doIt(path + "part_" + str(i) + ".bin", path + "part_" + str(i) + "_o.bin")
        new = open(path + "part_" + str(i) + "_o.bin", "rb")
        text = new.read().decode("UTF-8", errors = "backslashreplace")
        text = text.replace("FF", " $f ")
        for j in controlCodes:
            text = text.replace(" " + j + " ", j)
        new.close()
        new = open(path + "part_" + str(i) + "_o.bin", "wb")
        new.write(reading[pointers[i]:(pointers[i] + 8)] + text.encode("UTF-8", errors = "backslashreplace"))
        new.close()
            
    combined = open(path + "combined.bin", "ab")
    combined.write(reading[0:16])
    total = int.from_bytes(reading[12:16], "little")
    for i in range(len(pointers) - 2):
        size = os.stat(path + "part_" + str(i) + "_o.bin").st_size
        total = total + size
        combined.write(total.to_bytes(4, "little"))
    for i in range(len(pointers) - 1):
        file = open(path + "part_" + str(i) + "_o.bin", "rb")
        combined.write(file.read())
        file.close()

if (leftOff < 1251):
    for i in range(leftOff, 1251):
        if (os.path.exists("./msg/bin/msg_" + str(i).zfill(4)) == True):
            left = open("leftOff.txt", "wt")
            left.write(str(i))
            left.close()
            print(str(i), flush = True)
            obfuscateMsg("msg_" + str(i).zfill(4))
        if (i == 1250):
            left = open("leftOff.txt", "wt")
            left.write(str(i))
            left.close()
            leftOff = 1251

remainder = [ "msg_cleaning", "msg_cleaning_coop", "msg_dig", "msg_horiderdiary", "msg_movie_jimaku" ]
for i in range(leftOff - 1251, 5):
    left = open("leftOff.txt", "wt")
    left.write(str(i + 1251))
    left.close()
    obfuscateMsg(remainder[i])

for i in range(1251):
    if (os.path.exists("./msg/bin/msg_" + str(i).zfill(4)) == True):
        file = open("./msg/bin/msg_" + str(i).zfill(4) + "/combined.bin", "rb")
        text = file.read().decode("UTF-8", errors = "backslashreplace")
        for i in range(4):
            text.replace("C" + str(i), "$c" + str(i))
        file.close()
        file = open("./msg/bin/msg_" + str(i).zfill(4) + "/combined.bin", "wb")
        file.write(text.encode("UTF-8", errors = "backslashreplace"))
        file.close()
        
        os.rename("./msg/bin/msg_" + str(i).zfill(4) + "/combined.bin", "./KASEKI2 - COPY/data/msg/msg_" + str(i).zfill(4))
        subprocess.run([ "./fftool.exe", "compress", "./KASEKI2 - COPY/data/msg", "-o", "msg_" + str(i).zfill(4), "-i", "msg_" + str(i).zfill(4),
            "-c", "Huffman", "-c", "Lzss" ])
for i in range(5):
    file = open("./msg/bin/" + remainder[i] + "/combined.bin", "rb")
    text = file.read().decode("UTF-8", errors = "backslashreplace")
    for i in range(4):
        text.replace("C" + str(i), "$c" + str(i))
    file.close()
    file = open("./msg/bin/" + remainder[i] + "/combined.bin", "wb")
    file.write(text.encode("UTF-8", errors = "backslashreplace"))
    file.close()
        
    os.rename("./msg/bin/" + remainder[i] + "/combined.bin", "./KASEKI2 - COPY/data/msg/" + remainder[i])
    subprocess.run([ "./fftool.exe", "compress", "./KASEKI2 - COPY/data/msg", "-o", remainder[i], "-i", remainder[i],
        "-c", "Huffman", "-c", "Lzss" ])
    
print("This took " + str(int((time.time() - startTime) / 60)) + " minutes")