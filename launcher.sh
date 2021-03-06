#!bin/bash
# Parameters $DOCKER_IMAGE $PRIVATE_KEY_EXTERNAL $RTSP_URL $DEVICE_ID $CASE_GSTREAMER
echo "launcher.sh parameters = ${*}"

######### Step 1
echo "Setting pipe ..."
export PIPE_NAME=/pipefile
mkfifo $PIPE_NAME
echo "Done setting pipe ..."

######### Step 2
echo "Saving private key of device"
echo "$1" > ./private.key  # save private key to file (for gcstreamer.py)
echo "Launching GCStreamer with device_id:" $3
export GOOGLE_APPLICATION_CREDENTIALS=$BIN_DIR/windy-site-254307-e41b7141a3d0.json
export TIMEOUT=3600

cd $BIN_DIR/python
python gcstreamer.py "$PIPE_NAME" "$3" &  # run in background
sleep 2

######### Step 3
echo "Launching gStreamer with" $2 $4
export RTSP_SOURCE=$2
export CAMERA_TYPE=$4
# External camera stream
if [ "$CAMERA_TYPE" == 'STANDARD' ];
then
      gst-launch-1.0 -v rtspsrc location=$RTSP_SOURCE ! rtpjitterbuffer ! rtph264depay \
            ! h264parse ! flvmux ! filesink location=$PIPE_NAME
fi
# Android
if [ "$CAMERA_TYPE" == 'MP4MUX' ];
then
      gst-launch-1.0 -v rtspsrc location=$RTSP_SOURCE ! rtpjitterbuffer ! rtph264depay \
            ! h264parse ! mp4mux ! filesink location=$PIPE_NAME
fi


