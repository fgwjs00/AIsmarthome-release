"""虚拟测试灯具平台：完整支持 HA 2025/2026 标准亮度、Kelvin 色温、RGB 彩光与场景复现。"""
from __future__ import annotations

from typing import Any

from homeassistant.components.light import ColorMode, LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DEFAULT_DEVICE_KEYS, DOMAIN, PRESET_BY_KEY


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Any,
) -> None:
    selected = entry.data.get("devices") or DEFAULT_DEVICE_KEYS
    auto_areas = bool(entry.data.get("auto_assign_areas", True))
    entities: list[QingSimLight] = []
    for dev_key in selected:
        preset = PRESET_BY_KEY.get(dev_key)
        if not preset:
            continue
        for spec in preset.get("entities", []):
            if spec.get("platform") == "light":
                entities.append(QingSimLight(hass, preset, spec, auto_areas))
    async_add_entities(entities)


class QingSimLight(LightEntity):
    """支持调光、调色温与 RGB 灯效的模拟智能灯具。"""

    _attr_should_poll = False
    _attr_min_color_temp_kelvin = 2700
    _attr_max_color_temp_kelvin = 6500

    def __init__(
        self,
        hass: HomeAssistant,
        preset: dict[str, Any],
        spec: dict[str, Any],
        auto_areas: bool,
    ) -> None:
        self._hass = hass
        obj_id = spec["object_id"]
        self.entity_id = f"light.{obj_id}"
        self._attr_unique_id = f"{DOMAIN}_{obj_id}"
        self._attr_name = spec["name"]
        self._attr_is_on = bool(spec.get("initial_on", False))
        self._attr_brightness = int(spec.get("brightness", 204))
        self._attr_color_temp_kelvin = int(spec.get("kelvin", 4000))
        self._attr_color_mode = ColorMode.COLOR_TEMP

        if spec.get("rgb"):
            self._attr_supported_color_modes = {ColorMode.COLOR_TEMP, ColorMode.RGB}
            self._attr_rgb_color = None
        else:
            self._attr_supported_color_modes = {ColorMode.COLOR_TEMP}

        effects = spec.get("effects")
        if effects:
            self._attr_supported_features = LightEntityFeature.EFFECT
            self._attr_effect_list = list(effects)
            self._attr_effect = None

        dev_kwargs: dict[str, Any] = {
            "identifiers": {(DOMAIN, preset["key"])},
            "name": preset["name"],
            "manufacturer": preset["manufacturer"],
            "model": preset["model"],
            "sw_version": "1.0-sim",
        }
        if auto_areas and preset.get("area"):
            dev_kwargs["suggested_area"] = preset["area"]
        self._attr_device_info = DeviceInfo(**dev_kwargs)

    async def async_added_to_hass(self) -> None:
        self._hass.data.setdefault(DOMAIN, {}).setdefault("entities", {})[self.entity_id] = self

    async def async_will_remove_from_hass(self) -> None:
        self._hass.data.get(DOMAIN, {}).get("entities", {}).pop(self.entity_id, None)

    async def async_turn_on(self, **kwargs: Any) -> None:
        self._attr_is_on = True
        if "brightness" in kwargs and kwargs["brightness"] is not None:
            self._attr_brightness = max(1, min(255, int(kwargs["brightness"])))
        if (
            "rgb_color" in kwargs
            and kwargs["rgb_color"] is not None
            and ColorMode.RGB in (self._attr_supported_color_modes or set())
        ):
            rgb = kwargs["rgb_color"]
            if isinstance(rgb, (list, tuple)) and len(rgb) == 3:
                self._attr_rgb_color = (
                    max(0, min(255, int(rgb[0]))),
                    max(0, min(255, int(rgb[1]))),
                    max(0, min(255, int(rgb[2]))),
                )
                self._attr_color_temp_kelvin = None
                self._attr_color_mode = ColorMode.RGB
        elif (
            "color_temp_kelvin" in kwargs
            and kwargs["color_temp_kelvin"] is not None
            and ColorMode.COLOR_TEMP in (self._attr_supported_color_modes or set())
        ):
            self._attr_color_temp_kelvin = max(
                self._attr_min_color_temp_kelvin,
                min(self._attr_max_color_temp_kelvin, int(kwargs["color_temp_kelvin"])),
            )
            self._attr_rgb_color = None
            self._attr_color_mode = ColorMode.COLOR_TEMP
        if "effect" in kwargs:
            eff = str(kwargs["effect"]) if kwargs["effect"] else None
            if eff is None or eff.strip().lower() == "off":
                self._attr_effect = None
            elif self._attr_effect_list and eff in self._attr_effect_list:
                self._attr_effect = eff
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        self._attr_is_on = False
        self.async_write_ha_state()
