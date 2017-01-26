import cv2

fps = 41.11
per = 1.0/fps

cap = cv2.VideoCapture("images/20170124-113059.h264")

play = True
while True:
	if play:
		ret, frame = cap.read()
	
		if not ret: break
	
		cv2.imshow('video', frame)
	
		i = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
		print('Frame #%d @ %.3f' % (i, i*per))
		
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'): break
	elif key == ord(' '): play = not play

cap.release()
cv2.destroyAllWindows()
