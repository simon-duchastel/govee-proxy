#!/bin/bash
if screen -list | grep -q "govee_proxy"; then
    echo "Stopping Govee Proxy..."
    screen -S govee_proxy -X quit
    echo "Govee Proxy stopped."
else
    echo "Govee Proxy is not running."
fi
