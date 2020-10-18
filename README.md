GCStreamer - A Media Streaming to Google Cloud Storage and Google Cloud IoT Core
===================================

GCStreamer is an open source media streaming and processing library used in conjunction with [Google Cloud Storage](https://cloud.google.com/storage/docs) to store video chunks and [Google Cloud IoT Core](https://cloud.google.com/iot/docs) to register device status.

[Google Cloud Storage](https://cloud.google.com/storage/docs) supports features like **Object Lifecycle Management**, whih allows to transition automatically to lower-cost storage classes when it meets specific criteria (for example, after 30 days).

GCStreamer library can run on premises or in the clouds. 

<table>
  <tr>
    <td><b>Homepage:</b></td>
    <td><a href="https://cloud.google.com/storage/docs/">Google Cloud Storage</a></td>
  </tr>
  <tr>
    <td><b>Homepage:</b></td>
    <td><a href="https://cloud.google.com/iot/docs/">Google Cloud IoT Core</a></td>
  </tr>
</table>


GCStreamer ingestion pipeline is behaved as a streaming proxy, converting from live streaming procotols to chunk-based uploading. Additonally sends periodical status messages to Cloud IoT Core.

To support live streaming protocols, we utilize [gStreamer](https://gstreamer.freedesktop.org) open-source multimedia framework. Do not confuse gStreamer with GCStreamer, we use both.

# Step 1: Create a named pipe

A named pipe is created to communicate between gStreamer and GCStreamer ingestion proxy. The two processes are running
inside the same Docker image.

```
$ export PIPE_NAME=/path_to_pipe/pipe_name
$ mkfifo $PIPE_NAME
```

# Step 2: Run GCStreamer ingestion proxy

Command line to run our example python code:

```
$ export GOOGLE_APPLICATION_CREDENTIALS=/path_to_credential/credential_json
$ export PIPE_NAME=/path_to_pipe/pipe_name
$ export TIMEOUT=3600
$ ./gcstreamer.py --video_path=$PIPE_NAME 
```

Here, $GOOGLE_APPLICATION_CREDENTIALS specifies where GCP credential json file is located.

# Step 3: Run gStreamer pipeline

gStreamer supports multiple live streaming protocols including but not limited to:

* HTTP Live Streaming (HLS)
* Real-time Streaming Protocol (RTSP)
* Real-time Protocol (RTP)
* Real-time Messaging Protocol (RTMP)
* WebRTC
* Streaming from Webcam

We use gStreamer pipeline to convert from these live streaming protocols to a decodable video stream, and writes the stream into
the named pipe we create in Step 1.

Here, we only provide examples RTSP. If you need other protocol support, please contact us.
```
$ export PIPE_NAME=/path_to_pipe/pipe_name
$ export RTSP_SOURCE=rtsp://ip_addr:port/stream
$ gst-launch-1.0 -v rtspsrc location=$RTSP_SOURCE ! rtpjitterbuffer ! rtph264depay \
      ! h264parse ! mp4mux ! filesink location=$PIPE_NAME
```


# Docker deployment Local

This [docker example](../env/Dockerfile) provides all dependencies configured. You can find the python files
binary in $BIN_DIR directory of the docker image.

Run the following command line on your host machine:
```
$ export DOCKER_IMAGE=gcr.io/windy-site-254307/docker-gcstreamer:latest
$ docker build -t $DOCKER_IMAGE -f env/Dockerfile .
$ docker run -it $DOCKER_IMAGE /bin/bash
```

The last command returns a response similar to the following example.
```
root@e504724e76fc:/#
```

Open another terminal:
```
$ docker exec -it e504724e76fc /bin/bash
```
Now, you have both host terminals that are in the same Docker container.

Some environment settings can be customized in the Docker image.
```
#set up environment for Google Video Intelligence Streaming API
ENV SRC_DIR /googlesrc  #Source code directory
ENV BIN_DIR /google     #Binary directory
```

# Docker deployment in GCP

Push Docker image to GCP container registry:
```
$ gcloud docker --verbosity debug -- push $DOCKER_IMAGE
```

Run the following commands in the terminal for your host machine:
```
$ export KUBE_ID=any_string_you_like
$ kubectl run -it $KUBE_ID --image=$DOCKER_IMAGE -- /bin/bash
```
This returns a response similar to the following:
```
root@$KUBE_ID-215855480-c4sqp:/#
```
To open another terminal connecting to the same Kubernetes container on GCP, run the following command line on host machine:
```
$ kubectl exec -it $KUBE_ID-215855480-c4sqp -- /bin/bash
```

# Flow control

Google Cloud Storage does not provide flow control. It should be required to create some basic flow control, to cover these two cases:

1. when GCStreamer ingestion client is sending requests to Google servers too frequently
2. when GCStreamer ingestion client is sending too much data to Google servers (beyond 20Mbytes per second).

# Code architecture

GCStreamer ingestion  includes the following two directories:

* [client](client): Python client libraries for connecting to Cloud Storage and IoT Core.
* [env](env): Docker example for GCStreamer ingestion.

# Third-party dependency

The open source GCStreamer ingestion library is based on the following third-party open source libraries:

* [gStreamer](https://gstreamer.freedesktop.org): cross-platform multimedia processing and streaming framework.
