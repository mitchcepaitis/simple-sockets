# Simple MITM

This script is meant to be used as a way to capture raw data communications between two hosts or applications.

Example use: intercepting communication between a web front end client which interacts with a back end application for the purpose of reverse engineering a custom protocol.
  
Usage:
```bash
$ python simple-mitm.py <remote ip> <remote port> <local port>
```
