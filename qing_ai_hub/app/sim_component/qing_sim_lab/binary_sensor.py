"""虚拟二元传感器平台：支持人在存在传感器 (occupancy) 与门窗传感器 (door) 实时触发自动化。"""
from __future__ import annotations

from typing import Any

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DEFAULT_DEVICE_KEYS, DOMAIN, PRESET_BY_KEY

_DC_MAP = {
    "occupancy": BinarySensorDeviceClass.OCCUPANCY,
    "door": BinarySensorDeviceClass.DOOR,
    "motion": BinarySensorDeviceClass.MOTION,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Any,
) -> None:
    selected = entry.data.get("devices") or DEFAULT_DEVICE_KEYS
    auto_areas = bool(entry.data.get("auto_assign_areas", True))
    entities: list[QingSimBinarySensor] = []
    for dev_key in selected:
        preset = PRESET_BY_KEY.get(dev_key)
        if not preset:
            continue
        for spec in preset.get("entities", []):
            if spec.get("platform") == "binary_sensor":
                entities.append(QingSimBinarySensor(hass, preset, spec, auto_areas))
    async_add_entities(entities)


class QingSimBinarySensor(BinarySensorEntity):
    """可由沙箱服务动态翻转状态的模拟存在/门磁传感器。"""

    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        preset: dict[str, Any],
        spec: dict[str, Any],
        auto_areas: bool,
    ) -> None:
        self._hass = hass
        obj_id = spec["object_id"]
        self.entity_id = f"binary_sensor.{obj_id}"
        self._attr_unique_id = f"{DOMAIN}_{obj_id}"
        self._attr_name = spec["name"]
        self._attr_is_on = bool(spec.get("initial_on", False))
        dc = spec.get("device_class")
        if dc in _DC_MAP:
            self._attr_device_class = _DC_MAP[dc]

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

    async def async_set_simulated_value(self, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, bool):
            self._attr_is_on = value
        elif isinstance(value, (int, float)):
            self._attr_is_on = bool(value)
        else:
            s = str(value).strip().lower()
            if s == "toggle":
                self._attr_is_on = not bool(self._attr_is_on)
            else:
                self._attr_is_on = s in ("on", "true", "1", "open", "detected", "有人", "打开")
        self.async_write_ha_state()
