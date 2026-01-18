import datetime
from netmiko import ConnectHandler
import pandas as pd

print("Current date and time:")
print(datetime.datetime.now())
print("Connecting via SSH => show version")

# SSH connection details
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="devnetsandboxiosxec9k.cisco.com",
    port="22",
    username="jade.piret",
    password="43JxCmOSInJU2_w_"
)

# Run the command
output = sshCli.send_command("show version")

# Extract info
ios_version = ""
hostname = ""
sys_uptime = ""
num_interfaces = ""

for line in output.splitlines():
    if 'Cisco IOS Software' in line:
        ios_version = line.strip()
    elif 'uptime' in line:
        hostname = line.split()[0]
        sys_uptime = line.strip()
    elif 'interface' in line:
        num_interfaces = line.split()[0]

print("\nIOS Version:", ios_version)
print("Hostname:", hostname)
print("System uptime:", sys_uptime)
print("Number of Interfaces:", num_interfaces)

# Store data in a dictionary
data = {
    "Date/Time": [datetime.datetime.now()],
    "Hostname": [hostname],
    "IOS Version": [ios_version],
    "System Uptime": [sys_uptime],
    "Number of Interfaces": [num_interfaces]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Export to Excel
output_file = "device_info.xlsx"
df.to_excel(output_file, index=False)

print(f"\n✅ Data has been saved to '{output_file}'")