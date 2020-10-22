#!/usr/bin/env python

from iotcore_client import get_iot_client
from iotcore_client import create_jwt

import logging
import datetime
import argparse
import io

from google.cloud import storage

PROJECT_ID="windy-site-254307"
CLOUD_REGION="europe-west1"
IOT_REGISTRY="camera_registry"
DESTINATION_BUCKET = "gcstreamer-videos"
CHUNK_SIZE = 5242880 # Set the chunk size to 5MB, or 5 * 1024 * 1024 (recommended less than 10MB).

def streaming_gcs_iot(stream_file, camera_id, iot_client):

    sub_topic = 'state'
    mqtt_topic = '/devices/{}/{}'.format(camera_id, sub_topic)

    # Load content.
    logging.info('Preparing to upload to bucket gcs://' + DESTINATION_BUCKET)
    stream = []
    storage_client = storage.Client()
    bucket = storage_client.bucket(DESTINATION_BUCKET)

    with io.open(stream_file, 'rb') as video_file:
        chunk_number = 0
        while True:
            logging.info('Waiting for receiving chunk number ' + str(chunk_number))
            data = video_file.read(CHUNK_SIZE)
            if not data:
                break
        
            # Send status update to IoT Core on behalf of the camera
            # Only once every 10, no need to update so frequently
            if ((chunk_number % 10) == 0):
                payload = "connected"
                logging.info('State: ' + payload)
                iot_client.publish(mqtt_topic, payload, qos=1)

            # Send chunk to GCS
            dateTimeObj = datetime.datetime.now()
            timestampStr = dateTimeObj.strftime("%d%b%Y#%H:%M:%S.%f")
            destination_blob_name = camera_id + "/" + timestampStr + "_" + camera_id + "_" + str(chunk_number) + ".mp4"
            
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_file(io.BytesIO(data))
            logging.info('Chunk uploaded to gs://' + DESTINATION_BUCKET + "/" + destination_blob_name)
     
            chunk_number += 1
            
            stream.append(data)

    # Send status info to IoT Core on behalf of the camera
    payload = "disconnected"
    logging.info('State: ' + payload)
    iot_client.publish(mqtt_topic, payload, qos=1)

    iot_client.disconnect()

if __name__ == '__main__':

    logging.basicConfig(
         format='%(asctime)s %(levelname)-8s %(message)s',
         level=logging.INFO,
         datefmt='%Y-%m-%d %H:%M:%S')
        
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'video_path', help='Pipe name for streaming video.')
    parser.add_argument(
        'camera_id', help='Camera identifier. Must be the same as IoT Core.')
    args = parser.parse_args()

    # Get IoT Core client
    iotcore_client = get_iot_client(
        PROJECT_ID, CLOUD_REGION, IOT_REGISTRY,
        args.camera_id, "../private.key", "RS256",
        "../roots.pem", "mqtt.googleapis.com", 8883)

    # Send to GCS as well as IoT updates
    streaming_gcs_iot(args.video_path, args.camera_id, iotcore_client)