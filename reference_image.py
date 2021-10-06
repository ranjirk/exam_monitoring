import cv2, datetime, json
import centre, multipleface, face_features
from centre import features
from multipleface import multi_face
from face_features import face_points
from datetime import datetime


class snapshot :

	def __init__(self, ref_image, user_id):
		self.ref_image, self.user_id = ref_image, f'./records/{user_id}'
		self.now = datetime.now()
		self.time = self.now.strftime("%Y_%m_%d___%H:%M:%S")

		self.obj_fea_1 = features(f'{self.user_id}')
		self.multi_f = multi_face()
		self.obj_face_points_1 = face_points()

	def capture(self):
		print(self.ref_image.shape)
		try :
			if self.ref_image is not False :
				pass
			else :
				return 'Image does not satisfy min. required resolution (1280x720)'
		except :
			return 'Image not found'

		self.obj_fea_1.folder_creation()
		self.obj_fea_1.save_image(self.ref_image, f'{self.user_id}/reference.jpg')
		self.res_lil = self.multi_f.face_points(self.ref_image)
		if len(self.res_lil) == 0 :
			self.obj_fea_1.write_record(f'{self.user_id}')
			return 'No face'
		elif len(self.res_lil) == 1 :
			self.ref_dic = self.res_lil[0]
			try :
				with open(f'{self.user_id}/ref_dict.json', 'w') as self.outfile:
					json.dump(self.ref_dic, self.outfile)
			except Exception as e :
				self.obj_fea_1.logger('Error in reference dictionary creation')
			return 'reference okay'
		else :
			return 'Multiple faces'

ref_image = cv2.imread('./records/Ranjith/reference.jpg')
obj = snapshot(ref_image, 'Ranjith')
print(obj.capture())
