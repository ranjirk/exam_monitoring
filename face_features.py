import cv2, dlib, datetime, math
from datetime import datetime

class face_points :
	def __init__(self) :
		self.detector  = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
		# self.obj_feat = features()

	def face_feature_points(self, image) :
		self.image = image
		self.larg, self.temp_dic, self.feature_ = 0, {}, []

		self.gray = cv2.cvtColor(src = self.image, code = cv2.COLOR_BGR2GRAY)
		self.faces = self.detector(self.gray)
		for self.face in self.faces :
			self.x1, self.y1, self.x2, self.y2 = self.face.left(), self.face.top(), self.face.right(), self.face.bottom()
			if (self.x2-self.x1) > self.larg :
				self.landmarks = self.predictor(image = self.gray, box = self.face)
				for self.n in range(0, 68) :
					x = self.landmarks.part(self.n).x
					y = self.landmarks.part(self.n).y
					self.temp_dic[f'{self.n}'] = (x, y)
					# self.featured = cv2.circle(self.image, (x, y) , 1, (0, 255, 0) ,2)
				self.feature_.append(self.temp_dic)
		if len(self.feature_[-1]) == 68 :
			return self.feature_[-1]
		else :
			return False

	def face_tracking(self, ref_dic, cur_dic) :
		self.ref_dic 	= ref_dic
		self.cur_dic 	= cur_dic

		self.feature_dict = { 'left_right':False, 'up_down':False, 'tilt':False }
		self.L_R_result = self.left_right_turn(self.ref_dic, self.cur_dic)
		self.feature_dict['left_right'] = self.L_R_result

		self.U_D_result = self.up_down(self.ref_dic, self.cur_dic)
		self.feature_dict['up_down'] 	= self.U_D_result

		self.tilt_result = self.tilt(self.ref_dic, self.cur_dic)
		self.feature_dict['tilt'] 		= self.tilt_result # for extreme angle value is true or just the angle 
		return self.feature_dict


	def left_right_turn(self, ref_dict, cur_dict) :
		# returns true is left/right turn is detected
		self.ref_dict, self.cur_dict, self.result = ref_dict, cur_dict, False
		self.ref_list 	= self.eyebrow_jawline_nosepoint(self.ref_dict)
		self.cur_list 	= self.eyebrow_jawline_nosepoint(self.cur_dict)
		self.result 	= self.perc_calc(self.ref_list, self.cur_list)
		return 'detected' if self.result else 'not detected'

	def up_down(self, ref_dict, cur_dict) :
		self.ref_dict, self.cur_dict = ref_dict, cur_dict
		self.down_res, self.up_res = False, False
		self.down_res = self.down_check(self.ref_dict, self.cur_dict)
		self.up_res = self.up_check(self.ref_dict, self.cur_dict)
		return 'detected' if (self.up_res or self.down_res) else 'not detected'

	def tilt(self, ref_dic, cur_dic): 									      
		self.ref_dic, self.cur_dic = ref_dic, cur_dic		
		if self.cur_dic['0'][0] > self.cur_dic['16'][0] :
			return True
		else :
			self.ref_a = self.ref_dic['16']
			self.ref_b = self.ref_dic['0']
			self.ref_c = (self.ref_dic['16'][0], self.ref_dic['0'][1])
			self.cur_a = self.cur_dic['16']
			self.cur_b = self.cur_dic['0']
			self.cur_c = (self.cur_dic['16'][0], self.cur_dic['0'][1])

			# print('ref three points ', self.ref_a, self.ref_b, self.ref_c)
			# print('cur three points ', self.cur_a, self.cur_b, self.cur_c)
			self.angle_ref = self.getAngle( self.ref_a, self.ref_b, self.ref_c )
			self.angle_cur = self.getAngle( self.cur_a, self.cur_b, self.cur_c )
			# print('ref angle ', self.angle_ref)
			# print('cur angle ', self.angle_cur)
			return int(self.angle_cur)
			# if abs(self.angle_ref - self.angle_cur) > 15 :
			# 	return True
			# else :
			# 	return False
	# ___________________________________________________________________________________________ 
	def eyebrow_jawline_nosepoint(self, dic) :							 # Left Right Calculation
		self.dic = dic
		self.len_1 = self.dic['17'][0] - self.dic['0'][0]
		self.len_2 = self.dic['16'][0] - self.dic['26'][0]
		self.len_3 = self.dic['30'][0] - self.dic['1'][0]
		self.len_4 = self.dic['15'][0] - self.dic['30'][0]
		return self.len_1, self.len_2, self.len_3, self.len_4

	def perc_calc(self, ref, curr) :
		self.ref_len_1, self.ref_len_2, self.ref_len_3, self.ref_len_4 = ref
		self.cur_len_1, self.cur_len_2, self.cur_len_3, self.cur_len_4 = curr

		self.per_ch_1 = (abs(self.ref_len_1 - self.cur_len_1)/self.ref_len_1)*100
		self.per_ch_2 = (abs(self.ref_len_2 - self.cur_len_2)/self.ref_len_2)*100
		self.per_ch_3 = (abs(self.ref_len_3 - self.cur_len_3)/self.ref_len_3)*100
		self.per_ch_4 = (abs(self.ref_len_4 - self.cur_len_4)/self.ref_len_4)*100

		if ( (self.per_ch_1>50) or (self.per_ch_2>50)) and (self.per_ch_3 > 25 ) and (self.per_ch_4 > 25 ) :
			# self.content = f'\
			# Dist bet [0]  to [17] in ref img {self.ref_len_1}, cur img {self.cur_len_1}, % change = {self.per_ch_1}\n\
			# Dist bet [26] to [16] in ref img {self.ref_len_2}, cur img {self.cur_len_2}, % change = {self.per_ch_2}\n\
			# Dist bet [1]  to [15] in ref img {self.ref_len_3}, cur img {self.cur_len_3}, % change = {self.per_ch_3}\n\
			# Dist bet [30] to [15] in ref img {self.ref_len_4}, cur img {self.cur_len_4}, % change = {self.per_ch_4}\n'
			# self.obj_feat.write_record(f'./{self.user_id}/facial_features/left_right/{self.count}.txt', self.content)
			return True
		else :
			return False
	# ___________________________________________________________________________________________

	# ___________________________________________________________________________________________
	def down_check(self, ref_dic, cur_dic) : 							  # Face Down Calculation
		self.ref_dic, self.cur_dic = ref_dic, cur_dic
		self.res_1, self.res_2 = False, False
		self.res_1 = self.down_check_absolute( [ 
			self.ref_dic['0'][1], self.ref_dic['17'][1], self.ref_dic['16'][1], self.ref_dic['26'][1] ], \
			[ self.cur_dic['0'][1], self.cur_dic['17'][1], self.cur_dic['16'][1], self.cur_dic['26'][1] ] )

		if self.res_1 :
			return True
		else :
			self.res_2 = self.down_check_nose( (self.ref_dic['27'],self.ref_dic['30']), \
				(self.cur_dic['27'], self.cur_dic['30']) )
			if self.res_2 :
				return True
			else :
				return False

	def down_check_nose(self, ref_dic_27_nd_30, cur_dic_27_nd_30) :
		# If nose distance increases above 26% then there is a down turning activity. Nose Length 30, 27.
		# ref_dic['27'], ref_dic['30'] as ref_dic_27_nd_30 
		# cur_dic['27'], cur_dic['30'] as cur_dic_27_nd_30
		self.ref_dic_27, self.ref_dic_30 = ref_dic_27_nd_30
		self.cur_dic_27, self.cur_dic_30 = cur_dic_27_nd_30
		self.ref_length_nose = self.ref_dic_30[1] - self.ref_dic_27[1] 
		self.cur_length_nose = self.cur_dic_30[1] - self.cur_dic_27[1]
		self.per_change = (abs(self.ref_length_nose - self.cur_length_nose)/self.ref_length_nose)*100
		if self.per_change > 26 :
			return True
		else :
			return False

	def down_check_absolute(self, ref_dic_0_17_16_26, cur_dic_0_17_16_26) :
		# if y axis of ref_dic['0'] > y axis of ref_dic['17'] and yaxis of cur_dic['0'] < yaxis of cur_dic['17']
		# [ ref_dic['0'][1], ref_dic['17'][1], ref_dic['16'][1], ref_dic['26'][1] ] as ref_dic_0_17_16_26
		# [ cur_dic['0'][1], cur_dic['17'][1], cur_dic['16'][1], cur_dic['26'][1] ] as cur_dic_0_17_16_26
		self.ref_dic_0_1, self.ref_dic_17_1, self.ref_dic_16_1, self.ref_dic_26_1 = ref_dic_0_17_16_26
		self.cur_dic_0_1, self.cur_dic_17_1, self.cur_dic_16_1, self.cur_dic_26_1 = cur_dic_0_17_16_26
		self.flg_1, self.flg_2 = False, False
		if (self.ref_dic_0_1 > self.ref_dic_17_1) and  (self.cur_dic_0_1 < self.cur_dic_17_1) :
			self.flg_1 = True
		if (self.ref_dic_16_1 > self.ref_dic_26_1) and  (self.cur_dic_16_1 < self.cur_dic_26_1) :
			self.flg_2 = True
		if (self.flg_1 == True) and (self.flg_2 == True) :
			return True
		else :
			return False

	# ___________________________________________________________________________________________

	# ___________________________________________________________________________________________
	def up_check(self, ref_dic, cur_dic) :								    # Face Up Calculation
		self.ref_dic, self.cur_dic = ref_dic, cur_dic
		self.res_1 = self.nose_len([self.ref_dic['27'][1], self.ref_dic['30'][1], self.cur_dic['27'][1], self.cur_dic['30'][1]])
		self.res_2 = self.nose_tip([self.cur_dic['0'][1], self.cur_dic['16'][1], self.cur_dic['30'][1]])
		if self.res_1 :
			return True
		elif self.res_2 :
			return True
		else :
			return False

	def nose_len(self, val) :
		self.ref_n_top, self.ref_n_bottom, self.cur_n_top, self.cur_n_bottom = val
		self.ref_len = self.ref_n_bottom - self.ref_n_top
		self.cur_len = self.cur_n_bottom - self.cur_n_top
		self.per_change =  (abs(self.ref_len - self.cur_len) / self.ref_len ) * 100
		if self.per_change > 50 :
			return True
		else :
			return False

	def nose_tip(self, val) :
		# cur_dic['0'][1], cur_dic['16'][1], cur_dic['30'][1] as val
		self.vall = val
		if (self.vall[0] > self.vall[2]) and (self.vall[1] > self.vall[2]) :
			return True
		else :
			return False
	# ___________________________________________________________________________________________
	def getAngle(self, a, b, c) :
		# b is the middle point, a,b,c can be 3 lists or 3 tuples, func returns float
		self.a, self.b, self.c = a, b, c
		self.ang = math.degrees(math.atan2(self.c[1]-self.b[1], self.c[0]-self.b[0]) - math.atan2(self.a[1]-self.b[1], self.a[0]-self.b[0]))
		# return self.ang + 360 if self.ang < 0 else self.ang
		# if self.ang < 0 :
		# 	return self.ang + 360
		# else :
		# 	return self.ang
		return self.ang

	# ___________________________________________________________________________________________

