import translateOEA
import os
import time
import glob
import subprocess

startTime = time.time()
fileNames = [ "text_action_info", "text_attack_info", "text_attack_information", "text_attack_name", "text_battle_enemy_name", "text_debug",
    "text_dino_information", "text_dino_kind", "text_dino_name", "text_dino_short_name", "text_exchange_name", "text_field_debugmenu",
    "text_guid_message", "text_headmask", "text_keyitem_name", "text_map_name", "text_museum", "text_radarskin", "text_super_skill_information",
    "text_super_skill_name", "text_symbolicon", "text_symbolicon_group", "text_ui"
]

leftT = open("leftOffT.txt", "rt")
leftOffT = int(leftT.read())
leftT.close()

def obfuscateText(fileName):
    path = "./text/bin/" + fileName + "/"
    zero = open(path + "0.bin", "rb")
    reading = zero.read()
    zero.close()
    
    pointers = []
    dataStart = int.from_bytes(reading[12:16], "little")  
    for i in range(12, dataStart, 4):
        number = int.from_bytes(reading[i:(i + 4)], "little")
        pointers.append(number)
    pointers.append(os.stat(path + "0.bin").st_size)
    
    for i in range(len(pointers) - 1):
        new = open(path + "part_" + str(i) + ".bin", "wb")
        text = reading[pointers[i]:pointers[i + 1]].decode("UTF-8", errors = "backslashreplace")
        text = text.replace("%s", " %s ")        
        new.write(text.encode("UTF-8", errors = "backslashreplace"))
        new.close()
        translateOEA.doIt(path + "part_" + str(i) + ".bin", path + "part_" + str(i) + "_o.bin")
        new = open(path + "part_" + str(i) + "_o.bin", "rb")
        text = new.read().decode("UTF-8", errors = "backslashreplace")
        text = text.replace(" %s ", "%s")
        new = open(path + "part_" + str(i) + "_o.bin", "wb")
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

for i in range(leftOffT, 23):
    leftT = open("leftOffT.txt", "wt")
    leftT.write(str(i))
    leftT.close()
    print(str(i), flush = True)
    obfuscateText(fileNames[i])

for i in range(23):
    file = open("./text/bin/" + fileNames[i] + "/combined.bin", "rb")
    text = file.read().decode("UTF-8", errors = "backslashreplace")
    file.close()
    file = open("./text/bin/" + fileNames[i] + "/combined.bin", "wb")
    file.write(text.encode("UTF-8", errors = "backslashreplace"))
    file.close()
    
    os.rename("./text/bin/" + fileNames[i] + "/combined.bin", "./KASEKI2 - COPY/data/text/" + fileNames[i])
    subprocess.run([ "./fftool.exe", "compress", "./KASEKI2 - COPY/data/text", "-o", fileNames[i], "-i", fileNames[i],
        "-c", "Huffman", "-c", "Lzss" ])
    
print("This took " + str(int((time.time() - startTime) / 60)) + " minutes")