from netmiko import ConnectHandler
import pandas as pd

print("Connecting via SSH => show ip interface brief")

# SSH connection details
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host="devnetsandboxiosxec9k.cisco.com",
    port="22",
    username="jade.piret",
    password="43JxCmOSInJU2_w_"
)

# Run the command
output = sshCli.send_command("show ip interface brief")
print(output)

# Split output into lines and parse table
lines = output.splitlines()

# Skip empty lines
lines = [line for line in lines if line.strip()]

# First line is header
header = lines[0].split()

# Remaining lines are data
data_lines = lines[1:]

data = []
for line in data_lines:
    # Split into max number of columns (5)
    parts = line.split(None, 4)
    if len(parts) < len(header):
        # Fill missing columns with empty string
        parts += [""] * (len(header) - len(parts))
    data.append(parts)

# Create DataFrame
df = pd.DataFrame(data, columns=header)

# Export to Excel
output_file = "ip_interface_brief.xlsx"
df.to_excel(output_file, index=False)

print(f"\n✅ IP interface brief has been saved to '{output_file}'")