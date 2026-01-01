#!/usr/bin/env python3
"""Debug script to check ICL light discovery."""

import asyncio
import logging
import sys

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("iaqualink")
logger.setLevel(logging.DEBUG)

async def main():
    # Import here to ensure logging is set up first
    from iaqualink.client import AqualinkClient
    from iaqualink.systems.iaqua.device import IaquaIclLight

    if len(sys.argv) < 3:
        print("Usage: python debug_icl.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    async with AqualinkClient(username, password) as client:
        systems = await client.get_systems()

        for serial, system in systems.items():
            print(f"\n{'='*60}")
            print(f"System: {system.name} ({serial})")
            print(f"Type: {system.data.get('device_type')}")
            print(f"Has ICL: {getattr(system, 'has_icl', 'N/A')}")
            print(f"{'='*60}")

            # Force update to get ICL info
            await system.update()

            print(f"\nAfter update - Has ICL: {getattr(system, 'has_icl', 'N/A')}")

            devices = await system.get_devices()
            print(f"\nTotal devices: {len(devices)}")

            # List all devices
            print("\nAll devices:")
            for name, dev in devices.items():
                dev_type = type(dev).__name__
                is_icl = isinstance(dev, IaquaIclLight)
                print(f"  - {name}: {dev_type} (ICL: {is_icl})")
                if is_icl:
                    print(f"      zone_id: {dev.zone_id}")
                    print(f"      is_on: {dev.is_on}")
                    print(f"      is_absent: {dev.is_absent}")
                    print(f"      data: {dev.data}")

            # Check for ICL-specific devices
            icl_devices = [d for d in devices.values() if isinstance(d, IaquaIclLight)]
            print(f"\nICL devices found: {len(icl_devices)}")

            for dev in icl_devices:
                print(f"\n  ICL Zone {dev.zone_id}:")
                print(f"    Name: {dev.label}")
                print(f"    State: {dev.state}")
                print(f"    Is On: {dev.is_on}")
                print(f"    Is Absent: {dev.is_absent}")
                print(f"    Brightness: {dev.brightness}")
                print(f"    Effect: {dev.effect}")
                print(f"    RGB: {dev.rgb}")

if __name__ == "__main__":
    asyncio.run(main())
