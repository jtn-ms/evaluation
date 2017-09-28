# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 00:03:24 2017

@author: Frank

ref: https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
"""
import requests
import json
import base64
import sys

appname = "general"
url = "http://localhost:4000/api/" + appname + "/1234"#'http://localhost:4000/api/add_message/1234'#

class UserError(Exception):
  """ User Error """
  pass

def image_dict(path,
         metadata = None,
         concept = None):
    
    data = {'data':{}}
    ### add concept
    if concept is not None:
        data['data']['concept'] = metadata
    ### add metadata   
    if metadata is not None:
        data['data']['metadata'] = metadata
    ### add imagedata as base        
    image = {'image':{}}    
    file_obj = open(path, 'rb')
    if file_obj is not None:
        file_obj.seek(0)
        if hasattr(file_obj, 'getvalue'):
            base64_imgstr = base64.b64encode(file_obj.getvalue()).decode('UTF-8')
            base64_bytes = base64_imgstr[:10] + '......' + base64_imgstr[-10:]
        elif hasattr(file_obj, 'read'):
            base64_imgstr = base64.b64encode(file_obj.read()).decode('UTF-8')
            base64_bytes = base64_imgstr[:10] + '......' + base64_imgstr[-10:]
        else:
            raise UserError("Not sure how to read your file_obj")
        image['image']['base64'] = base64_imgstr#base64_bytes#
        
    data['data'].update(image)
    
    return data

def simple_dict(path):
    
    ### add imagedata as base
    file_obj = open(path, 'rb')
    if file_obj is not None:
        file_obj.seek(0)
        if hasattr(file_obj, 'getvalue'):
            base64_imgstr = base64.b64encode(file_obj.getvalue()).decode('UTF-8')
            base64_bytes = base64_imgstr[:10] + '......' + base64_imgstr[-10:]
        elif hasattr(file_obj, 'read'):
            base64_imgstr = base64.b64encode(file_obj.read()).decode('UTF-8')
            base64_bytes = base64_imgstr[:10] + '......' + base64_imgstr[-10:]
        else:
            raise UserError("Not sure how to read your file_obj")
        data = {'image':base64_imgstr}#base64_bytes#
    else:
        data = {'image':'ping'}
            
    return data

def main():
    filename = sys.argv[1]
    url='http://localhost:5000/rupload/'+ filename
    headers={'Content-Type':'application/octet-stream'}
    
    json_parse = False
    if json_parse:
        params = {"image":"ping"} or simple_dict(filename)
    else:
        file = open(filename,'rb')
        params = {'file': file}
    
    status_code = 199
    attempts = 10
       
    while status_code != 200 and attempts > 0:
        res = requests.post(url, headers=headers,data=file)
        status_code = res.status_code
        attempts -= 1
        if status_code == 429 or int(status_code / 100)== 5:
            continue
        break        
        
    if res.ok:
        print(res.json())

if __name__ == "__main__":
    main()