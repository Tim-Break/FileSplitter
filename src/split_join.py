import os, sys

basics = {"B":1, "KB":1_024, "MB":1_048_576, "GB":1_073_741_824}
lenData = 0
maxIndex = 0


def indexReader(path: str):
    with open(path, 'rb') as file:
        index = file.read(1)
        maxIndex_ = file.read(1)
        if index[0] > maxIndex_[0]:
            return
        if index[0] > maxIndex: maxIndex = index
        elif maxIndex == maxIndex_: return
        return index


def nameReader(path: str):
    with open(path, 'rb') as file:
        return file.read(254).decode("ascii").rstrip(" ")


def split(path: str, outPath: str, splitSize: list[int, str], openInExplorer: bool = True):
    path = os.path.realpath(path)
    outPath = os.path.realpath(outPath)
    splitSize = splitSize[0] * basics[splitSize[1]]
    name = os.path.basename(path)
    nameClamped = (name[abs(254-len(name)):] if len(name) > 254 else name + " "*(254-len(name))).encode("ascii")
    size = os.path.getsize(path)
    pCount = size // splitSize + (0 if size % splitSize > 0 else -1)
    print(pCount)
    if pCount + 1 > 32: return ("With this file size and chunk size, there are too many of them (more than 32).", 1)
    
    count = 0
    with open(path, 'rb') as file:
        while size > 0:
            with open(os.path.join(outPath, f"{name}-{count}.split"), 'wb') as partFile:
                partFile.write(bytes([count, pCount])+nameClamped)
                partFileSize = 256
                while partFileSize < splitSize:
                    toEnd = splitSize - partFileSize
                    addSize = basics["MB"]
                    if toEnd < basics["MB"] and toEnd >= basics["KB"]: addSize = basics["KB"]
                    elif toEnd < basics["KB"]: addSize = basics["B"]

                    data = file.read(addSize)
                    if len(data) == 0: break
                    partFile.write(data)
                    partFileSize += addSize
                size -= partFileSize
            count += 1
    
    if openInExplorer: os.system(f"explorer /select,\"{os.path.join(outPath, f'{name}-0.split')}\"")
    
    return ("Done!", 0)


def join(parts: list[str], outPath: str, openInExplorer: bool = True):
    global lenData
    outPath = os.path.realpath(outPath)
    parts = list(map(os.path.realpath, parts))
    try: lenData = len(parts)
    except: return ("You selected not all parts!", 1)
    names = set([nameReader(p) for p in parts])
    if len(names) > 1: return ("These chunks do not form a single file.", 2)
    del names
    outPath = os.path.join(outPath, nameReader(parts[0])[1:])
    parts.sort(key=indexReader)

    with open(outPath, 'wb') as file:
        for path in parts:
            size = os.path.getsize(path)
            with open(path, 'rb') as partFile:
                partFile.read(256)
                while size >= 0:
                    file.write(partFile.read(basics["MB"]))
                    size-=basics["MB"]
    
    lenData = 0
    if openInExplorer: os.system(f"explorer /select,\"{outPath}\"")

    return ("Done!", 0)
