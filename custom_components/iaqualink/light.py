"""Support for Aqualink pool lights."""

from __future__ import annotations

from typing import Any

from iaqualink.device import AqualinkLight
from iaqualink.systems.iaqua.device import IaquaIclLight

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_EFFECT,
    ATTR_RGB_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import AqualinkConfigEntry, refresh_system
from .entity import AqualinkEntity
from .utils import await_or_reraise

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: AqualinkConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up discovered lights."""
    entities = []
    for dev in config_entry.runtime_data.lights:
        if isinstance(dev, IaquaIclLight):
            entities.append(HassAqualinkIclLight(dev))
        else:
            entities.append(HassAqualinkLight(dev))
    async_add_entities(entities, True)


class HassAqualinkLight(AqualinkEntity[AqualinkLight], LightEntity):
    """Representation of a light."""

    def __init__(self, dev: AqualinkLight) -> None:
        """Initialize AquaLink light."""
        super().__init__(dev)
        self._attr_name = dev.label
        if dev.supports_effect:
            self._attr_effect_list = list(dev.supported_effects)
            self._attr_supported_features = LightEntityFeature.EFFECT
        color_mode = ColorMode.ONOFF
        if dev.supports_brightness:
            color_mode = ColorMode.BRIGHTNESS
        self._attr_color_mode = color_mode
        self._attr_supported_color_modes = {color_mode}

    @property
    def is_on(self) -> bool:
        """Return whether the light is on or off."""
        return self.dev.is_on

    @refresh_system
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light.

        This handles brightness and light effects for lights that do support
        them.
        """
        # For now I'm assuming lights support either effects or brightness.
        if effect_name := kwargs.get(ATTR_EFFECT):
            await await_or_reraise(self.dev.set_effect_by_name(effect_name))
        elif brightness := kwargs.get(ATTR_BRIGHTNESS):
            # Aqualink supports percentages in 25% increments.
            pct = int(round(brightness * 4.0 / 255)) * 25
            await await_or_reraise(self.dev.set_brightness(pct))
        else:
            await await_or_reraise(self.dev.turn_on())

    @refresh_system
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        await await_or_reraise(self.dev.turn_off())

    @property
    def brightness(self) -> int:
        """Return current brightness of the light.

        The scale needs converting between 0-100 and 0-255.
        """
        return self.dev.brightness * 255 // 100

    @property
    def effect(self) -> str:
        """Return the current light effect if supported."""
        return self.dev.effect


class HassAqualinkIclLight(AqualinkEntity[IaquaIclLight], LightEntity):
    """Representation of an ICL (IntellliCenter Light) zone with RGB support."""

    def __init__(self, dev: IaquaIclLight) -> None:
        """Initialize AquaLink ICL light."""
        super().__init__(dev)
        self._attr_name = dev.label
        self._attr_effect_list = list(dev.supported_effects)
        self._attr_supported_features = LightEntityFeature.EFFECT
        # ICL lights support RGB colors
        self._attr_supported_color_modes = {ColorMode.RGB}
        self._attr_color_mode = ColorMode.RGB

    @property
    def is_on(self) -> bool:
        """Return whether the light is on or off."""
        return self.dev.is_on

    @property
    def brightness(self) -> int | None:
        """Return current brightness of the light (0-255 scale)."""
        if self.dev.brightness is not None:
            return self.dev.brightness * 255 // 100
        return None

    @property
    def rgb_color(self) -> tuple[int, int, int] | None:
        """Return the current RGB color."""
        return self.dev.rgb

    @property
    def effect(self) -> str | None:
        """Return the current light effect if supported."""
        return self.dev.effect

    @refresh_system
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light.

        Handles RGB colors, effects, and brightness for ICL lights.
        """
        if rgb_color := kwargs.get(ATTR_RGB_COLOR):
            # Set custom RGB color
            r, g, b = rgb_color
            await await_or_reraise(self.dev.set_rgb(r, g, b))
        elif effect_name := kwargs.get(ATTR_EFFECT):
            # Set preset color effect
            await await_or_reraise(self.dev.set_effect_by_name(effect_name))
        elif brightness := kwargs.get(ATTR_BRIGHTNESS):
            # Set brightness (0-100 scale for ICL)
            pct = brightness * 100 // 255
            await await_or_reraise(self.dev.set_brightness(pct))
        else:
            # Just turn on
            await await_or_reraise(self.dev.turn_on())

    @refresh_system
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off the light."""
        await await_or_reraise(self.dev.turn_off())
