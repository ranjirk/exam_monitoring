

class mouth :
	# def __init__(self, ref_dic, cur_dic):


	def mouth_opener(self, ref_dic, cur_dic) :
		self.ref_dic = ref_dic
		self.cur_dic = cur_dic
		
		self.ref_a = self.ref_dic['61'][1] 
		self.ref_b = self.ref_dic['62'][1]
		self.ref_c = self.ref_dic['63'][1]
		self.ref_x = self.ref_dic['67'][1]
		self.ref_y = self.ref_dic['66'][1]
		self.ref_z = self.ref_dic['65'][1]

		self.cur_a = self.cur_dic['61'][1] 
		self.cur_b = self.cur_dic['62'][1]
		self.cur_c = self.cur_dic['63'][1]
		self.cur_x = self.cur_dic['67'][1]
		self.cur_y = self.cur_dic['66'][1]
		self.cur_z = self.cur_dic['65'][1]

		self.ref_len_a2x = abs(self.ref_x - self.ref_a)
		self.ref_len_b2y = abs(self.ref_y - self.ref_b)
		self.ref_len_c2z = abs(self.ref_z - self.ref_c)

		self.cur_len_a2x = abs(self.cur_x - self.cur_a)
		self.cur_len_b2y = abs(self.cur_y - self.cur_b)
		self.cur_len_c2z = abs(self.cur_z - self.cur_c)

		self.ref_len_a2x = 1 if self.ref_len_a2x < 1 else self.ref_len_a2x
		self.ref_len_b2y = 1 if self.ref_len_b2y < 1 else self.ref_len_b2y
		self.ref_len_c2z = 1 if self.ref_len_c2z < 1 else self.ref_len_c2z

		if (self.cur_len_a2x == self.ref_len_a2x) or (self.ref_len_b2y == self.cur_len_b2y) or (self.ref_len_c2z == self.cur_len_c2z):
			return False
		else :
			self.A_to_X_per = self.perc(self.ref_len_a2x, self.cur_len_a2x)
			self.B_to_Y_per = self.perc(self.ref_len_b2y, self.cur_len_b2y)
			self.C_to_Z_per = self.perc(self.ref_len_c2z, self.cur_len_c2z)

			if (self.A_to_X_per or self.B_to_Y_per or self.C_to_Z_per) > 250 :
				return True
			else :
				return False

	def perc(self, a, b) :
		self.a, self.b = a, b
		self.change = (abs( self.a - self.b )/self.a)*100
		return self.change
