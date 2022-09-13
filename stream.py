from flask import Flask, render_template, url_for, Response
from cam_opencv import Camera
app = Flask (__name__)

app.config['SECRET_KEY'] = '1231231231231231231efsf3f33'

@app.route('/')
def index():
	cameras = {
		'cam1':'http://127.0.0.1:5600/video_feed',
		'cam2':'http://192.168.1.5:5600/video_feed',#shu yerde camera goshulyar
	}
	return render_template('index.html',cameras=cameras)

@app.route('/video_feed')
def video_feed():
	return Response(gen(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/dash')
# def dashboard():
# 	return render_template('dashboard.html')

if __name__ == "__main__":
	app.run(host="0.0.0.0" , port=5000 , debug=True)