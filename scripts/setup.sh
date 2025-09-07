#!/bin/bash
# This script sets up the system to run main_startup.py on boot,
# plays a sound on startup, and plays a sound on failed SSH login attempts.
# It also updates .bashrc to play a sound on successful SSH login and adds 
# an alias for python3.
# Make sure to run this script only once.

# ------------------------------------------------------------------
RC_FILE="/etc/rc.local"
PY_SCRIPT="/home/admin/scripts/main_startup.py"

# Backup existing rc.local (just in case)
if [ -f "$RC_FILE" ]; then
    sudo cp "$RC_FILE" "${RC_FILE}.bak.$(date +%F-%H%M%S)"
    echo "[INFO] Backup of rc.local created."
fi

sudo tee "$RC_FILE" > /dev/null << EOF
#!/bin/bash
python3 $PY_SCRIPT &
exit 0
EOF

sudo chmod +x "$RC_FILE"

echo "[DONE] New rc.local installed. $PY_SCRIPT will run on boot."

# ------------------------------------------------------------------
# Add startup-sound.service to /etc/systemd/system
STARTUP_SOUND_SERVICE="/etc/systemd/system/startup-sound.service"

sudo tee "$STARTUP_SOUND_SERVICE" > /dev/null << EOF
[Unit]
Description=Play sound at startup
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/home/admin/startup_sound.sh

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable startup-sound.service

echo "[DONE] Created and enabled $STARTUP_SOUND_SERVICE."

# ------------------------------------------------------------------
# Add ssh-fail-sound.service to /etc/systemd/system
SSH_FAIL_SOUND_SERVICE="/etc/systemd/system/ssh_fail_sound.service"

sudo tee "$SSH_FAIL_SOUND_SERVICE" > /dev/null << EOF
[Unit]
Description=Play sound at startup
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/home/admin/ssh_fail_sound.sh

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ssh_fail_sound.service

echo "[DONE] $SSH_FAIL_SOUND_SERVICE created and enabled."

# ------------------------------------------------------------------
# Update ~/.bashrc to play sound on SSH login and add python3 alias
BASHRC_FILE="/home/admin/.bashrc"

sudo tee -a "$BASHRC_FILE" > /dev/null << 'EOF'

# Play SSH login sound if this is an SSH session
if [ -n "$SSH_CONNECTION" ]; then
    mpg123 -q /home/admin/audio_files/im_in.mp3 &
fi

alias py="python3"
EOF

echo "[DONE] $BASHRC_FILE updated with SSH login sound and py alias."

# ------------------------------------------------------------------
# USAGE:
# 1. Save this file as setup.sh
# 2. Make it executable: chmod +x setup.sh
# 3. Run it once: ./setup.sh
# 4. After reboot, $PY_SCRIPT will run automatically.
#
# Notes:
# - A backup of your original rc.local is stored with a timestamp.
# - You can restore it if needed:
#       sudo mv /etc/rc.local.bak.YYYY-MM-DD-HHMMSS /etc/rc.local
# ------------------------------------------------------------------