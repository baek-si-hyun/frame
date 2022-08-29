import cv2
import numpy as np
import sys
# 동영상 3개를 이어붙인다 생각하면됨
# 합성시킬 두 개의 영상 열기
cap1 = cv2.VideoCapture('video1.mp4')
cap2 = cv2.VideoCapture('video2.mp4')

if not cap1.isOpened() or not cap2.isOpened():
    sys.exit()

# 각 영상 프레임 수
frame_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap1.get(cv2.CAP_PROP_FPS)
# fps는 초당 프레임이니까 전환효과를 2초주고 싶으면 fps*2해주면 됨
# effect_frames = round(fps * 2)
effect_frames = round(fps)

delay = round(1000 / fps)

# 영상 가로 세로 설정
w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 비디오 코덱 설정
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

# 1번 영상 열기
for i in range(frame_cnt1 - effect_frames):
    ret1, frame1 = cap1.read()

    if not ret1:
        sys.exit()

    out.write(frame1)
    cv2.imshow('frame', frame1)
    cv2.waitKey(delay)

# 합성하기
for i in range(effect_frames):
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        sys.exit()

    dx = int((w / effect_frames) * i)

    frame = np.zeros((h, w, 3), dtype=np.uint8) # np.zeros = 0으로 가득찬 배열을 하나
    frame[:, 0:dx, :] = frame2[:, 0:dx, :]  # 0부터 dx까지는 영상2
    frame[:, dx:w, :] = frame1[:, dx:w, :]  # dx 부터 끝까지는 영상1

    # 프레임 저장
    out.write(frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(delay)

for i in range(effect_frames, frame_cnt2):
    ret2, frame2 = cap2.read()

    if not ret2:
        sys.exit()

    out.write(frame2)
    cv2.imshow('frame', frame2)
    cv2.waitKey(delay)
