from pyfcm import FCMNotification
 
APIKEY = 
 
TOKEN =
 
# 파이어베이스 콘솔에서 얻어 온 서버 키를 넣어 줌
push_service = FCMNotification(APIKEY)
 
def sendMessage(body, title):
    # 메시지 (data 타입)
    data_message = {
        "body": body, 
        "title": title
    }
 
    # 토큰값을 이용해 1명에게 푸시알림을 전송함
    #message_body is notification part
    result = push_service.notify_multiple_devices(registration_ids=TOKEN,message_body=body, data_message=data_message)
 
    # 전송 결과 출력
    print(result)
 
sendMessage("RasCCTV detect someone", "RasCCTV detect someone")
