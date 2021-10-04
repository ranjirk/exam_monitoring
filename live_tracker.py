import cv2, dlib, imutils


class face_points :
	def __init__(self) :
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
		self.feature_points_dict = {}

	def feature_points(self, image):
		self.image, self.featured = image, image
		self.gray = cv2.cvtColor(src = self.image, code = cv2.COLOR_BGR2GRAY)
		self.faces = self.detector(self.gray)
		self.flag = False
		for self.face in self.faces :
			self.x1, self.y1, self.x2, self.y2 = self.face.left(), self.face.top(), self.face.right(), self.face.bottom()
			self.landmarks = self.predictor(image = self.gray, box = self.face)
			for self.n in range(0, 68) :
				x = self.landmarks.part(self.n).x
				y = self.landmarks.part(self.n).y
				self.featured = cv2.circle(self.image, (x, y) , 1, (0, 255, 0) ,2)
			self.flag = True
				# self.feature_points_dict[f'{self.n}'] = (x, y)
			# break
		return self.featured, self.flag

	def feed(self) :
		self.count = 0
		self.cam = cv2.VideoCapture(0)
		self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
		self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

		while (True) :
			self.ret, self.frame = self.cam.read()
			self.frame = cv2.flip(self.frame, 1)
			# print(self.frame.shape[0], self.frame.shape[1])
			# print(self.frame.shape[0], self.frame.shape[1]) # 640 480
			# self.frame = cv2.resize(self.frame, (1280, 960))
			# print(self.frame.shape[0], self.frame.shape[1])			
			if self.count%5 == 0 :
				self.processed, self.flag = self.feature_points(self.frame)
				if self.flag :
					cv2.imshow( "video output", self.processed)
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break
			self.count += 1
		self.cam.release()
		cv2.destroyAllWindows()

obj = face_points()
obj.feed()



