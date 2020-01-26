# Credits
# Written by Garlfin and Danila voronochkin (Данила вороночкин)
# youtube/sciong @garlfin - vk/cms_vorono4ka
# Big thanks to BlaCoiso, Sector, Cosmic, and Kjkui (They were nice to me when I pestered them)
# Possibly get support in this discord (not guaranteed): https://discord.gg/E3ket4T


import struct
import sys
import os
import os.path


def printDebug(inputSTR):
    if len(sys.argv) > 2:
        print("DEBUG: " + inputSTR)


def printDebugQuestion(inputSTRQuest):
    if len(sys.argv) > 2:
        print("DEBUG: " + inputSTRQuest)
        ynQuackstion = input()  # ynQuestion... more like ynQuackstion

        if ynQuackstion.lower() == 'y':
            return True
        else:
            return False


def crap():
    pathtoobj = str(sys.argv[1])
    # print(str(sys.argv[1]))
    obj = open(pathtoobj, 'r')
    vn = []
    vt = []
    v = []
    f = []

    textFixed = open(pathtoobj).read()
    for line in textFixed.split('\n'):
        if line.startswith('f ') and len(line.split()) == 5:
            fragments = ''
            for l in range(1, len(line.split())):
                if l < 4:
                    fragments += line.split()[l] + ' '
                else:
                    fragments1 = ' '.join(fragments.split()[0::2]) + ' ' + line.split()[l]
                    textFixed = textFixed.replace(line, 'f %s\nf %s' % (fragments, fragments1))
    open(pathtoobj, 'w').write(textFixed)
    for line in obj.read().split('\n'):
        if line.startswith('v '):
            for x in range(3):
                v.append(float(line.split()[x + 1]))
        elif line.startswith('vn '):
            for x in range(3):
                vn.append(float(line.split()[x + 1]))
        elif line.startswith('vt '):
            for x in range(2):
                vt.append(float(line.split()[x + 1]))
        elif line.startswith('f '):
            for x in range(3):
                f.append(line.split()[x + 1].split('/')[0])  # v
                f.append(line.split()[x + 1].split('/')[2])  # vn
                f.append(line.split()[x + 1].split('/')[1])  # vt

    if len(v) == 0:
        print(pathtoobj + " doesnt have any geometry! ABORTING")
        return
    if len(v) >= 65535*3:
        print(pathtoobj + " has too much geometry! ABORTING")
        return
    if len(vn) >= 65535*3:
        print(pathtoobj + " has too many normals! ABORTING")
        return
    if len(f) == 0:
        print(pathtoobj + " doesnt have any triangles! ABORTING")
        return
    if len(f) >= 65535*9:
        print(pathtoobj + " has too many triangles! ABORTING")
        return
    if len(vt) >= 65535*2:
        print(pathtoobj + " has too many texture coordinates! ABORTING")
        return

    printDebug("Vertex Length: " + str(len(v)))
    printDebug("Vertex Texture Length: " + str(len(vt)))
    printDebug("Vertex Normal Length: " + str(len(vn)))
    printDebug("Triangle Length: " + str(len(f)))
    boolYESNO = printDebugQuestion("Display file content? Y/N")
    printDebug(str(boolYESNO))
    if boolYESNO == True:
        itWouldntHurt = open(pathtoobj).read()
        arrayText = ""
        for line in itWouldntHurt.split('\n'):
            arrayText += line + " "
        printDebug(arrayText)

    vt[1::2] = [x * -1 + 1 for x in vt[1::2]]
    # print(v)
    in_file = open("nita_bear_geo.scw", "rb")
    geoPacked = in_file.read(55)
    size = int(29125 + len(v) / 3 * 6 + len(vn) / 3 * 6 + len(vt) / 2 * 4 + len(f) / 9 * 18)
    in_file.seek(35769)
    geoPacked += struct.pack('>i4sh4sh6s', size, 'GEOM'.encode('utf-8'), 4, 'main'.encode('utf-8'), 6,
                             'geoGrp'.encode('utf-8'))

    geoPacked += b"\x03"
    geoPacked += struct.pack('>h8s', 8, "POSITION".encode('utf-8'))

    geoPacked += b"\x00"
    scalev = max(max(v), abs(min(v)))

    geoPacked += struct.pack('>hfI', 3, scalev, int(len(v) / 3))
    for x in v:
        geoPacked += struct.pack('>h', int(x * 32767 / scalev))

    geoPacked += struct.pack('>h6s', 6, "NORMAL".encode('utf-8'))

    geoPacked += b"\x01"
    scalevn = max(max(vn), abs(min(vn)))
    geoPacked += struct.pack('>HfI', 3, scalevn, int(len(vn) / 3))
    for vbruh in vn:
        geoPacked += struct.pack('>h', int(vbruh * 32767 / scalevn))

    geoPacked += struct.pack('>h8s', 8, "TEXCOORD".encode('utf-8'))  # LINE 65 oh

    geoPacked += b"\x02"

    if len(vt) == 0:
        print(pathtoobj + " doesn't have any texture coordinates! Setting vtcount to 0!")
        geoPacked += struct.pack('>HfI', 2, 1, 0)
    else:
        scalevt = max(max(vt), abs(min(vt)))
        geoPacked += struct.pack('>HfI', 2, scalevt, int(len(vt) / 2))
        for x in vt:
            geoPacked += struct.pack('>h', int(x * 32512 / scalevt))
    data2 = in_file.read(29045)
    geoPacked += data2
    geoPacked += struct.pack('>HH', int(len(f) / 9), 770)  # testing time!
    for x in f:
        geoPacked += struct.pack('>h', int(x) - 1)  # i fixed it! Ok

    geoPacked += struct.pack('I', 62384957)
    in_file.seek(142834)

    data3 = in_file.read()
    geoPacked += data3
    in_file.close()
    out_file = open(os.path.splitext(os.path.basename(pathtoobj))[0] + ".scw", "wb")
    out_file.write(geoPacked)
    out_file.close()
    print("Done at " + os.path.splitext(os.path.basename(pathtoobj))[0] + ".scw")


if len(sys.argv) >= 2:
    pathtoobj = str(sys.argv[1])
    print("INITALIZING " + str(sys.argv[1]) + ".")
    if os.path.exists(pathtoobj):
        print(pathtoobj + " exists.")
        crap()

    else:
        print(pathtoobj + " doesn't exist. Please check it and try again")
elif len(sys.argv) == 1:
    print("Please provide the path to the obj. Ex: python convert.py quackage.obj")
