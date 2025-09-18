#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2025 Bryan Ward, www.bryanward.net
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# mistapi Library Copyright (c) 2023 Thomas Munzer, https://github.com/tmunzer/mistapi_python

import os
import json
import argparse
import mistapi

# Handle command-line arguments
parser = argparse.ArgumentParser(
    description="Generate a report that correlates Mist AP BSSIDs, AP MAC Addresses, and AP Names.",
    prog="mist-bssid-report.py",
)

parser.add_argument(
    "--apiurl",
    help="Mist API URL.  Can also specify via environment variable MIST_APIURL.",
    dest="apiurl",
    required=False,
)

parser.add_argument(
    "--orgid",
    help="Mist ORG ID.  Can also specify via environment variable MIST_ORGID.",
    dest="orgid",
    required=False,
)

parser.add_argument(
    "--token",
    help="Mist API Token.  Requires org-level read access.  Can also specify via environment variable MIST_TOKEN.",
    dest="token",
    required=False,
)

parsergroup_format = parser.add_mutually_exclusive_group(required=False)
parsergroup_format.add_argument(
    "--json",
    help="Output as JSON (default).",
    dest="json",
    default=True,
    action="store_true",
)
parsergroup_format.add_argument(
    "--csv", help="Output at quoted CSV.", dest="csv", default=False, action="store_true"
)

args = parser.parse_args()


# Ensure we have the required Mist API information
if args.apiurl is not None:
    MIST_APIURL = args.apiurl
elif os.environ.get("MIST_APIURL") is not None:
    MIST_APIURL = os.environ.get("MIST_APIURL")
else:
    raise Exception("MIST API URL is not set!")

if args.orgid is not None:
    MIST_ORGID = args.orgid
elif os.environ.get("MIST_ORGID") is not None:
    MIST_ORGID = os.environ.get("MIST_ORGID")
else:
    raise Exception("MIST ORGID is not set!")

if args.token is not None:
    MIST_TOKEN = args.token
elif os.environ.get("MIST_TOKEN") is not None:
    MIST_TOKEN = os.environ.get("MIST_TOKEN")
else:
    raise Exception("MIST TOKEN is not set!")

# Create Mist API Session
mistapisession = mistapi.APISession(apitoken=MIST_TOKEN, host=MIST_APIURL)

# Get /orgs/:org_id/devices/radio_macs
# This is paginated, so we need to use get_all
result = mistapi.get_all(
    mistapisession,
    mistapi.api.v1.orgs.devices.listOrgApsMacs(mistapisession, MIST_ORGID),
)
assert result is not None
assert type(result) is list
assert len(result) > 0
radio_macs = result

# Get /orgs/:org_id/devices
# This is paginated, so we need to use get_all
result = mistapi.get_all(
    mistapisession,
    mistapi.api.v1.orgs.devices.listOrgDevices(mistapisession, MIST_ORGID),
)
assert result is not None
assert type(result) is list
assert len(result) > 0
devices = result

# BSSIDs are made up of the following characters
hexchars = "0123456789abcdef"

# Create some variables to use for data processing
devicesdict = {}
report = {}

# Extract AP MACs and Names
for device in devices:
    devicesdict[device["mac"]] = device["name"]

# Since radio_macs does not have the AP Name in the response, we need to correlate them here
for ap in radio_macs:
    for radio_mac in ap["radio_mac"]:
        # Since the last character of a BSSID can be one of any 16 hex chars, let's produce a list of all of them
        for hexchar in hexchars:
            possible_radio_mac = radio_mac[:-1] + hexchar
            # Save the correlation to our report
            report[possible_radio_mac] = {
                "ap_mac": ap["mac"],
                "ap_name": devicesdict[ap["mac"]],
            }

if args.json:
    # Print as JSON
    print(json.dumps(report, indent=4))
elif args.csv:
    # Print as CSV
    print('"BSSID","AP_MAC","AP_NAME"')
    for record in report:
        print(f'"{record}","{report[record]["ap_mac"]}","{report[record]["ap_name"]}"')
