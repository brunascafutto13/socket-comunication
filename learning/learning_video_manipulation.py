import cv2

cap = cv2.VideoCapture(0)  

if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

try:
    while True:
        ret, frame = cap.read()  

        if not ret:
            print("Erro ao capturar o frame.")
            break
        
        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print('Ecerrando...')

finally:
    cap.release()
    cv2.destroyAllWindows()
