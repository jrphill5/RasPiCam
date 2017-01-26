import os, io, sys, picamera
from select import select
from datetime import datetime

# Number of seconds to record when key pressed
rectime = 10

filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
print('Files will be stored in %s' % filepath)

with picamera.PiCamera() as camera:
	# 1 1920x1080 @  30 fps, Partial FoV, No Bins
	# 2 3280x2464 @  -- fps, Full FoV,    No Bins
	# 3 3280x2464 @  -- fps, Full FoV,    No Bins
	# 4 1640x1232 @  30 fps, Full FoV,    2x2 Bins
	# 5 1640x 922 @  41 fps, Full FoV,    2x2 Bins
	# 6 1280x 720 @  68 fps, Partial FoV, 2x2 Bins
	# 7  640x 480 @ 120 fps, Partial FoV, 2x2 Bins
	camera.resolution = (1640,922)
	camera.framerate = 41

	stream = picamera.PiCameraCircularIO(camera, seconds=rectime)
	camera.start_preview()
	camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
	camera.start_recording(stream, format='h264')

	print('Hit <w> to write the stream to disk')
	print('Hit <q> to quit the program')

	while camera.recording:
		while True:
			camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[0:-3]
			delayTime = 0
			camera.wait_recording(delayTime)
			r, w, x = select([sys.stdin], [], [], delayTime)
			if r: break

		c = input()
		if c == 'q':
			print('Quitting program!')
			camera.stop_recording()
			camera.stop_preview()
		elif c == 'w':
			filename = datetime.now().strftime('%Y%m%d-%H%M%S.h264')
			sys.stdout.write('Writing last %d seconds to %s ... ' % (rectime, filename))
			# Lock the stream, so the camera doesn't mutate it
			with stream.lock:
				pts = []
				for frame in stream.frames:
					pts.append(frame.timestamp)
				ib = 0
				for i,v in enumerate(pts):
					if v is not None:
						ib = i
						break
				ie = 0
				for i,v in enumerate(reversed(pts)):
					if v is not None:
						ie = i
						break
				fps = 1.0e6*(len(pts)-1-ie - ib)/float(pts[len(pts)-1-ie] - pts[ib])

				sys.stdout.write("%.2f fps ... " % fps)
				# Seek to first header frame in stream
				for frame in stream.frames:
					if frame.header:
						stream.seek(frame.position)
						break

				# Write remainder of stream to file
				if not os.path.exists(filepath): os.makedirs(filepath)
				with io.open(os.path.join(filepath, filename), 'wb') as output:
					while True:
						buf = stream.read1()
						if not buf: break
						output.write(buf)
				print('done!')
		else:
			print('Invalid key <%s> detected!' % c)
