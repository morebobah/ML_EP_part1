import pika, logging, json, time, base64
import httpx
#import torch
#from PIL import Image
#from transformers import TrOCRProcessor, VisionEncoderDecoderModel

model_cost = 30.0

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
) 

logger = logging.getLogger(__name__) 

connection_params = pika.ConnectionParameters(host='rabbitmq',
                                              port=5672,
                                              virtual_host='/',
                                              credentials=pika.PlainCredentials(
                                                  username='rbbmq',
                                                  password='rbbmqpwd'
                                              ),
                                              heartbeat=30,
                                              blocked_connection_timeout=2)

connection = pika.BlockingConnection(connection_params)

chanel = connection.channel()

queue_name = 'ml_task_queue'

#def predict_text(image_data):
#    image = Image.frombytes('RGBA', (128,128), image_data)
#    pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(model.device)
#    model.eval()
#    with torch.no_grad():
#        output_ids = model.generate(pixel_values)
#    predicted_text = processor.batch_decode(output_ids, skip_special_tokens=True)[0]
#    return predicted_text

def callback(ch, method, properties, body, *args, **kwargs):
    payload = json.loads(body)
    file_name = payload['image']
    image = base64.b64decode(payload['bytes'])

    #model_name = "emelnov/ocr-captcha-v4-mailru"
    #processor = TrOCRProcessor.from_pretrained(model_name)
    #model = VisionEncoderDecoderModel.from_pretrained(model_name).to(
    #    torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #)
    #predict_text(image)
    result = 'ml solved string'
    
    data = {'task_id': payload['task_id'],
            'user_id': payload['user_id'],
            'result': result, 
            'cost': model_cost, 
            'key': 'secret_key'}
    
    r = httpx.patch('http://app:8000/ml/task/complete', 
                   data=json.dumps(data), 
                   headers={"Content-Type": "application/json"},)
    if 199<r.status_code<300:
        logger.info(f'Успешно: "{r.json()}"')
    else:
        logger.info(f'С ошибкой: "{r.json()}"')
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    

chanel.basic_consume(queue_name, 
                     on_message_callback=callback,
                     auto_ack=False)

logger.info('Waiting for messages. To exit, press Ctrl+C') 
chanel.start_consuming()