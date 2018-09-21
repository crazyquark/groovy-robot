#!/bin/bash
gst-launch-1.0 -v alsasrc device="plughw:1,0" ! audioconvert ! vorbisenc ! oggmux ! tcpserversink host=0.0.0.0 port=5000


