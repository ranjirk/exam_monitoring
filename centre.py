import cv2, datetime, PIL, os, face_recognition, dlib, json
import face_features, mouth_opening, multipleface
from PIL import Image
from face_features import face_points
from mouth_opening import mouth
from multipleface import multi_face
from datetime import datetime

class features :

	def __init__(self, path) :
		self.path = path # ./record/user_id
		self.obj_face_points_2 = face_points()
		self.obj_multiF = multi_face()

		self.now = datetime.now()
		self.time_ = str(self.now.strftime("%Y_%m_%d_%H_%M_%S"))	

	def get_data(self):
		if os.path.isfile(f'{self.path}/reference.jpg') :
			if os.path.isfile(f'{self.path}/ref_dict.json') :
				self.image = cv2.imread(f'{self.path}/reference.jpg')
				with open(f'{self.path}/ref_dict.json') as self.f :
					self.ref_dict = json.load(self.f)
				return self.image, self.ref_dict
			else :
				self.logger('Reference image or Reference dictionary not found !!!')
				return False, False
		else :
			self.logger('Reference image or Reference dictionary not found !!!')
			return False, False


	def face_trk(self, cur_image, ref_dic):
		self.cur_image 	= cur_image 
		self.ref_dic 	= ref_dic
		self.cur_dic = self.obj_face_points_2.face_feature_points(self.cur_image)
		self.feature_dict = { 'left_right':False, 'up_down':False, 'tilt':False }
		if not self.cur_dic is False :
			self.feature_dict = self.obj_face_points_2.face_tracking(self.ref_dict, self.cur_dic)
			try :
				self.write_record(f'{self.path}/facial_feature/{self.time_}.txt', f'{str(self.feature_dict)} as {self.time_}.jpg ')
				self.save_image(self.cur_image, f'{self.path}/facial_feature/{self.time_}.jpg')
			except Exception as e :
				self.logger(f'{str(e)} {type(e)} in face_trk')
		return self.feature_dict

	def face_match(self, curr_image, ref_image) :
		self.curr_image = curr_image
		self.ref_image  = ref_image
		# self.b_e is biden_encoding, u_e is unknown_encoding
		self.b_e = face_recognition.face_encodings(self.ref_image)[0]
		self.u_e = face_recognition.face_encodings(self.curr_image)[0]
		self.results = face_recognition.compare_faces([self.b_e], self.u_e)
		if not self.results[0]:
			try :
				self.write_record(f'{self.path}/face_mismatching.txt', f'{str(self.time_)}.jpg')
				self.save_image(self.curr_image, f'{self.path}/Face_Mismatch/{str(self.time_)}.jpg')
			except Exception as e :
				self.logger(f'{str(e)} {type(e)} in face_match()')
			return False
		else :
			return True

	def mouth_open(self, cur_image, ref_dic) :
		self.cur_image 	= cur_image
		self.ref_dic 	= ref_dic
		self.cur_dic = self.obj_face_points_2.face_feature_points(self.cur_image)

		if not self.cur_dic is False :
			self.obj_mouth = mouth()
			self.result = self.obj_mouth.mouth_opener(self.ref_dic, self.cur_dic)
			if self.result :
				try :
					self.write_record(f'{self.path}/mouth_open.txt', f'{self.time_}.jpg')
					self.save_image(self.cur_image, f'{self.path}/mouth/{self.time_}.jpg')
				except Exception as e :
					self.logger(f'{str(e)} {type(e)} in mouth_open()')
				return 'open'
			else :
				return 'closed'

	def multi_f(self, prev_image, curr_image):
		self.prev_image = prev_image
		self.curr_image = curr_image
		self.res, self.noF = self.obj_multiF.face_case(self.prev_image, self.curr_image)
		if self.res is True :
			if self.noF[0] > 1 :
				try :
					self.write_record(f'{self.path}/multiple_face.txt', f'{self.time_}.jpg')
					self.save_image(self.curr_image, f'{self.path}/Multiple_Faces/{self.time_}_current.jpg')
					# self.save_image(self.prev_image, f'{self.path}/Multiple_Faces/{self.time_}_previous.jpg')
				except Exception as e :
					self.logger(f'{str(e)} {type(e)} at multi_f')
				return True, 'multiple faces'
			else :
				return True, 'multiple faces'
		elif not self.res :
			if self.noF == 'single' : # single face
				return False, 'single face'
			elif self.noF == 'no' : # No face
				try :
					self.write_record(f'{self.path}/no_face.txt', f'{self.time_}.jpg')
					self.save_image(self.curr_image, f'{self.path}/No_Face/{self.time_}_current.jpg')
					# self.save_image(self.prev_image, f'{self.path}/No_Face/{self.time_}_previous.jpg')
				except Exception as e :
					self.logger(f'{str(e)} {type(e)} at multi_f')
				return True, 'no face'
		else :
			return True, False
			
	def save_image(self, frame, name):
		self.frame 	= frame
		self.name 	= name
		self.img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
		self.img_pil = Image.fromarray(self.img)
		self.img_pil.save(self.name)

	def write_record(self, filename, content):
		self.record_name = filename
		self.content = content + '\n'
		self.f = open(self.record_name, 'a+', encoding='utf-8')
		self.f.write(self.content)
		self.f.close()

	def logger(self, text) :
		self.text = text
		with open(f'./{self.path}/Error_Log.txt', 'a+', encoding='utf-8') as self.f :
			self.f.write(f'\n | {self.time_} | {self.text} |\n')

	def folder_creation(self) :

		try :
			if not os.path.exists(f'{self.path}'):
				os.makedirs(f'{self.path}')

			if not os.path.exists(f'{self.path}/Face_Mismatch'):
				os.makedirs(f'{self.path}/Face_Mismatch')

			if not os.path.exists(f'{self.path}/Multiple_Faces'):
				os.makedirs(f'{self.path}/Multiple_Faces')

			if not os.path.exists(f'{self.path}/No_Face'):
				os.makedirs(f'{self.path}/No_Face')

			if not os.path.exists(f'{self.path}/facial_feature'):
				os.makedirs(f'{self.path}/facial_feature')

			if not os.path.exists(f'{self.path}/facial_features/marked'):
				os.makedirs(f'{self.path}/facial_features/marked')

			if not os.path.exists(f'{self.path}/mouth'):
				os.makedirs(f'{self.path}/mouth')

		except Exception as e :
			self.logger( str( str(e), type(e) ) )

