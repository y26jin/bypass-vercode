# -*- coding: utf-8 -*-
import os
import sys
import PIL
from PIL import Image
from PIL import ImageOps
import requests
import json
import numpy as np
from StringIO import StringIO

class HupuVercode:
    training_image_set = []

    def get_training_vercode(self):
        for i in range(50):
            training_image_path = "testset-"
            training_image_path += str(i+1)
            training_image_path += ".png"

            captcha_url = "http://captcha.hupu.com/?a=getcode"
            ret = requests.get(captcha_url)
            ret_json = json.loads(ret.text)
            img = requests.get(ret_json['msg']['img_path'])
            if img.status_code == 200:
                im = Image.open(StringIO(img.content))
                im.convert('L')
                im = im.point(lambda x:255 if x>128 or x==0 else x)
                im = im.point(lambda x:0 if x<255 else 255)
                im.save(training_image_path)
                self.training_image_set.append(training_image_path)

    def process_training_imageset(self):
        for img_path in self.training_image_set:
            im = Image.open(img_path)
            w,h = im.size
            top=0
            bottom=h
            maxsize=(40,40)
            for i in range(40):
                cropped_path="./training_image/test"
                cropped_path+=img_path[:-4]+"-"
                cropped_path+=str(i)
                cropped_path+=".png"
                left=i*w/40
                right=(i+1)*w/40
                tmp_im = im.crop((left,top,right,bottom))

                # normalize
                pix = np.asarray(tmp_im)
                pix = pix[:,:,0:3]
                idx = np.where(pix-255)[0:2]
                box = box = map(min,idx)[::-1] + map(max,idx)[::-1]
                region = tmp_im.crop(box)
                region.thumbnail(maxsize,Image.ANTIALIAS)
                region.save(cropped_path)


if __name__=="__main__":
    proj = HupuVercode()
    proj.get_training_vercode()
    proj.process_training_imageset()

