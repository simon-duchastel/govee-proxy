#!/bin/bash
# Check if govee_proxy is already running
if screen -list | grep -q "govee_proxy"; then
    echo "Govee Proxy is already running."
else
    echo "Starting Govee Proxy in the background..."
    screen -dmS govee_proxy bash -c "source govee-env/bin/activate && python3 govee_proxy.py"
    echo "Proxy started. Use './stop_govee.sh' to kill it or 'screen -r govee_proxy' to see logs."
fi
