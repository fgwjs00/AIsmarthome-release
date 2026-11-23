"""轻主机虚拟测试沙箱常量与预设全屋模拟设备清单。"""
from __future__ import annotations

from typing import Any, Dict, List

DOMAIN = "qing_sim_lab"

SIM_DEVICE_PRESETS: List[Dict[str, Any]] = [
    {
        "key": "main_light",
        "name": "客厅吸顶主灯",
        "area": "客厅",
        "manufacturer": "易来模拟 (测试)",
        "model": "qing.light.ceiling1",
        "category": "照明",
        "summary": "支持开关、亮度 1~100%、色温 2700K~6500K 无极调节",
        "entities": [
            {
                "platform": "light",
                "object_id": "sim_living_main_light",
                "name": "客厅吸顶主灯",
                "rgb": False,
                "initial_on": True,
                "brightness": 204,
                "kelvin": 4200,
            }
        ],
    },
    {
        "key": "lightstrip",
        "name": "客厅氛围灯带",
        "area": "客厅",
        "manufacturer": "米家模拟 (测试)",
        "model": "qing.light.strip1",
        "category": "照明",
        "summary": "支持开关、亮度、色温、RGB 全彩与流光氛围灯效",
        "entities": [
            {
                "platform": "light",
                "object_id": "sim_living_strip",
                "name": "客厅氛围灯带",
                "rgb": True,
                "effects": ["温馨暖光", "影院氛围", "流光溢彩", "柔和呼吸"],
                "initial_on": True,
                "brightness": 153,
                "kelvin": 3200,
            }
        ],
    },
    {
        "key": "spotlight",
        "name": "客厅防眩射灯",
        "area": "客厅",
        "manufacturer": "绿米模拟 (测试)",
        "model": "qing.light.spot1",
        "category": "照明",
        "summary": "支持开关、亮度 1~100%、色温 2700K~6500K 双色温调光",
        "entities": [
            {
                "platform": "light",
                "object_id": "sim_living_spotlight",
                "name": "客厅防眩射灯",
                "rgb": False,
                "initial_on": False,
                "brightness": 128,
                "kelvin": 3500,
            }
        ],
    },
    {
        "key": "presence_sensor",
        "name": "客厅人在存在传感器",
        "area": "客厅",
        "manufacturer": "绿米模拟 (测试)",
        "model": "qing.sensor.fp2",
        "category": "传感",
        "summary": "毫米波有人/无人状态检测 + 环境光照度 (lx) 双实体联动",
        "entities": [
            {
                "platform": "binary_sensor",
                "object_id": "sim_living_presence",
                "name": "客厅人在存在传感器",
                "device_class": "occupancy",
                "initial_on": False,
            },
            {
                "platform": "sensor",
                "object_id": "sim_living_illuminance",
                "name": "客厅环境光照度",
                "device_class": "illuminance",
                "unit": "lx",
                "initial_value": 45.0,
            },
        ],
    },
    {
        "key": "th_sensor",
        "name": "客厅温湿度传感器",
        "area": "客厅",
        "manufacturer": "米家模拟 (测试)",
        "model": "qing.sensor.ht1",
        "category": "传感",
        "summary": "实时温度 (℃) + 相对湿度 (%) + 电池电量百分比（可联动真实空调）",
        "entities": [
            {
                "platform": "sensor",
                "object_id": "sim_living_temperature",
                "name": "客厅温度",
                "device_class": "temperature",
                "unit": "°C",
                "initial_value": 26.5,
            },
            {
                "platform": "sensor",
                "object_id": "sim_living_humidity",
                "name": "客厅湿度",
                "device_class": "humidity",
                "unit": "%",
                "initial_value": 55.0,
            },
            {
                "platform": "sensor",
                "object_id": "sim_living_th_battery",
                "name": "客厅温湿度计电量",
                "device_class": "battery",
                "unit": "%",
                "diagnostic": True,
                "initial_value": 92.0,
            },
        ],
    },
    {
        "key": "curtain",
        "name": "客厅智能窗帘",
        "area": "客厅",
        "manufacturer": "绿米模拟 (测试)",
        "model": "qing.cover.curtain1",
        "category": "遮阳",
        "summary": "支持全开、全关、暂停与 0~100% 精准开合度控制",
        "entities": [
            {
                "platform": "cover",
                "object_id": "sim_living_curtain",
                "name": "客厅智能窗帘",
                "initial_position": 100,
            }
        ],
    },
    {
        "key": "door_sensor",
        "name": "玄关门窗传感器",
        "area": "玄关",
        "manufacturer": "绿米模拟 (测试)",
        "model": "qing.sensor.magnet1",
        "category": "传感",
        "summary": "入户门开合状态监测，适合测试开门迎宾与离家联动",
        "entities": [
            {
                "platform": "binary_sensor",
                "object_id": "sim_entrance_door",
                "name": "玄关门窗传感器",
                "device_class": "door",
                "initial_on": False,
            }
        ],
    },
    {
        "key": "entrance_light",
        "name": "玄关筒灯",
        "area": "玄关",
        "manufacturer": "易来模拟 (测试)",
        "model": "qing.light.downlight1",
        "category": "照明",
        "summary": "支持开关、亮度与色温调节，配合玄关门磁测试晚归亮灯",
        "entities": [
            {
                "platform": "light",
                "object_id": "sim_entrance_light",
                "name": "玄关筒灯",
                "rgb": False,
                "initial_on": False,
                "brightness": 204,
                "kelvin": 4000,
            }
        ],
    },
    {
        "key": "bedroom_light",
        "name": "主卧吸顶灯",
        "area": "主卧",
        "manufacturer": "易来模拟 (测试)",
        "model": "qing.light.bed1",
        "category": "照明",
        "summary": "支持开关、助眠低亮与暖白双色温调节",
        "entities": [
            {
                "platform": "light",
                "object_id": "sim_bedroom_light",
                "name": "主卧吸顶灯",
                "rgb": False,
                "initial_on": False,
                "brightness": 180,
                "kelvin": 3000,
            }
        ],
    },
]

PRESET_BY_KEY: Dict[str, Dict[str, Any]] = {p["key"]: p for p in SIM_DEVICE_PRESETS}
DEFAULT_DEVICE_KEYS: List[str] = [p["key"] for p in SIM_DEVICE_PRESETS]
