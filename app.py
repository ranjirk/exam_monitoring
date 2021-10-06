# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2, videoCapture
from videoCapture import live_feed



# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    user_id = 'Ranjith'
    obj = live_feed(img, user_id)
    response = obj.capture()


    # response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
