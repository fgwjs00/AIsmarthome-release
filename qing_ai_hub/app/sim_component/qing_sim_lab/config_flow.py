"""轻主机虚拟测试沙箱配置流（支持无重启即时挂载与卸载）。"""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries

from .const import DEFAULT_DEVICE_KEYS, DOMAIN


class QingSimLabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """管理虚拟测试设备集的配置条目。"""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            raw_devs = user_input.get("devices")
            if isinstance(raw_devs, str):
                dev_keys = [x.strip() for x in raw_devs.split(",") if x.strip()]
            elif isinstance(raw_devs, list):
                dev_keys = [str(x).strip() for x in raw_devs if str(x).strip()]
            else:
                dev_keys = list(DEFAULT_DEVICE_KEYS)
            auto_areas = bool(user_input.get("auto_assign_areas", True))
            return self.async_create_entry(
                title="轻主机虚拟测试沙箱",
                data={
                    "devices": dev_keys or list(DEFAULT_DEVICE_KEYS),
                    "auto_assign_areas": auto_areas,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional("devices", default=",".join(DEFAULT_DEVICE_KEYS)): str,
                    vol.Optional("auto_assign_areas", default=True): bool,
                }
            ),
        )
