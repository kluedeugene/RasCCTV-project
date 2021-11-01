from pyfcm import FCMNotification
 
APIKEY = "AAAAh4ShnlI:APA91bFJhV__84JTeh2IMVxCgvs8AZMU4DJZYpICqJ6bVCCnsuePGOz16Ok0SEVHTj_XdffgBm_9A4GQxb4rWblyEnyExqflT8WY9CZxv6tpXzTrBsUGqYsoX5ZPA1zijRPi9vsseCtE"
 
TOKEN = ["cyE3dAJqRS2oA_GUWNGEj6:APA91bG_fPl7gB7WoumnxIiIloYTK4fz-xDhEtOZSPzKYNuzIjvy44SNjABrVx_cPz-qjblv0ONleYqFOpVdfkdsn1waPmUkvU8nqFnSYY4mslA1UroBpLvfi1wH3L6faPzTiFfUN3L2",
        "etABQmG6TQeUmL6ZkARp_S:APA91bHjloZ2Y_07eC2jex08Vzrd85sk8j1WZAcB_dXTd-MwsPonbHRFHn6WooCU3BjvVNsQ8CK3w9S8QkzkzprL7LQSQqq51BiHjX4FBTwRFzOj8SqR2LFE7YsmHx8MImrGr9MWHviH"]
 
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