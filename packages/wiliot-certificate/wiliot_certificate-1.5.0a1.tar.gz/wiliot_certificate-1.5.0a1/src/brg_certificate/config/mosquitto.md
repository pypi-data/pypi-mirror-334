
## Downloading and Running a Mosquitto MQTT Broker Locally

This guide will walk you through the process of downloading and running the Mosquitto MQTT broker on your local machine.

__Step 1:__ Download Mosquitto

For Windows:
1. Visit the Mosquitto website download page: https://mosquitto.org/download/
2. Download the latest Windows installer (mosquitto-{version}-install-windows-x64.exe).
3. Run the installer and follow the installation steps.
   - <strong style="color:red">IMPORTANT NOTE:</strong> Make sure to check the option to add Mosquitto to your system's PATH during installation!
4. The default installation path is C:\Program Files\mosquitto.

For Linux (Ubuntu/Debian):
1. Open the terminal.
2. Run the following commands to install Mosquitto and the client utilities:
   ```bash
   sudo apt update
   sudo apt install mosquitto mosquitto-clients
   ```

For macOS:
1. Install Homebrew if you don’t have it by running:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Run the following command to install Mosquitto:
   ```bash
   brew install mosquitto
   ```

__Step 2:__ Start the Mosquitto Broker

For Windows:
1. Open the Command Prompt or PowerShell.
2. Navigate to the Mosquitto installation folder, if it’s not added to your PATH:
   ```bash
   cd "C:\Program Files\mosquitto"
   ```
3. Run the Mosquitto broker:
   ```bash
   mosquitto
   ```

For Linux (Ubuntu/Debian):
1. Start the Mosquitto service:
   ```bash
   sudo systemctl start mosquitto
   ```
   Or, to run it manually for testing:
   ```bash
   mosquitto -v
   ```

For macOS:
1. Start Mosquitto using the terminal:
   ```bash
   mosquitto -v
   ```

__Step 3:__ Test the Mosquitto Broker

You can test the broker by publishing and subscribing to a topic.

Open two terminal windows:

1. In the first window (Subscriber):
   ```bash
   mosquitto_sub -t test/topic
   ```

2. In the second window (Publisher):
   ```bash
   mosquitto_pub -t test/topic -m "Hello, MQTT!"
   ```

If everything works correctly, you should see the message "Hello, MQTT!" in the subscriber window.

__Step 4:__ Enable Mosquitto on Startup (Optional)

For Linux (Ubuntu/Debian):
To make Mosquitto start automatically on boot:
```bash
sudo systemctl enable mosquitto
```

__Step 5:__ Stop the Mosquitto Broker

To stop the broker, use CTRL+C in the terminal where it’s running or stop the service:

For Linux:
```bash
sudo systemctl stop mosquitto
```
