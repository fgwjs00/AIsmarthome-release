"""虚拟数值传感器平台：支持温度、湿度、光照度与电池电量模拟注入（真实触发 numeric_state 自动化）。"""
from __future__ import annotations

import math
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DEFAULT_DEVICE_KEYS, DOMAIN, PRESET_BY_KEY

_DC_MAP = {
    "temperature": SensorDeviceClass.TEMPERATURE,
    "humidity": SensorDeviceClass.HUMIDITY,
    "illuminance": SensorDeviceClass.ILLUMINANCE,
    "battery": SensorDeviceClass.BATTERY,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Any,
) -> None:
    selected = entry.data.get("devices") or DEFAULT_DEVICE_KEYS
    auto_areas = bool(entry.data.get("auto_assign_areas", True))
    entities: list[QingSimSensor] = []
    for dev_key in selected:
        preset = PRESET_BY_KEY.get(dev_key)
        if not preset:
            continue
        for spec in preset.get("entities", []):
            if spec.get("platform") == "sensor":
                entities.append(QingSimSensor(hass, preset, spec, auto_areas))
    async_add_entities(entities)


class QingSimSensor(SensorEntity):
    """可动态修改数值的模拟环境/电量传感器。"""

    _attr_should_poll = False
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        hass: HomeAssistant,
        preset: dict[str, Any],
        spec: dict[str, Any],
        auto_areas: bool,
    ) -> None:
        self._hass = hass
        obj_id = spec["object_id"]
        self.entity_id = f"sensor.{obj_id}"
        self._attr_unique_id = f"{DOMAIN}_{obj_id}"
        self._attr_name = spec["name"]
        self._attr_native_value = float(spec.get("initial_value", 0.0))
        self._attr_native_unit_of_measurement = spec.get("unit")
        dc = spec.get("device_class")
        if dc in _DC_MAP:
            self._attr_device_class = _DC_MAP[dc]
        if spec.get("diagnostic"):
            self._attr_entity_category = EntityCategory.DIAGNOSTIC

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
        if value is None or isinstance(value, bool):
            raise ValueError(f"Invalid boolean/null simulated sensor value: {value!r}")
        num = round(float(value), 1)
        if not math.isfinite(num):
            raise ValueError(f"Invalid non-finite simulated sensor value: {value!r}")
        self._attr_native_value = int(num) if num.is_integer() else num
        self.async_write_ha_state()
