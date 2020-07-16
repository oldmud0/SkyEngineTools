#!/usr/bin/env python3

"""
Extracts a device rating table that is used to determine what graphics quality
settings are available to the user. There are six possible quality settings:

    system_quality_default           Default Mode (30fps)
    system_quality_highquality       High Performance Mode (60fps)
    system_quality_highquality_alt   Boosted Def Mode (30fps)
    system_quality_lowpower          Energy Saving Mode (Low Resolution)
    system_quality_presentation      High Def Mode (Native Resolution 30fps)
    system_quality_presentation_alt  High Def Mode (30fps)

Presumably, if your device sucks, you will get the `_alt` settings instead of
the non-alt settings. It's also theoretically possible to modify your device's
rating if you think your device can run better than what the benchmark thinks.

It's not clear what the source of these benchmark scores are - my guess is that
they were imported from some public benchmarking database.

To get this script to work, you'll need to extract two parts of
libBootloader.so:

 - A string table of device names (hint: first device is "10.or d")
 - Array of pointers to those device names plus ratings

Because the game looks through the list with a binary search, it's pretty fast.
As of 0.10.0 (151406), the device table contained 2,652 devices.

In C++, the data structures look like this:

    struct DeviceEntry {
        char *device_name;
        int64_t device_rating;
    };

    char *device_names[];
    DeviceEntry device_entries[];
"""

import argparse
import struct

parser = argparse.ArgumentParser(
    description='Extract device names and ratings from the device table to a CSV.'
)

parser.add_argument('device_table', default='device_table.bin',
                    help='file containing array of device strings')
parser.add_argument('rating_table', default='rating_table.bin',
                    help='file containing array of pointers and ratings')

args = parser.parse_args()

with open(args.device_table, 'rb') as f:
    devices = f.read()
with open(args.rating_table, 'rb') as f:
    ratings = list(struct.iter_unpack('Qq', f.read()))

base = ratings[0][0]
print('name,rating')
for device in ratings:
    name_begin = device[0] - base
    name_end = devices.index(b'\0', name_begin)
    name = devices[name_begin : name_end].decode('utf-8')
    rating = device[1]
    print(f'"{name}","{rating}"')
