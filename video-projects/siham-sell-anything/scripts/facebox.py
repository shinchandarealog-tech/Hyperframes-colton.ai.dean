import sys, subprocess, numpy as np, cv2, mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
src, model, out = sys.argv[1], sys.argv[2], sys.argv[3]; ts = [float(x) for x in sys.argv[4].split(',')]
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(base_options=BaseOptions(model_asset_path=model), min_detection_confidence=0.5))
tiles = []
for t in ts:
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', src, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    img = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).copy()
    base = sys.argv[5] if len(sys.argv) > 5 else src
    rb = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', base, '-frames:v', '1', '-vf', 'scale=270:480', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'])
    small = np.frombuffer(rb, np.uint8).reshape(480, 270, 3)
    for d in det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(small))).detections:
        b = d.bounding_box; x0, y0, w, h = b.origin_x*4, b.origin_y*4, b.width*4, b.height*4
        cv2.rectangle(img, (int(x0), int(y0 - .15*h)), (int(x0+w), int(y0+1.12*h)), (255, 0, 0), 4)
    cv2.putText(img, f'{t:.2f}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 4)
    tiles.append(cv2.resize(img, (360, 640)))
cv2.imwrite(out, cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR))
