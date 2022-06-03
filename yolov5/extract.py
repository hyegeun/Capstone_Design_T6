import cv2
import os

input_video = os.listdir('video')
filepath = 'video/' + input_video[0]
video = cv2.VideoCapture(filepath) #'' 사이에 사용할 비디오 파일의 경로 및 이름을 넣어주도록 함

if not video.isOpened():
    print("Could not Open :", filepath)
    exit(0)
    
half_fps = int(0.5*(video.get(cv2.CAP_PROP_FPS)))
print('half fps: ', half_fps)

#프레임을 저장할 디렉토리를 생성
try:
    if not os.path.exists('video_frame'):
        os.makedirs('video_frame')
except OSError:
    print ('Error: Creating directory. ' +  filepath[:-4])
    
cnt = 0

while(video.isOpened()):
    ret, image = video.read()
    if not ret:
        break 
    if(int(video.get(1)) % half_fps == 0): #앞서 불러온 fps 값을 사용하여 1초마다 추출
        cv2.imwrite("video_frame/%.5d.jpg" %(cnt), image)
        print('Saved frame number :', str(int(video.get(1))))
        cnt += 1
        
video.release()
