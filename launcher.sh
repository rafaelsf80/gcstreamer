#!bin/bash
echo "Launching gStreamer"
echo "Parameters = ${*}"

# Step 1
echo "Setting pipe ..."
export PIPE_NAME=/pipefile
mkfifo $PIPE_NAME
echo "Done setting pipe ..."

# Step 2
echo "Launching GCStreamer with camera_id" $3
export GOOGLE_APPLICATION_CREDENTIALS=$BIN_DIR/windy-site-254307-e41b7141a3d0.json
export TIMEOUT=3600
cd $BIN_DIR/python
python gcstreamer.py "$PIPE_NAME" "$3" &
sleep 2

# Step 3
echo "Launching gStreamer with" $2
export RTSP_SOURCE=$2
gst-launch-1.0 -v rtspsrc location=$RTSP_SOURCE ! rtpjitterbuffer ! rtph264depay \
      ! h264parse ! mp4mux ! filesink location=$PIPE_NAME
