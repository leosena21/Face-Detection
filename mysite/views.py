import json
import cv2
import sys

from twilio.rest import Client #Pacote referente ao envio de SMS
from django.shortcuts import render
from django.http.response import StreamingHttpResponse

from .models import Contact


def index(request):
    return render(request, 'mysite/index.html')

def video_feed_1(request):
    return StreamingHttpResponse(stream_1(), content_type='multipart/x-mixed-replace; boundary=frame') # Retorna imagem capturada para o HTML (Tela)

def stream_1():
    cascPath = "haarcascade_frontalface_default.xml" # Arquivo contendo modelos pre-treinados
    faceCascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Definição de camera

    count = 0;
    sendEmail = False # Flag de envio de email

    # client = Client("AC7139693ce26ea2ee6ccc71ad97b4d324", "a37147b7c0f956888178a4b4283b9322") # Autenticação de envio de email

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read() # Inicio da captura da camera

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Conversão da coloração

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        ) # Detecta objetos de tamanhos diferentes na imagem de entrada. Os objetos detectados são retornados como uma lista de retângulos.

        if (faces != ()): # Se identificar faces
            if (sendEmail == False): # Check de envio
                print("ENVIANDO")
                cv2.imwrite(str(count) + ".png", frame) #Salva imagem contendo o rosto
                print(frame)
                sendEmail = True
                count += 1
                # client.messages.create(to="+5571992492638",
                #                        from_="+12055499653",
                #                        body="ALERTA DE PESSOA") #Destino e origem do envio SMS + msg
        else:
            sendEmail = False;

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Exibe o retangulo na tela

        # Display the resulting frame
        # cv2.imshow('Video', frame)
        cv2.imwrite('runtime.jpg', frame) #Tira uma imagem to-do frme
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('runtime.jpg', 'rb').read() + b'\r\n') # Acessa a imagem retornando para a tela

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


