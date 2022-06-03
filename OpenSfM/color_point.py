import json
import numpy as np
import pandas as pd
import os, sys


dirpath = sys.argv[1]


#1) get all labels

print("...loading all labels...")
ratio=float(sys.argv[2])

#bbox xyxy
def getLabel(fpath):
    f=open(fpath,'r+')
    lines=f.readlines()
    labels=[]

    for index,line in enumerate(lines):
        line=line.strip('\n')
        lineList=line.split(' ')

        cx = int(float(lineList[1]))
        cy = int(float(lineList[2]))
        width = int(float(lineList[3]) * ratio)
        height = int(float(lineList[4]) * ratio)

        left = int(cx-width/2)
        right = int(left+width)
        top = int(cy-height/2)
        bottom = int(top+height)

        label=[ left, right, top, bottom ]
        #print(label)
        labels.append(label)

    f.close()
    return labels


def getLabels(dirpath):
    files=os.listdir(dirpath)
    allLabels=dict()
    for fname in files:
        #print(fname)
        labels=getLabel(os.path.join(dirpath,fname))
        allLabels[fname.replace("txt", "jpg")]=labels

    return allLabels


labelPath = os.path.join(dirpath,'labels')
labelPath = os.path.abspath(labelPath)
allLabels = getLabels(labelPath)
#print("allLabels: ")
#print(allLabels)




#2)
#change colors in bbox
print("...changing colors(in bbox)...")


trackPath = os.path.join(dirpath,'tracks.csv')
trackPath = os.path.abspath(trackPath)
tracks_pd = pd.read_csv(trackPath, delimiter='\t', names=['image', 'trackId', 'id', 'x', 'y', 's', 'r', 'g', 'b', 'segmentation', 'instance'])


def pixel_to_normalized_coordinates(px_coord, size):
    inv_size = 1.0/np.max(size)
    return np.array([(px_coord[0]+0.5-size[0]/2.0)*inv_size, (px_coord[1]+0.5-size[1]/2.0)*inv_size])


with open(os.path.join(dirpath,'camera_models.json')) as f:
    cam_json = json.load(f)

size = [cam_json[list(cam_json)[0]]['width'], cam_json[list(cam_json)[0]]['height']]
trackIds=[]
redColor = [255,0,0]
for k, v in allLabels.items():
    tracks_shot = tracks_pd[tracks_pd['image']==k]
    #print("image: ", k)

    #한 이미지 내의 하나의 bbox에 대해서
    for index, bbox in enumerate(v):
        p1=pixel_to_normalized_coordinates([bbox[0],bbox[2]], size)
        p2=pixel_to_normalized_coordinates([bbox[1],bbox[3]], size)
        #print("     for bbox", index, " in image ", k, ", p1=", p1, "p2=", p2)
        inBbox = tracks_shot[(tracks_shot['x']>=p1[0]) & (tracks_shot['x']<=p2[0]) & (tracks_shot['y']>=p1[1]) & (tracks_shot['y']<=p2[1])]
        #print("     ", inBbox.shape[0], "are in the bbox ", index)

        #bbox 안에 있으면 색을 바꿔줌
        for i, row in inBbox.iterrows():
            trackId = row['trackId']

            tracks_pd.loc[i,'r'] = redColor[0]
            tracks_pd.loc[i,'g'] = redColor[1]
            tracks_pd.loc[i,'b'] = redColor[2]

            trackIds.append(trackId)
            print("Changing color to ", redColor," completed for the track id ", trackId, " in bbox", index, " in shot ", k)



uniqueTrackIds, count = np.unique(trackIds, return_counts = True)
#trackId가 같은 애들 지금 바꿔줌
print("...changing colors(same trackIds)... ")
for uti in uniqueTrackIds:
    tracks_pd.loc[(tracks_pd['trackId'] == uti), 'r'] = redColor[0]
    tracks_pd.loc[(tracks_pd['trackId'] == uti), 'g'] = redColor[1]
    tracks_pd.loc[(tracks_pd['trackId'] == uti), 'b'] = redColor[2]






#tracks.csv save
tracks_pd.to_csv(os.path.join(dirpath, 'tracks.csv'), sep='\t', index=False, header= None)
print("tracks.csv saved")





