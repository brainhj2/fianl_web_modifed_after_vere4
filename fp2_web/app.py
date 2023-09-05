#-----------------------------------수정전----------------
from flask import Flask, render_template, request, send_from_directory, jsonify, url_for, redirect
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import requests


app = Flask(__name__)
 
cards = []

@app.route('/')
def index_before():
    return render_template('index.html')

@app.route('/imageupload')
def index():
    return render_template('imageupload.html')

from PIL import Image
# 수정 전 잘 돌아가는 get_prediction 여기부터 시작-------
@app.route('/predict', methods=['POST'])
def get_prediction():
    img = request.files['img']
    filename = secure_filename(img.filename)
    # ... (rest of the existing code)
    folder = '/Users/brainhj2/Desktop/final2/fp2_web/predicted'
    img_path = os.path.join(folder, filename)
    img.save(img_path)
    
    predicted_filename = '/Users/brainhj2/Desktop/final2/fp2_web/yolo_predicted_results'

    model = YOLO('yolov8n-seg.pt')
    predict = model.predict(source=img_path,
                            conf=0.25,
                            save=True)

    result = predict[0]
    result_image = Image.fromarray(result.plot()[:,:,::-1])
    path = os.path.join(predicted_filename, filename)
    result_image.save(path)
    img_url = url_for('send_predicted_file', filename=filename)

    
    cards.append({
        "img_src": img_url,
        "link": "http://naver.com",
        "title": "PM 13항 위반종류별",
        "date": "2020/22/22",
        "description": '"안전모 미착용"을 하셨기 때문에 벌금 10만원이 부과됩니다.',
        "comment": "10만원."
    })
    
    return redirect(url_for('gallery'))

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/get-cards')
def get_cards():
    
    return jsonify(cards=cards)

# 수정 전 잘 돌아가는 get_prediction 끝 
@app.route('/predicted/<filename>')
def send_predicted_file(filename):
    return send_from_directory('/Users/brainhj2/Desktop/final2/fp2_web/yolo_predicted_results', filename)
 
@app.route('/get-processed-img')
def get_processed_img():
    # ... determine the filename of the processed image ...
    filename = 'processed_image.jpg'  # replace this with the actual filename
    img_url = '/predicted/' + filename
    return jsonify({'img_url': img_url})

 
 
@app.route('/add-card', methods=['POST'])
def add_card():
    data = request.get_json()
    img_url = data.get('img_url')

    # Add a new card to your data source with the received image URL
    cards.append({
        "img_src": img_url,
        "link": "http://naver.com",
        "title": "PM 13항 위반종류별",
        "date": "2020/22/22",
        "description": '"안전모 미착용"을 하셨기 때문에 벌금 10만원이 부과됩니다.',
        "comment": "10만원."
    })
    return jsonify(success=True)


     
if __name__ == '__main__':
    app.run(debug=True,port=5001)

#-------수정후






# 이미지 업로드 버튼 눌르고 
# 확인하기 눌르면 다음 main() 함수 실행? 

# def main():
#     def algo1() 
#     def algo2()
#     def algo3()

#     input_image = input(~~)#업로드된 이미지파일 


#     위반 bbox = []

#     pm위반 사항 total = []

#     algo1(input_image)

#     if algo1:

#         bbox.append(1 위반객체'sbbox)
#         pm위반 사항1 total.append(pm code)

#     algo2(input_image)

#     if algo2:

#         bbox.append(2 위반객체'sbbox)
#         pm위반 사항2 total.append(pm code)
#     algo3(input_image)

#     if algo3:
#         bbox.append(3 위반객체'sbbox)

#         pm위반 사항3 total.append(pm code)


#     # cv2. ~image draw 
#     input 받은 이미지에 위반 bbox_list에 담긴 좌표를 모두 빨간 네모박스치기
#     박스친후 이미지게시 

#     print(f" {pm위반사항1 }, 과 {pm2위반사항2}.... 을 위반하셨습니다")
#     return None

# if __name__ == '__main__':
#     main()
    