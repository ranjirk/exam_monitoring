import cv2, dlib

class multi_face() :

	def __init__(self) :
		self.detector  = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
		self.feature_points_dict = {}		

	def face_points(self, image) :
		self.image = image 
		self.lis_d, self.zero_67_dict = [], {}
		self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
		self.faces = self.detector(self.gray)
		if len(self.faces) >= 1 :
			for self.face in self.faces :
				self.x1, self.y1, self.x2, self.y2 = self.face.left(), self.face.top(), self.face.right(), self.face.bottom()
				self.landmarks = self.predictor(image = self.gray, box = self.face)
				for self.n in range(0, 68) :
					x = self.landmarks.part(self.n).x
					y = self.landmarks.part(self.n).y
					self.zero_67_dict[f'{self.n}'] = (x, y)
				self.lis_d.append(self.zero_67_dict)
		return self.lis_d

	def face_case(self, prev_img, cur_img) :
		self.prev_img, self.cur_img = prev_img, cur_img
		
		self.p_lis = self.face_points(self.prev_img)
		self.c_lis = self.face_points(self.cur_img)
		# print('len of prev list and cur list faces : ', len(self.p_lis), len(self.c_lis))
		# self.p_lis and self.c_lis have [ {'0':(x,y),..,'67':(x,y)}, {'0':(x,y),..,'67':(x,y)} ]

		if (len(self.p_lis) == 1) and (len(self.c_lis) == 1) :  # Single face
			return False, 'single'
		elif (len(self.p_lis) == 0) or (len(self.c_lis) == 0) : # No face found
			return False, 'no'
		else :
			self.blink_yes, self.blink_no = 0, 0
			for self.pf_dic, self.i in enumerate(self.p_lis, start=0):
				for self.cf_dic, self.j in enumerate(self.c_lis, start=0) :

					self.x_p = self.pf_dic['0'][0]
					self.y_p = self.pf_dic['0'][1]

					self.x_c = self.cf_dic['0'][0]
					self.y_c = self.cf_dic['0'][1]

					if self.x_c in range(self.x_p - 10, self.x_p + 10) :
						if self.y_c in range(self.y_p - 10, self.y_p + 10) :

							self.res = self.blinker(self.pf_dic, self.cf_dic) 
							if self.res :
								self.blink_yes += 1
							else :
								self.blink_no += 1
							break
			return True, (self.blink_yes, self.blink_no)

	def blinker(self, p_dic, c_dic) :
		self.p_dic, self.c_dic = p_dic, c_dic

		self.p_len_37_41 = self.p_dic['41'][1] - self.p_dic['37'][1] # Eye 1
		self.c_len_37_41 = self.c_dic['41'][1] - self.c_dic['37'][1]

		self.p_len_38_40 = self.p_dic['40'][1] - self.p_dic['38'][1]
		self.d_len_38_40 = self.d_dic['40'][1] - self.d_dic['38'][1] # _____

		self.p_len_43_47 = self.p_dic['47'][1] - self.p_dic['43'][1] # Eye 2
		self.c_len_43_47 = self.c_dic['47'][1] - self.c_dic['43'][1]

		self.p_len_44_46 = self.p_dic['46'][1] - self.p_dic['44'][1]
		self.c_len_44_46 = self.c_dic['46'][1] - self.c_dic['44'][1] # _____

		self.p_lis = [self.p_len_37_41, self.p_len_38_40, self.p_len_43_47, self.p_len_44_46]
		self.c_lis = [self.c_len_37_41, self.c_len_38_40, self.c_len_43_47, self.c_len_44_46]

		if (0 in self.p_lis) and (0 not in self.c_lis) :
			return True
		elif (0 not in self.p_lis) and (0 in self.c_lis) :
			return True
		elif (self.p_lis[0] == self.c_lis[0]) or (self.p_lis[1] == self.c_lis[1]) or (self.p_lis[2] == self.c_lis[2]) or (self.p_lis[3] == self.c_lis[3]) :
			return False
		else :
			self.per_change_a1 = (abs(self.p_len_37_41 - self.c_len_37_41)/self.p_len_37_41) * 100
			self.per_change_a2 = (abs(self.p_len_38_40 - self.c_len_38_40)/self.p_len_38_40) * 100
			self.per_change_b1 = (abs(self.p_len_43_47 - self.c_len_43_47)/self.p_len_43_47) * 100			
			self.per_change_b2 = (abs(self.p_len_44_46 - self.c_len_44_46)/self.p_len_44_46) * 100

			if (self.per_change_a1 or self.per_change_a1 or self.per_change_a1 or self.per_change_a1) > 80 :
				return True

	def per_change(self, a, b) :
		self.a, self.b = a, b
		self.change = (abs(self.a - self.b)/self.a) * 100
		return self.change
