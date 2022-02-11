import ezdxf
import sys
import numpy as np

from os import listdir
from os.path import isfile, join
"""
todo:

figure out some kind of notation system that represents the head unqiuely (whether that be in the form of an array or a string or something)
"""
def normListLength(inList):
    biggest = 0
    for i in inList:
        if i > biggest:
            biggest = i
    tempList = inList
    outList = []
    for j,i in enumerate(tempList):
        # make all lists 13 long
        if len(i) <biggest:
            for n in range(biggest-len(i)):
                outList[j].append(0)
    return tempList
def findGoodFiles(subFolderName):
    # get all files in sub folder
    unfilteredFiles = [f for f in listdir(subFolderName) if isfile(join(subFolderName, f))]
    # make new list only keeping the dxf files
    filteredFiles = []
    for j,i in enumerate(unfilteredFiles):
        if i[-3:] == 'dxf':
            filteredFiles.append(i)
    # add the sub folder
    for j,f in enumerate(filteredFiles):
        filteredFiles[j] = subFolderName+'/' + f
    return filteredFiles
            

def docPrepper(subFolderName):
    # break all docs in a folder and reshapes them
    # Get all docs
    fPathList = findGoodFiles(subFolderName)
    # store all results in a dictionary with the file name as a key
    megaDict = {}
    for i in fPathList:
        megaDict.update({i[len(subFolderName)+1:-5]:docLoader(i)})
    # resize all the items to a uniform length and store them in a seperate list
    items = normListLength(megaDict.items())
    # resize all the keys to a unitfom length and store them in a seperate list
    keys = normListLength([[chr(j) for j in i] for i in megaDict.keys()])
    # use keys to contruct the input for the nn
    X = np.reshape(keys,[len(keys),len(keys[0]),1])
    Y = np.reshape(items,[len(items),len(items[0]),1])
    return X,Y
def docLoader(fName):
    # attempt to load DXF
    try: 
        doc = ezdxf.readfile(fName)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)
    return docBreaker(doc)
def docBreaker(doc):
    # put all objects i care about into a list with list of info on those objects 

    # layers to get objects from
    msp = doc.modelspace()
    goodNoodleLayers = ['Visible','Visible Narrow','Dimensions']
    goodNoodles = []
    for i in msp:
        # make a list of all objects on acceptable layers
        if (i.dxf.layer in goodNoodleLayers):
            # break that list down into each object's values (0 isnt used because of the way objects are extened in length)
            if i.dxftype() == 'DIMENSION':
                goodNoodles.append([
                    1,
                    goodNoodleLayers.index(i.dxf.layer),
                    i.dxf.defpoint.x,i.dxf.defpoint.y,i.dxf.defpoint.z,
                    i.dxf.defpoint2.x,i.dxf.defpoint2.y,i.dxf.defpoint2.z,
                    i.dxf.text_midpoint.x,i.dxf.text_midpoint.y,i.dxf.text_midpoint.z,
                    i.dxf.angle,
                    [chr(j) for j in i.dxf.text]])
            elif i.dxftype() == 'LINE':
                goodNoodles.append([
                    2,
                    goodNoodleLayers.index(i.dxf.layer),
                    i.dxf.start.x,i.dxf.start.y,i.dxf.start.z,
                    i.dxf.end.x,i.dxf.end.y,i.dxf.end.z])
            elif i.dxftype() == 'ARC':
                goodNoodles.append([
                    3,
                    goodNoodleLayers.index(i.dxf.layer),
                    i.dxf.center.x,i.dxf.center.y,i.dxf.center.z,
                    i.dxf.radius,
                    i.dxf.start_angle,
                    i.dxf.end_angle])
            elif i.dxftype() == 'CIRCLE':
                goodNoodles.append([
                    4,
                    goodNoodleLayers.index(i.dxf.layer),
                    i.dxf.center.x,i.dxf.center.y,i.dxf.center.z,
                    i.dxf.radius])

    goodNoodles = normListLength(goodNoodles)
    masterNoodles = []
    for i in goodNoodles:
    # make a strr out of the list (object length is 13 items)]
        for j in i:
            masterNoodles.append(j)
    return masterNoodles
def docMaker(nfname,masterNoodles):
    # create a dxf from an list
    # make a new document
    doc = ezdxf.new("R2010",setup=True)
    # get modelspace
    msp = doc.modelspace()
    # rebuild goodNoodles
    goodNoodles = []
    for i in range(len(masterNoodles)/13):
        tempNoodles = []
        for j in range(13):
            tempNoodles.append(masterNoodles[(i*13)+j])
        goodNoodles.append(tempNoodles)
    for i in goodNoodles:
        # for each entry in the list make that object
        if i[0] == 1:
            msp.add_linear_dim(
                base=(i[8],i[9],i[10]),
                p1 = (i[2],i[3],i[4]),
                p2 = (i[5],i[6],i[7]),
                angle = i[11],
                text = i[12]
            )
        elif i[0] == 2:
            msp.add_line(
                start = (i[2],i[3],i[4]),
                end = (i[5],i[6],i[7])
            )
        elif i[0] == 3:
            msp.add_arc(
                center = (i[2],i[3],i[4]),
                radius=(i[5]),
                start_angle=(i[6]),
                end_angle=(i[7])
            )
        elif i[0] == 4:
            msp.add_circle(
                center = (i[2],i[3],i[4]),
                radius=(i[5])
            )
    doc.saveas(nfname)
def cleanFromNN(masternoodle,decim):
    # round numbers to make them nicer going into docMaker
    # decim decides how many decimals to round to
    pass
