"""轻主机虚拟测试沙箱：注册真实 HA 物理设备与可控实体，支持模拟传感器状态变化与一键无痕卸载。"""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS: list[Platform] = [
    Platform.LIGHT,
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.COVER,
]


def _register_set_state_service(hass: HomeAssistant) -> None:
    if hass.services.has_service(DOMAIN, "set_state"):
        return

    async def _handle_set_state(call: ServiceCall) -> None:
        raw_eid = call.data.get("entity_id")
        if isinstance(raw_eid, list):
            eids = [str(x).strip() for x in raw_eid if str(x).strip()]
        elif isinstance(raw_eid, str):
            eids = [x.strip() for x in raw_eid.split(",") if x.strip()]
        else:
            eids = []
        val: Any = call.data.get("value")
        if val is None and "state" in call.data:
            val = call.data.get("state")
        if val is None:
            return
        entities_map = hass.data.get(DOMAIN, {}).get("entities", {})
        for eid in eids:
            ent = entities_map.get(eid)
            if ent is not None and hasattr(ent, "async_set_simulated_value"):
                await ent.async_set_simulated_value(val)

    hass.services.async_register(DOMAIN, "set_state", _handle_set_state)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """在集成域级别预先注册 set_state 服务，与 services.yaml 契约严格对齐。"""
    _register_set_state_service(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """动态加载虚拟测试设备与状态注入服务。"""
    store = hass.data.setdefault(DOMAIN, {"entities": {}, "entries": set()})
    store["entries"].add(entry.entry_id)
    _register_set_state_service(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载测试沙箱并彻底清理内存引用与服务。"""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data:
        entries: set[str] = hass.data[DOMAIN].get("entries", set())
        entries.discard(entry.entry_id)
        if not entries:
            if hass.services.has_service(DOMAIN, "set_state"):
                hass.services.async_remove(DOMAIN, "set_state")
            hass.data.pop(DOMAIN, None)
    return unload_ok
