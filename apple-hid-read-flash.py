#!/usr/bin/env python3

import usb.core
import struct
from collections import namedtuple

APPLE_VID = 0x05ac

Target = namedtuple("Target", ["vid", "pid", "name", "model", "total_size"])

targets = [
  Target(APPLE_VID, 0x0269, "Magic Mouse", "A1657", 524288),
  Target(APPLE_VID, 0x026c, "Magic Keyboard with Numeric Keypad", "A1843", 524288),
  Target(APPLE_VID, 0x029a, "Magic Keyboard with Touch ID", "A2449", 2097152),
  Target(APPLE_VID, 0x029c, "Magic Keyboard", "A2450", 524288),
  Target(APPLE_VID, 0x029f, "Magic Keyboard with Touch ID and Numeric Keypad", "A2520", 2097152),
  Target(APPLE_VID, 0x0315, "Apple TV Remote", "A2854", 1015800),
]

dev = usb.core.find(idVendor=APPLE_VID)
if dev is not None:

  for x in range(5):
    if dev.is_kernel_driver_active(x):
      dev.detach_kernel_driver(x)

  for t in targets:
    if dev.idProduct == t.pid:
      with open("%s.bin" % t.model, "wb") as f:
        offset = 0
        chunk_size = 256
        while offset < t.total_size:
          dev.ctrl_transfer(0x21, 0x09, 0x03B6, 0, b"\xB6" + struct.pack(">I", offset)[1:])
          res = bytes(dev.ctrl_transfer(0xa1, 0x01, 0x03B6, 0, chunk_size))
          offset += (len(res) - 4)
          f.write(res[4:])
          print(bytearray(res).hex())
      print("created %s.bin" % t.model)
      quit()

print("no supported device found")
