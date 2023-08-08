# Smart Home Project

Welcome to the Smart Home project! This project aims to create a smart home system that gathers data from various sensors, stores it in InfluxDB, and triggers actions based on sensor readings. The system uses Python for implementation.

## Features

- Reads CO2 concentration from MH-Z14B sensor and logs it into InfluxDB every 15 seconds.
- Reads temperature, pressure, and humidity from BME680 sensor and logs it into InfluxDB every minute.
<!-- - Retrieves heart rate data from Fitbit API and logs it into InfluxDB. -->
<!-- - Triggers LED blinking and sends Discord notifications based on sensor data. -->

## Getting Started

1. Clone this repository:

   ```
   git clone https://github.com/sh-mug/smarthome.git
   cd smarthome
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure the project:

   - Edit `config.py` to set InfluxDB connection details and other thresholds.
   <!-- - Obtain Fitbit API credentials and update the `config.py` accordingly. -->

4. Hardware Setup (Raspberry Pi 4):

   Connect the sensors to the Raspberry Pi GPIO pins as follows:

   - **MH-Z14B:**
     - VCC: 5V (Pin 2)
     - GND: Ground (Pin 6)
     - TXD: GPIO14 (Pin 8)
     - RXD: GPIO15 (Pin 10)

   - **BME680:**
     - VCC: 3.3V (Pin 17)
     - GND: Ground (Pin 9)
     - SDA: GPIO2 (Pin 3)
     - SCL: GPIO3 (Pin 5)

5. Run the project:

   ```
   python main.py
   ```

## Project Structure

The project is structured as follows:

- `main.py`: Entry point of the project, controls sensor readings and actions.
- `config.py`: Configuration file for project settings.
- `sensors/`: Contains modules for reading sensor data.
- `actions/`: Contains modules for controlling actions like LED and notifications.
- `requirements.txt`: List of required dependencies.

> [!NOTE]  
> The directory `actions/` is currently under development and does not yet contain the implemented modules for controlling actions such as LED indications and notifications.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
