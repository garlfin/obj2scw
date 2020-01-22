import struct
import sys
import os

pathtoobj = str(sys.argv[1])
print(str(sys.argv[1]))
def crap():
    obj = open(pathtoobj, 'r')
    vn = []
    vt = []
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
                f.append(line.split()[x + 1].split('/')[0])  # v
                f.append(line.split()[x + 1].split('/')[2])  # vn
                f.append(line.split()[x + 1].split('/')[1])  # vt

    vt[1::2] = [x*-1+1 for x in vt[1::2]]
    print(v)
    in_file = open("nita_bear_geo.scw", "rb")
    geoPacked = in_file.read(55)
    size = int(29125+len(v)/3*6+len(vn)/3*6+len(vt)/2*4+len(f)/9*18)

    print(29125+len(v)/3*6+len(vn)/3*6+len(vt)/2*4+len(f)/9*18)
    print(len(v)/3*6)
    print(len(vn)/3*6)
    print(len(vt)/2*4)
    print(len(f)/9*18)
    print(size)
    in_file.seek(35769)
    geoPacked += struct.pack('>i4sh4sh6s',size, 'GEOM'.encode('utf-8'), 4, 'main'.encode('utf-8'), 6, 'geoGrp'.encode('utf-8'))

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
    scalevt = max(max(vt), abs(min(vt)))
    geoPacked += struct.pack('>HfI', 2, scalevt, int(len(vt) / 2))
    for x in vt:
        geoPacked += struct.pack('>h', int(x * 32512 / scalevt))
    data2 = in_file.read(29045)
    geoPacked += data2
    geoPacked  += struct.pack('>HH',int(len(f)/9), 770)  # testing time!
    for x in f:
        geoPacked += struct.pack('>h', int(x)-1)# i fixed it! Ok

    geoPacked += struct.pack('I',62384957 )
    in_file.seek(142834)

    data3 = in_file.read()
    geoPacked += data3
    in_file.close()
    out_file = open(os.path.splitext(os.path.basename(pathtoobj))[0]+".scw", "wb")
    out_file.write(geoPacked)
    out_file.close()

crap()


