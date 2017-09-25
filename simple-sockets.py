#! /usr/bin/env python

import socket
import argparse
import sys
import binascii
import select
import time


# Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("ip", help="target IP address")
parser.add_argument("port", help="target port")
parser.add_argument("listen_port", help="local port on which to listen")
args = parser.parse_args()


def close_sockets_and_exit():
  """Close sockets and cleanly exit script"""
  c.close()
  s.close()
  sys.exit()


def host_a_to_capture_to_host_b(host_a, host_b):
  """Receive data on local listening connection and send to remote connection"""
  try:
    data = c.recv(1024)
    capture.append(host_a + ": " + str(binascii.hexlify(data)))
  except:
    print("[!] Data could not be received from " + host_a)
    close_sockets_and_exit()

  if data:
    try:
      s.send(data)
    except:
      print("[!] Data could not be sent to " + host_b)
      close_sockets_and_exit()



def host_b_to_capture_to_host_a(host_a, host_b):
  """Receive data from remote connection, capture it, and forward 
  to local listening connection"""
  try:
    data = s.recv(1024)
    capture.append(host_b + ": " + str(binascii.hexlify(data)))
  except:
    print("[!] Data could not be received from " + host_b)
    close_sockets_and_exit()

  if data:
    try:
      c.send(data)
    except:
      print("[!] Data could not be sent to " + host_a)
      close_sockets_and_exit()


def main():
  # Grab command line arguments
  TCP_IP = str(args.ip)                # IP needs to be string
  TCP_PORT = int(args.port)            # Port needs to be an integer
  LISTEN_PORT = int(args.listen_port)  # Listen port needs to be an integer
  LISTEN_IP = ''                       # Open port on machine which runs this script


  # List of intercepted data
  capture = []


  # Remote Connection
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("[+] Successfully connected to " + str(TCP_IP) + ":" + str(TCP_PORT))
  except:
    # If the connection fails, exit
    print("[!] Failed to connect to remote host.")
    sys.exit()


  # Local Listening Connection
  try:
    l = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    l.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    l.bind((LISTEN_IP, LISTEN_PORT))
    l.listen(1)
    print("[+] Listening for connections on localhost port " + str(LISTEN_PORT))
  except:
    print("[!] Failed to open local listening port.")
    sys.exit()


  # Listen for incoming connection
  try:
    c, addr = l.accept()
    print("[+] Connection received from " + str(addr[0]))
  except:
    print("[!] Could not receive connection.")
    close_sockets_and_exit()


  # Define hosts for easier reference
  host_a = str(addr[0])
  host_b = TCP_IP


  # Loop through the exchange
  while True:

    try:
      # Determine which socket has data waiting
      r, w, e = select.select(socket_list, [], [], 5)
    except:
      print("[i] Socket timeout")
      break
    if r:
      if r == c:
        host_a_to_capture_to_host_b(host_a, host_b)
      elif r == s:
        host_b_to_capture_to_host_a(host_a, host_b)
    else:
      break

  print("[+] Data interception complete")


  # Print intercepted data
  ## TODO: print ASCII chars if in range
  for line in capture:
    print("[i] " + line)
  close_sockets_and_exit()

if __name__ == "__main__":
  main()
