"""虚拟电动窗帘平台：支持全开、全关、暂停及 0~100% 开合度调节。"""
from __future__ import annotations

from typing import Any

from homeassistant.components.cover import CoverDeviceClass, CoverEntity, CoverEntityFeature
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
    entities: list[QingSimCover] = []
    for dev_key in selected:
        preset = PRESET_BY_KEY.get(dev_key)
        if not preset:
            continue
        for spec in preset.get("entities", []):
            if spec.get("platform") == "cover":
                entities.append(QingSimCover(hass, preset, spec, auto_areas))
    async_add_entities(entities)


class QingSimCover(CoverEntity):
    """支持百分比开合度的模拟智能窗帘。"""

    _attr_should_poll = False
    _attr_device_class = CoverDeviceClass.CURTAIN
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.STOP
        | CoverEntityFeature.SET_POSITION
    )

    def __init__(
        self,
        hass: HomeAssistant,
        preset: dict[str, Any],
        spec: dict[str, Any],
        auto_areas: bool,
    ) -> None:
        self._hass = hass
        obj_id = spec["object_id"]
        self.entity_id = f"cover.{obj_id}"
        self._attr_unique_id = f"{DOMAIN}_{obj_id}"
        self._attr_name = spec["name"]
        self._attr_current_cover_position = int(spec.get("initial_position", 100))

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

    @property
    def is_closed(self) -> bool:
        return (self._attr_current_cover_position or 0) <= 0

    async def async_added_to_hass(self) -> None:
        self._hass.data.setdefault(DOMAIN, {}).setdefault("entities", {})[self.entity_id] = self

    async def async_will_remove_from_hass(self) -> None:
        self._hass.data.get(DOMAIN, {}).get("entities", {}).pop(self.entity_id, None)

    async def async_open_cover(self, **kwargs: Any) -> None:
        self._attr_current_cover_position = 100
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs: Any) -> None:
        self._attr_current_cover_position = 0
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs: Any) -> None:
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        pos = int(kwargs.get("position", 50))
        self._attr_current_cover_position = max(0, min(100, pos))
        self.async_write_ha_state()
