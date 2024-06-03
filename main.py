import network
import usocket as socket
import machine
import time
import onewire
import ds18x20
import secrets

# Set up network
wifi_ssid = secrets.SSID
wifi_password = secrets.PASSWORD

# Connect to WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_password)

# Disable WiFi power saver mode
wifi.config(pm=0xa11140)

# Wait until connected to WiFi
while not wifi.isconnected():
    pass

# Print IP address
ip_address = wifi.ifconfig()[0]
print("Pico W IP address:", ip_address)

# Set up GPIO for heater
heater_pin = machine.Pin(22, machine.Pin.OUT)
heater_pin.value(0)  # Initially turn off heater

# Set up DS18x20 temperature sensor
ds_pin = machine.Pin(26)  # DS18x20 data pin
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

# Default setpoint value
setpoint = 30.0

# HTML form
html = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Reservoir Temperature Control</title></head>
<body>
<h2>Reservoir Temperature Control</h2>
<form id="setpointForm" action="/" method="get">
  <label for="setpoint">Setpoint:</label><br>
  <input type="number" id="setpoint" name="setpoint" min="0" max="100" step="0.1" value="{0:.1f}"><br><br>
  <input type="submit" value="Submit">
</form>
<div id="temperature">Temperature: {0:.1f}</div>
<div id="setpointDisplay">Setpoint: {0:.1f}</div>
<script>
function updateTemperature() {{
  fetch("/temperature")
    .then(response => response.text())
    .then(data => {{
      document.getElementById("temperature").innerHTML = "Temperature: " + data + "°C";
    }})
    .catch(error => console.error('Error fetching temperature:', error));
}}

document.getElementById("setpointForm").addEventListener("submit", function(event) {{
  event.preventDefault();
  var newSetpoint = document.getElementById("setpoint").value;
  fetch("/?setpoint=" + newSetpoint)
    .then(response => {{
      if (response.ok) {{
        console.log("Setpoint updated successfully.");
        // Update temperature display
        updateTemperature();
        // Update setpoint display
        document.getElementById("setpointDisplay").innerHTML = "Setpoint: " + newSetpoint + "°C";
      }} else {{
        throw new Error("Failed to update setpoint.");
      }}
    }})
    .catch(error => console.error('Error updating setpoint:', error));
}});

// Initial update of temperature and setpoint
updateTemperature();
document.getElementById("setpointDisplay").innerHTML = "Setpoint: {0:.1f}" + "°C";

setInterval(updateTemperature, 5000); // Update temperature every 5 seconds
</script>
</body>
</html>
""".format(setpoint)

# Function to parse HTTP request
def parse_request(request):
    request_str = request.decode('utf-8')
    if "GET /?setpoint=" in request_str:
        start = request_str.find("setpoint=") + len("setpoint=")
        end = request_str.find(" HTTP")
        setpoint_str = request_str[start:end]
        return setpoint_str.strip()
    return None

# Function to handle HTTP requests
def handle_request(client_socket):
    global setpoint
    request = client_socket.recv(1024)
    setpoint_str = parse_request(request)
    if setpoint_str:
        print("Setpoint:", setpoint_str)
        try:
            setpoint = float(setpoint_str)
        except ValueError:
            pass
        
    if request.startswith(b"GET /temperature"):
        # Read temperature from DS18x20 sensor
        ds_sensor.convert_temp()
        time.sleep(1)
        temperature = ds_sensor.read_temp(roms[0])
        if temperature is None:
            temperature = "Error"
        else:
            temperature = "{:.1f}".format(temperature)  # Format temperature to one decimal place
            ftemperature = float(temperature)
            if ftemperature < setpoint:
                heater_pin.value(1)
            else:
                heater_pin.value(0)
        client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + bytes(temperature, 'utf-8'))
        client_socket.close()
        return
    
    # Send HTML response
    client_socket.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
    client_socket.send(html)
    client_socket.close()

# Set up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

print("Server running on port 80...")

# Main loop to handle incoming connections
while True:
    client, addr = s.accept()
    print("Client connected from:", addr)
    handle_request(client)
