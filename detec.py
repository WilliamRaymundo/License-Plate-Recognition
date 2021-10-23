import datetime
import cv2
import imutils
import pytesseract
import json
import requests 
from datetime import datetime


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
cap = cv2.VideoCapture('http://192.168.0.100:8080/?action=stream')
#car_cascade = cv2.CascadeClassifier('cascades/cars.xml')
bg = None;
contador = 0;
#cor pra colocar
color_fingers = (0,255,255)

while True:
    ret, frame = cap.read()
    if ret == False: break


    frame = imutils.resize(frame, width=640)
    frameAux = frame.copy()

   

    if bg is not None:
        #cv2.imshow('bg',bg)

        #REGIÃO DE INTERESSE
        ROI = frame[50:300,200:600]
        cv2.rectangle(frame,(200-2,50-2),(600+2,300+2),color_fingers,1)

        grayRoi = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        glausRoi = cv2.GaussianBlur(grayRoi, (5, 5), 0)
        ret, treshRoi = cv2.threshold(glausRoi, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contornosRoi,_ = cv2.findContours(treshRoi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contornosRoi = sorted(contornosRoi, key = cv2.contourArea,reverse=True)[:1]
        cv2.drawContours(ROI,contornosRoi,0,(0,255,0),1)
        for c in contornosRoi:
            contador += 1;
            if contador % 15 == 0:
                perimetro = cv2.arcLength(c, True)
                if perimetro > 5:
                    approx = cv2.approxPolyDP(c, 0.03 * perimetro, True)
                    if len(approx) == 4:
                        (x, y, lar, alt) = cv2.boundingRect(c)

                        cv2.rectangle(ROI, (x, y), (x + lar, y + alt), (0, 255, 0), 2)

                        roi = ROI[y:y + alt, x:x + lar]
                        placa = ROI[y:y + alt, x:x + lar]

                        config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6'
                        caracs = pytesseract.image_to_string(placa, lang='eng', config=config)
                        
                        caracs = caracs.replace(' ', "")
                        caracs = caracs.replace('  ', "")
                        caracs = caracs.replace("-", "")
                        
                        letras = caracs[:3]
                        num = caracs[4:]
                        
                        letras = letras.replace("-", "")
                        num = num.replace("-", "")

                        num = num.replace('O', "0")
                        letras = letras.replace('0', "O")

                        num = num.replace('I', "1")
                        letras = letras.replace('1', "I")

                        num = num.replace('G', "6")
                        letras = letras.replace('6', "G")

                        num = num.replace('B', "8")
                        letras = letras.replace('8', "B")

                        num = num.replace('T', "1")
                        letras = letras.replace('1', "T")

                        num = num.replace('Z', "2")
                        letras = letras.replace('2', "Z")

                        num = num.replace('H', "11")
                        letras = letras.replace('11', "H")
                        
                        letras = letras.replace('', "")
                        num = num.replace('', "")

                        placa_escrita = letras + '-1' + num
                        print(placa_escrita[:8])
                        print("-----------------")
                        if(1==1):
                       # if(len(placa_escrita) >= 0):
                            #sql = "INSERT INTO historico (fk_local, entrada, saida, capPlaca, Permi, captura) VALUES (%s, %s, %s, %s,%s, %s)"

                            #sql_data = (1, '2020/06/06','2021/04/01',placa_escrita[:8],'Pendente','captura/img001.png')
                           # mycursor = mydb.cursor()
                            
                           # mycursor.execute(sql,sql_data)
                          #  mydb.commit()

                            #url = 'http://localhost:3000/historico'
                            #myobj = {'fk_local': 1,'entrada': '2020/06/06', 'saida': '2021/04/01','capPlaca': placa_escrita[:8],'Permi':'Pendente','captura':'captura/img001.png' }

                           # x = requests.post(url, data = myobj)

                           # print(x.text)
                            data_atual = datetime.now()
                            data_e_hora_em_texto = data_atual.strftime('%Y/%m/%d %H:%M:%S')

                            print(data_e_hora_em_texto)

                            url = 'http://localhost:/Interface-License-Plate-Recognition/index/conecta.php'
                            myobj = '{"fk_local":"1","entrada":"'+data_e_hora_em_texto+'", "saida":"2021/04/01","capPlaca": "'+placa_escrita[:8]+'","Permi":"Pendente","captura":"captursa/img001.png" }'
                            jsonObj = json.loads(myobj)
                            x = requests.post(url, data = jsonObj )

                            print(x.text)
                           
                            file = "imagenTeste.png"
                            cv2.imwrite(file,frame)
                                                
                             

                       # url = "https://docs.google.com/forms/d/e/1FAIpQLSdUhEkJBoJsSjux9DsP6r5FhM784uO9VIbqM4NJFiuY1E9kzw/formResponse"
                        #placa = text
                        #obj = {'entry.1441223166': placa}
                        #r = requests.post(url, params=obj)

                        #print('placa=', text)
                        #print('contador=',contador)

            #bgROI = bg[50:300,380:600]
           # cv2.imshow('ROI',ROI)
            #cv2.imshow('grayROI',grayRoi)
            #cv2.imshow('bgRoi',bgROI)



    cv2.imshow('Frame', frame)
    #teclas de auxilo (Desliga programa etc)
    k = cv2.waitKey(20)
    if k == ord("i"):
        bg = cv2.cvtColor(frameAux,cv2.COLOR_BGR2GRAY)

    if k == 27:
       break

    if k == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()