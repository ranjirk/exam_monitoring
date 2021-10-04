import cv2, centre, multipleface
from centre import features
from multipleface import multi_face
import json

class live_feed :

	def __init__(self, cur_image, user_id):
		self.cur_image, self.user_id = cur_image, user_id
		self.obj_fea_2 = features(f'./records/{self.user_id}')
		self.result_dic = {'reference data':False, 'multiple Face':False, \
		'face match':False, 'face track':False, 'mouth open':False}

	def capture(self):
		self.obj_fea_2.folder_creation()
		self.ref_image, self.ref_dict = self.obj_fea_2.get_data()

		if (self.ref_dict is not False) and (self.ref_image.shape[0]>20) :
			self.result_dic['reference data'] = True
			self.result_dic['multiple Face'] = self.obj_fea_2.multi_f(self.ref_image, self.cur_image)
			if not self.result_dic['multiple Face'][0] :
				print('')
				# self.result_dic['face match'] = self.obj_fea_2.face_match(self.cur_image, self.ref_image)
				self.result_dic['face track'] = self.obj_fea_2.face_trk(self.cur_image, self.ref_dict)
				self.result_dic['mouth open'] = self.obj_fea_2.mouth_open(self.cur_image, self.ref_dict)

		return self.result_dic

# uncomment last three to test without api,\
# make sure you have an ref_image and ref_dict.json before running this file
# As shown below you'll need a current image to run this program
# img = cv2.imread('./images/mouth/slight_3.jpg')
# obj = live_feed(img, 'Ranjith')
# print('\n\n', obj.capture())