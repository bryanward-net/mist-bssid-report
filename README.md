# Mist BSSID Report

Generate a report that correlates Mist AP BSSIDs, AP MAC Addresses, and AP Names.
Report can be formatted as either JSON or CSV.


## Installation

Requires Python 3.9 or higher.
Requires mistapi library by Thomas Munzer, https://github.com/tmunzer/mistapi_python .

`pip install mistapi`
or
`uv pip install mistapi`

Set environment variables (preferred).
```
export MIST_APIURL="api.mist.com"
export MIST_ORGID="11111111-2222-3333-4444-555555555555"
export MIST_TOKEN="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

Run as follows.


## Usage

`mist-bssid-report.py [-h] [--apiurl APIURL] [--orgid ORGID] [--token TOKEN] [--json | --csv]`

```
options:
  -h, --help       show this help message and exit
  --apiurl APIURL  Mist API URL. Can also specify via environment variable MIST_APIURL.
  --orgid ORGID    Mist ORG ID. Can also specify via environment variable MIST_ORGID.
  --token TOKEN    Mist API Token. Requires org-level read access. Can also specify via environment variable MIST_TOKEN.
  --json           Output as JSON (default).
  --csv            Output at quoted CSV.
```


Example:

```
mist-bssid-report.py

{
    "5c5b35111110": {
        "ap_mac": "5c5b3511115c",
        "ap_name": "MyMistAP"
    },
    "5c5b35111111": {
        "ap_mac": "5c5b3511115c",
        "ap_name": "MyMistAP"
    },
    "5c5b35111112": {
        "ap_mac": "5c5b3511115c",
        "ap_name": "MyMistAP"
    }
    ...
}
```

```
mist-bssid-report.py --csv

"5c5b35111110","5c5b3511115c","MyMistAP"
"5c5b35111111","5c5b3511115c","MyMistAP"
"5c5b35111112","5c5b3511115c","MyMistAP"
...
```


To save the report to a file, use your operating system's output redirection.

### Linux (including WLANPi and WSL on Windows) and MacOS

`mist-bssid-report.py > myreport.json`

`mist-bssid-report.py --csv > myreport.csv`


### Windows Powershell

`mist-bssid-report.py | Out-File -FilePath .\myreport.json`

`mist-bssid-report.py --csv | Out-File -FilePath .\myreport.csv`
