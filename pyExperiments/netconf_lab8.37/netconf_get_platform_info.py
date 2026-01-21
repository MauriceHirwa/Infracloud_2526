#!/usr/bin/env python3
"""
Cisco CSR1000v / IOS XE 16.9+ NETCONF Inventory Script
- Option to display all XML sections or only summary (hostname, interfaces, IPv4)
- Summary data exported to Excel
"""

from ncclient import manager
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import pandas as pd

# --- Router details ---
ROUTER = {
    "host": "devnetsandboxiosxec9k.cisco.com",
    "port": 830,
    "user": "jade.piret",
    "password": "43JxCmOSInJU2_w_",
}

# --- Connect to router ---
print("\nNow connecting to router via NETCONF...\n")
m = manager.connect(
    host=ROUTER["host"],
    port=ROUTER["port"],
    username=ROUTER["user"],
    password=ROUTER["password"],
    hostkey_verify=False,
    device_params={"name": "csr"},
    look_for_keys=False,
    allow_agent=False
)

# --- Helper functions ---
def get_pretty(reply):
    """Return pretty-formatted XML data"""
    return parseString(reply.data_xml).toprettyxml()

def get_data(filter_xml, get_config=False):
    """Perform NETCONF get or get-config"""
    if get_config:
        reply = m.get_config(source="running", filter=("subtree", filter_xml))
    else:
        reply = m.get(filter=("subtree", filter_xml))
    return reply

# --- Ask user ---
choice = input("Do you want to see 'all' data or only a 'summary' (hostname, interfaces, IPv4)? ").strip().lower()

# === [1] Hostname ===
hostname_filter = """
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <hostname/>
</native>
"""
hostname_reply = get_data(hostname_filter, get_config=True)
hostname_xml = get_pretty(hostname_reply)

# Extract hostname
root = ET.fromstring(hostname_reply.data_xml)
ns = {"ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native"}
hostname_elem = root.find(".//ios:hostname", ns)
hostname = hostname_elem.text if hostname_elem is not None else "Unknown"

# === [2] Platform / Software Version ===
platform_filter = """
<platform-software xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform-software-oper"/>
"""
platform_reply = get_data(platform_filter)
platform_xml = get_pretty(platform_reply)

# === [3] Hardware Inventory ===
hardware_filter = """
<components xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform-oper"/>
"""
hardware_reply = get_data(hardware_filter)
hardware_xml = get_pretty(hardware_reply)

# === [4] Interfaces ===
interfaces_filter = """
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
  <interface/>
</interfaces>
"""
interfaces_reply = get_data(interfaces_filter)
interfaces_xml = get_pretty(interfaces_reply)

# Extract interfaces + IPv4
root = ET.fromstring(interfaces_reply.data_xml)
ns_if = {"if": "urn:ietf:params:xml:ns:yang:ietf-interfaces",
         "ip": "urn:ietf:params:xml:ns:yang:ietf-ip"}

interfaces = []
for intf in root.findall(".//if:interface", ns_if):
    name = intf.find("if:name", ns_if)
    ipv4 = intf.find(".//ip:address/ip:ip", ns_if)
    interfaces.append({
        "Interface": name.text if name is not None else "N/A",
        "IPv4": ipv4.text if ipv4 is not None else "N/A"
    })

# === [5] Routing (OSPF) ===
ospf_filter = """
<ospf-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper"/>
"""
ospf_reply = get_data(ospf_filter)
ospf_xml = get_pretty(ospf_reply)

# === [6] CDP Neighbors ===
cdp_filter = """
<cdp-neighbor-details xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper"/>
"""
cdp_reply = get_data(cdp_filter)
cdp_xml = get_pretty(cdp_reply)

# === [7] LLDP Neighbors ===
lldp_filter = """
<lldp-entries xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper"/>
"""
lldp_reply = get_data(lldp_filter)
lldp_xml = get_pretty(lldp_reply)

# === OUTPUT ===
if choice == "all":
    print("\nHostname:")
    print(hostname_xml)
    print("\nPlatform / Software Version:")
    print(platform_xml)
    print("\nHardware Inventory:")
    print(hardware_xml)
    print("\nInterfaces:")
    print(interfaces_xml)
    print("\nRouting (OSPF):")
    print(ospf_xml)
    print("\nCDP Neighbors:")
    print(cdp_xml)
    print("\nLLDP Neighbors:")
    print(lldp_xml)

else:
    print(f"\nDevice Hostname: {hostname}")
    print("\nInterfaces and IPv4 Addresses:")
    for item in interfaces:
        print(f"{item['Interface']}: {item['IPv4']}")

    # Export to Excel
    df = pd.DataFrame(interfaces)
    df.insert(0, "Device Name", hostname)
    output_file = "netconf_summary.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\n✅ Summary exported to '{output_file}'")

m.close_session()
print("\nOK: NETCONF inventory query complete.\n")