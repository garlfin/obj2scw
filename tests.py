# Credits
# Written by Garlfin and Danila voronochkin (Данила вороночкин)
# youtube/sciong @garlfin - vk/cms_vorono4ka
# Big thanks to BlaCoiso, Sector, Cosmic, and Kjkui (They were nice to me when I pestered them)
# Possibly get support in this discord (not guaranteed): https://discord.gg/E3ket4T
import struct

obj = open('test.obj', 'r')
vn = []
vtpre = []
vt=[]
v = []
f = []
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
            f.append(line.split()[x + 1].split('/')[0])  # v PyCharm to help)
            f.append(line.split()[x + 1].split('/')[2])  # vn
            f.append(line.split()[x + 1].split('/')[1])

#Uvs are messed up, attemps to fix it:
vt[1::2] = [x*-1+1 for x in vt[1::2]]
#for x in range(1,len(vtpre),2):
   # vt.append(vtpre[x]*-1)

print("Made by Garlfin and Daniel")
print("This is in BETA and is not guaranteed to work.")
print("Make sure to triangulate the model.")
print("License in readme.md")

print("\n\nOBJ FAX:\nAmount of verticies: ",len(v),"\nAmount of UV Coords: ",len(vt))

#print(v)
#print(len(v), ":", len(v)/3)
fout = open('test.scw', 'wb')


def writeString(word):
    length = int.to_bytes(len(word), 2, 'big')
    return length + word.encode('utf-8')


def HeadWrite():
    headStruct = struct.Struct('>4sI4shhhhh28s')
    headPacked = headStruct.pack('SC3D'.encode('utf-8'), 39, 'HEAD'.encode('utf-8'), 2, 30, 0, 200, 28,'sc3d/character_materials.scw'.encode('utf-8'))
    fout.write(headPacked)
    # Remaining & CRC
    fout.write(b"\x00\xea\xe2\x3d\x90")


def GeomWrite():
    # GEOM
    geoStart = struct.Struct('>i4sh4sh6s')
    size = 104+(6*int(len(v)/3))+(6*int(len(vn)/3))+(4*int(len(vt)/2))+(18*int(len(f)/9))
    geoStartPacked = geoStart.pack(size, 'GEOM'.encode(
        'utf-8'), 4, 'main'.encode('utf-8'), 6, 'geoGrp'.encode('utf-8'))

    fout.write(geoStartPacked)
    fout.write(b"\x03")
    geoPOS = struct.pack('>h8s', 8, "POSITION".encode('utf-8'))
    fout.write(geoPOS)
    fout.write(b"\x00")
    scalev = max(max(v), abs(min(v)))

    POSITION = struct.pack('>hfI', 3, scalev, int(len(v)/3))
    for x in v:
        POSITION += struct.pack('>h', int(x*32767/scalev))

    POSITION += struct.pack('>h6s', 6, "NORMAL".encode('utf-8'))
    fout.write(POSITION)
    fout.write(b"\x01")  
    scalevn = max(max(vn), abs(min(vn)))
    NORMAL = struct.pack('>HfI', 3, scalevn, int(len(vn)/3))
    for vbruh in vn:
        NORMAL += struct.pack('>h', int(vbruh*32767/scalevn))

    NORMAL += struct.pack('>h8s', 8, "TEXCOORD".encode('utf-8'))  # LINE 65 oh
    fout.write(NORMAL)
    fout.write(b"\x02")
    scalevt = max(max(vt), abs(min(vt)))
    TEXCOORD = struct.pack('>HfI', 2, scalevt, int(len(vt)/2))
    for x in vt:
        TEXCOORD += struct.pack('>h', int(x*32512/scalevt))
        #TEXCOORD += struct.pack('>h', int(vt[x-1]*32512/scalevt))
        #TEXCOORD += struct.pack('>h', 1-int(vt[x]*32512/scalevt))
    fout.write(TEXCOORD)
    fout.write(b"\x00\x00\x00\x00\x00\x00\x01")
    Finalstuff = struct.pack('>h13sHHH', 13, "character_mat".encode('utf-8'), 0, int(len(f)/9), 770)  # testing time!
    for x in f:
        Finalstuff += struct.pack('>h', int(x)-1)# i fixed it! Ok
    fout.write(Finalstuff)
    fout.write(b"\x3D\xeb\xb7\x03")


def NodeWrite():
    nodePacked = struct.pack('>I4sHH9sHHHBhhhhhffffffH4sH9sHHBhhhhhffffffH4sH4sH4sH4sHH13sH13sHBBBB', 168, "NODE".encode('utf-8'), 3, 9, "CHARACTER".encode('utf-8'), 0, 0, 1, 0, 0, 0, 0, 0, 32512, 0, 0, 0, 1, 1, 1, 4, "ROOT".encode('utf-8'), 9, "CHARACTER".encode(
        'utf-8'), 0, 1, 0, 0, 0, 0, 0, 32512, 0, 0, 0, 1, 1, 1, 4, "main".encode('utf-8'), 4, "ROOT".encode('utf-8'), 1, "GEOM".encode(), 4, "main".encode('utf-8'), 1, 13, "character_mat".encode('utf-8'), 13, "character_mat".encode('utf-8'), 0, 216, 44, 226, 217)
    fout.write(nodePacked)


def WendWrite():
    wendStruct = struct.Struct('I4s')
    wendPacked = wendStruct.pack(0, 'WEND'.encode('utf-8'))
    fout.write(wendPacked)
    fout.write(b'\x1e\x84\x40\x2e')


HeadWrite()
GeomWrite()
NodeWrite()
WendWrite()

# Made in Visual Studio Code
# And Pycharm (A lil bit)
# Say hi to blacoiso for me!