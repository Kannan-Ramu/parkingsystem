import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

def generate_frames():
    cap_original = cv2.VideoCapture(0)

    while True:
        success_original, frame = cap_original.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        if not (success_original):
            break

        frame_combined = cv2.hconcat([frame, gray_frame, blur_frame])

        ret, buffer = cv2.imencode('.jpg', frame_combined)
        frame_combined = buffer.tobytes()

        yield (
            b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_combined + b'\r\n'
        )

    cap_original.release()
    cap_grayscale.release()
    cap_blur.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed_combined')
def video_feed_combined():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
