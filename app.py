#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from flask import *
import boto3
import random



def upload_img(data):
"""画像をS3にアップロードする関数
"""

    print("upload_img")
    client = boto3.client("s3", region_name="ap-northeast-1")
    s3_key = str(random.randint(0, 10000))
    try:
        # putObject
        response = client.put_object(
            Bucket='poc-compare-actress',
            Body=data,
            Key=s3_key,
        )
    except Exception as ex:
        print(ex)
    else:
        return s3_key

def check_unmached(response_dict):
    """rekigtionの分類結果を確認する関数
    """
    return len(response_dict["FaceMatches"])>0

def compare_actress(s3_key):
    """rekognitionに画像分類させた結果を返す関数
    """
    print("compare_actress")
    client = boto3.client("rekognition", region_name="ap-northeast-1")
    try:
        response = client.compare_faces(
            SourceImage={
                'S3Object': {
                    'Bucket': 'poc-compare-actress',
                    'Name': 'mana1.jpeg'
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': 'poc-compare-actress',
                    'Name': s3_key
                }
            })
        print(response)
        if check_unmached(response):
            response=face_matches = f'{response["FaceMatches"][0]["Similarity"]}%'
        else:
            response=face_matches = "UnMatched"
            
    except Exception as ex:
        print(ex)
        return "Invalid Image"
    else:
        return response


app = Flask(__name__)

# GETでアクセスされた場合には、画像UPLOAD用のフォーム画面に遷移
@app.route('/', methods=['GET'])
def return_form():
    return render_template("form.html")

# POSTでアクセスされた場合には、画像分類の予測結果を返却する
@app.route('/', methods=['POST'])
def predict_image():
    # データの取り出し
    data = request.files['file']
    s3_key = upload_img(data)
    response = compare_actress(s3_key)
    return render_template("result.html", response=response)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
