#!/bin/bash

SOUND_FILE="/home/admin/audio_files/disqualified_loud.mp3"

journalctl -fu ssh | \
while read -r line; do
    if echo "$line" | grep -q "Failed password"; then
        mpg123 -q "$SOUND_FILE"
    fi
done