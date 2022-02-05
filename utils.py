from cv2 import cv2
import numpy as np
from PIL import Image
import requests #OCR API
from udpy import UrbanClient #Python wrapper for Urban Dictionary API.
import io
import json
import re
import pytesseract as pytes




# Reconocimiento OCR con python, openCV ,tesseract y  API 
class OptycalCharacterRecognizer:

    def __init__(self,images):
        pytes.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.IMAGE = cv2.imread(images) #openCv vuelve la img a numpy array
        self.IMAGE_NAME = images 
        

    def api_process(self):
       #Tratado de imagen: carga y conversion a bytes
       #image = self.IMAGE
       image = cv2.cvtColor(self.IMAGE, cv2.COLOR_BGR2GRAY)
       ret,th1 = cv2.threshold(image,150,200,cv2.THRESH_BINARY_INV)        
       other,buffer = cv2.imencode('.png',th1,[1,90])
       img_bytes = io.BytesIO(buffer)  #se puede leer en bytes directamente con open('file','rb')
       # Obtener API KEY
       file_key = open('apikey.txt','r')
       api_key = file_key.readline()
       file_key.close()
       # peticion API 
       payload = {'isOverlayRequired': False,
               'apikey': api_key,
               'language': 'eng',
               }
       url_api = 'https://api.ocr.space/parse/image'
       response = requests.post(url_api,
                     files = {self.IMAGE_NAME: img_bytes},
                     data = payload)
       # respuesta API
       result = response.content.decode()
       result = json.loads(result)
       text = result.get('ParsedResults')[0].get('ParsedText')
       print(text)
       stringfinal =''
       for t in text.splitlines():
           words = t.split()
           for w in words:
               w = w.strip('¢~!` \n\'s\t ][|":?><,./\?¿!@#$%^&*()_+{\}-=0123456789')
               stringfinal= stringfinal+';'+ w 
       print(stringfinal)        
       cv2.imshow('Urban dictionary', th1)
       cv2.waitKey(0)
       return text
    #    print(text)
    #    print(type(text))


    def tesseract_process(self):
        image = cv2.cvtColor(self.IMAGE, cv2.COLOR_BGR2GRAY)
        ret,th1 = cv2.threshold(image,150,200,cv2.THRESH_BINARY_INV)
        words = pytes.image_to_data(th1, lang='eng')
        #regex = r"[A-Z|a-z]+"
        finalString = ''
        index = 0
        for word in words.splitlines():
            data = word.split()
            if index != 0 and len(data) == 12:
                x, y, width, height = int(data[6]), int(data[7]), int(data[8]), int(data[9])
                cv2.rectangle(th1, (x, y), (x + width, y + height), (255,0,255), 1)
                word = data[11].strip('¢~!` \n\'s\t ][|":?><,./\?¿!@#$%^&*()_+{\}-=0123456789')
                if len(word)>1:
                    finalString= finalString+';'+word                  
            index += 1
        print(finalString)
        cv2.imshow('Urban dictionary', th1)
        cv2.waitKey(0)
        return finalString

    def process(self,ptype):       
        if ptype == 1:
            return self.api_process()
        elif ptype == 2:
            return self.tesseract_process()
    
    
    # WRAPPER UD
    def definition_term(self, term):
        words = term.split(";")
        client = UrbanClient()
        cont = 1
        #iniciar 
        for w in words[1:]:
            print(w)
            try:
                defs = client.get_definition(f'{w}')
                # d = defs[0]
                file_text = open(f'Definitions/{w}.txt','w')
                for d in defs:
                    file_text.write(f' \n Urban term \t ===> \t {w} \n Definition [{cont}]: \n {d.definition} \n \n')
                    cont+=1
                file_text.close()
            except (RuntimeError, TypeError, NameError, ValueError) :
                pass
        
    #API UD
    def definition_term2(self,term):
        words = term.split(";")
        #iniciar 
        for w in words[1:]:
            print(w)
            try:
                url_api = f"http://api.urbandictionary.com/v0/define?term={w}"
                response = requests.get(url_api)
                # respuesta API
                result = response.content.decode()
                result = json.loads(result)
                defs = result.get("list")
                file_text = open(f'otro/{w}.txt','w')
                for d in defs:
                    #print(d.get("definition"))
                    file_text.write(f'urbanTerm[{w}] \n definition \n [{d.get("definition")}]\n')
                file_text.close()
            except (RuntimeError, TypeError, NameError, ValueError) :
                pass




    def show(self):
        cv2.imshow('Imagen', self.IMAGE)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    
    
        
    

    

    