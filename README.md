# Home Assistant iAqualink Integration with ICL Support

Custom Home Assistant integration for Jandy iAqualink pool systems with **IntellliCenter Light (ICL) zone support**.

## Features

This custom component extends the official iaqualink integration with:

- **ICL Light Zone Control** - Full support for IntellliCenter Light zones
- **RGB Color Control** - Set custom RGB colors on ICL lights
- **Preset Color Effects** - 17 preset colors (Alpine White, Caribbean Blue, Magenta, etc.)
- **Brightness Control** - 0-100% brightness adjustment
- **Multi-Zone Support** - Control up to 4 ICL zones independently

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu → "Custom repositories"
3. Add this repository URL with category "Integration"
4. Search for "iAqualink ICL" and install

### Manual Installation

1. Copy the `custom_components/iaqualink` folder to your Home Assistant `config/custom_components/` directory:

```bash
cp -r custom_components/iaqualink /path/to/homeassistant/config/custom_components/
```

2. Restart Home Assistant

3. The custom component will override the built-in iaqualink integration

## Configuration

Configure through the Home Assistant UI:

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Jandy iAqualink"
4. Enter your iAqualink credentials

## ICL Light Features

### Color Modes

ICL lights appear as RGB lights in Home Assistant with:

- **RGB Color Picker** - Select any custom color
- **Effect Selector** - Choose from 17 preset effects:
  - Off, Alpine White, Sky Blue, Cobalt Blue, Caribbean Blue
  - Spring Green, Emerald Green, Emerald Rose, Magenta
  - Garnet Red, Violet, Color Splash, Slow Splash, Fast Splash
  - USA!, Ruby Red, Mardi Gras

### Services

Use standard light services:

```yaml
# Turn on with preset color
service: light.turn_on
target:
  entity_id: light.icl_zone_1
data:
  effect: "Caribbean Blue"

# Set custom RGB color
service: light.turn_on
target:
  entity_id: light.icl_zone_1
data:
  rgb_color: [255, 0, 128]

# Set brightness
service: light.turn_on
target:
  entity_id: light.icl_zone_1
data:
  brightness: 200  # 0-255 scale
```

## Dependencies

This integration uses a forked version of iaqualink-py with ICL support:
- https://github.com/agrieco/iaqualink-py/tree/feature/icl-light-support

Once the upstream PR is merged, this will be updated to use the official package.

## Troubleshooting

### ICL lights not appearing

1. Ensure your iAqualink system has ICL hardware installed
2. Check Home Assistant logs for ICL detection messages
3. Verify the `is_icl_present` flag is set in your system

### Debug logging

Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    iaqualink: debug
    custom_components.iaqualink: debug
```

## Credits

- Original iaqualink-py library by [@flz](https://github.com/flz)
- ICL support implementation by [@agrieco](https://github.com/agrieco)

## License

BSD 3-Clause License
