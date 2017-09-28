# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 23:29:16 2017

@author: Frank

"""
import requests
import sys
import os
import base64
import json
import copy
authurl="http://localhost:5000/json"

CLIENT_VERSION = '2.0.32'
OS_VER = os.sys.platform
PYTHON_VERSION = '.'.join(map(str, [os.sys.version_info.major, os.sys.version_info.minor, \
                                    os.sys.version_info.micro]))
GITHUB_TAG_ENDPOINT = 'https://api.github.com/repos/clarifai/clarifai-python/git/refs/tags'

DEFAULT_TAG_MODEL = 'general-v1.3'

class UserError(Exception):
  """ User Error """
  pass

class Input(object):

  """ The Clarifai Input object
  """

  def __init__(self, input_id=None, concepts=None, not_concepts=None, metadata=None, geo=None,
               regions=None, feedback_info=None):
    ''' Construct an Image/Video object. it must have one of url or file_obj set.
    Args:
      input_id: unique id to set for the image. If None then the server will create and return
      one for you.
      concepts: a list of concept names this asset is associated with
      not_concepts: a list of concept names this asset does not associate with
      metadata: metadata as a JSON object to associate arbitrary info with the input
      geo: geographical info for the input, as a Geo() object
      regions: regions of Region object
      feedback_info: FeedbackInfo object
    '''

    self.input_id = input_id

    if not isinstance(concepts, (list, tuple)) and concepts is not None:
      raise UserError('concepts should be a list or tuple')

    if not isinstance(not_concepts, (list, tuple)) and not_concepts is not None:
      raise UserError('not_concepts should be a list or tuple')

    if not isinstance(metadata, dict) and metadata is not None:
      raise UserError('metadata should be a dictionary')

    self.concepts = concepts
    self.not_concepts = not_concepts
    self.metadata = metadata
    self.geo = geo
    self.feedback_info = feedback_info
    self.regions = regions
    self.score = 0
    self.status = None

  def dict(self):
    ''' Return the data of the Input as a dict ready to be input to json.dumps. '''
    data = {'data':{}}

    if self.input_id is not None:
      data['id'] = self.input_id

    # fill the tags
    if self.concepts is not None:
      pos_terms = [(term, True) for term in self.concepts]
    else:
      pos_terms = []

    if self.not_concepts is not None:
      neg_terms = [(term, False) for term in self.not_concepts]
    else:
      neg_terms = []

    terms = pos_terms + neg_terms
    if terms:
      data['data']['concepts'] = [{'id':name, 'value':value} for name, value in terms]

    if self.metadata:
      data['data']['metadata'] = self.metadata

    if self.geo:
      data['data'].update(self.geo.dict())

    if self.feedback_info:
      data.update(self.feedback_info.dict())

    if self.regions:
      data['data']['regions'] = [r.dict() for r in self.regions]

    return data


class Image(Input):

  def __init__(self, url=None, file_obj=None, base64=None, filename=None, crop=None,
               image_id=None, concepts=None, not_concepts=None,
               regions=None,
               metadata=None, geo=None, feedback_info=None, allow_dup_url=False):
    '''
      url: the url to a publically accessible image.
      file_obj: a file-like object in which read() will give you the bytes.
      crop: a list of float in the range 0-1.0 in the order [top, left, bottom, right] to crop out
            the asset before use.
    '''

    super(Image, self).__init__(image_id, concepts, not_concepts, metadata=metadata, geo=geo,
                                regions=regions,
                                feedback_info=feedback_info)

    if crop is not None and (not isinstance(crop, list) or len(crop) != 4):
      raise UserError("crop arg must be list of 4 floats or None")

    self.url = url.strip() if url else url
    self.filename = filename
    self.file_obj = file_obj
    self.base64 = base64
    self.crop = crop
    self.allow_dup_url = allow_dup_url

    # override the filename with the fileobj as fileobj
    if self.filename is not None:
      if not os.path.exists(self.filename):
        raise UserError("Invalid file path %s. Please check!")
      elif not os.path.isfile(self.filename):
        raise UserError("Not a regular file %s. Please check!")

      self.file_obj = open(self.filename, 'rb')
      self.filename = None

    if self.file_obj is not None:
      if not hasattr(self.file_obj, 'getvalue') and not hasattr(self.file_obj, 'read'):
        raise UserError("Not sure how to read your file_obj")

      if hasattr(self.file_obj, 'mode') and self.file_obj.mode != 'rb':
        raise UserError(("If you're using open(), then you need to read bytes using the 'rb' mode. "
                         "For example: open(filename, 'rb')"))

  def dict(self):

    data = super(Image, self).dict()

    image = {'image':{}}

    if self.file_obj is not None:
      # DO NOT put 'read' as first condition
      # as io.BytesIO() has both read() and getvalue() and read() gives you an empty buffer...

      # rewind the fileobj first
      self.file_obj.seek(0)

      if hasattr(self.file_obj, 'getvalue'):
        base64_imgstr = base64.b64encode(self.file_obj.getvalue()).decode('UTF-8')
      elif hasattr(self.file_obj, 'read'):
        base64_imgstr = base64.b64encode(self.file_obj.read()).decode('UTF-8')
      else:
        raise UserError("Not sure how to read your file_obj")

      image['image']['base64'] = base64_imgstr
    elif self.base64 is not None:
      image['image']['base64'] = self.base64.decode('UTF-8')
    else:
      image['image']['url'] = self.url

    if self.crop is not None:
      image['image']['crop'] = self.crop

    image['image']['allow_duplicate_url'] = self.allow_dup_url

    data['data'].update(image)
    return data

if __name__ == "__main__":
    fileio = open(sys.argv[1], 'rb')
    objs = Image(file_obj=fileio)
    params={"Inputs":[objs.dict()]}#params = {"inputs": [obj.dict() for obj in objs]}
    status_code = 199
    retry = True
    max_attempts = attempts = 3
    headers = {}
    while status_code != 200 and attempts > 0 and retry is True:
      if params and params.get('inputs') and len(params['inputs']) > 0:
        params_copy = copy.deepcopy(params)
        for data in params_copy['inputs']:
          data = data['data']
          if data.get('image') and data['image'].get('base64'):
            base64_bytes = data['image']['base64'][:10] + '......' + data['image']['base64'][-10:]
            data['image']['base64'] = base64_bytes
          if data.get('video') and data['video'].get('base64'):
            base64_bytes = data['video']['base64'][:10] + '......' + data['video']['base64'][-10:]
            data['video']['base64'] = base64_bytes
      elif params and params.get('query') and params['query'].get('ands'):
        params_copy = copy.deepcopy(params)

        queries = params_copy['query']['ands']

        for query in queries:
          if query.get('output') and query['output'].get('input') and \
                  query['output']['input'].get('data') and \
                  query['output']['input']['data'].get('image') and \
                  query['output']['input']['data']['image'].get('base64'):
            data = query['output']['input']['data']
            base64_bytes = data['image']['base64'][:10] + '......' + data['image']['base64'][-10:]
            data['image']['base64'] = base64_bytes
      else:
        params_copy = params
    #################################################################33
      headers = {'Content-Type': 'application/json'}
      res = requests.post(authurl, data=json.dumps(params))#, headers=headers)
      status_code = res.status_code
      attempts -= 1
      if status_code == 429 or int(status_code / 100)== 5:
          continue
      break


    print(res)
