# 更新日志

## 0.3.14 (2026-11-26)
- **全面新增 X86_64 (`amd64`) 架构原生支持（覆盖 Intel N100/J4125 迷你主机、软路由、NAS 与 PVE/VMware/Unraid HAOS 虚拟机）**：
  - **华为「智慧生活」& 小艺引擎 X86 网卡自动桥接垫片 (`native/netshim.c` / `huawei_bridge.py` / `huawei_bridge_worker.py` / `Dockerfile`)**：内置原生 `libqing_netshim.so` 用户态兼容垫片，在采用可预测网卡命名（`enp*` / `eno*` / `ens*`）而无 `eth0` 的 X86 HAOS 主机上自动将活动局域网网卡无感映射为 `eth0`（无需宿主机手动创建 `macvlan`），同时校验 64 位 ELF `e_machine` 杜绝 `amd64`/`aarch64` 跨架构 `.so` 误加载
  - **Rust 安全壳 `qing-launcher` X86 物理机与虚拟机指纹增强 (`fingerprint.rs`)**：过滤 AMI/OEM 主板常见未烧录占位 UUID（`Default string` / `To be filled by O.E.M.` / `03000200-...`），新增主板 `board_serial` 与 NVMe 硬盘序列号回退采集，并兼容 PVE/VMware/Hyper-V 虚拟化网卡 `NET_ADDR_SET` 固定 MAC（不影响既有 ARM64 设备机器码）
  - **X86 虚拟空壳串口去噪与双架构构建导出工具链升级 (`zigbee.py` / `build_release.ps1` / `export_binary_addon.py`)**：自动过滤 X86 Linux 内核默认暴露的 32 个 `platform/serial8250` 空壳 `/dev/ttyS*` 槽位；支持 `build_release.ps1 -Arch amd64|arm64|all` 与 `export_binary_addon.py --platform linux/amd64` 一键构建导出 X86 商业零源码安装包

## 0.3.13 (2026-11-26)
- **修复「华为智慧生活设备同步 (`huawei_smarthome`)」组件下载 `HTTP 404` 问题 (`installer.py`)**：
  - 原社区仓库 `xiasi0/ha-huawei-smarthome` 已下线迁移，现已切换至最新活跃维护源 `duanyudan86/ha-huawei-smarthome`（`v2026.11.15`），并内置 `kosmo888/ha-huawei-smarthome`、`lwd333/ha-huawei-smarthome` 多仓库自动故障转移兜底
- **保留 Web UI 云端远程隧道开关与自定义主机名 (`config.py`)**：升级加载项或在 Supervisor 配置页修改其他项时，不再被默认 `options.json` 静默重置已绑定的云端远程开关与名称

## 0.3.12 (2026-11-26)
- **华为「智慧生活」& 小艺墙壁开关灯控（一开/二开/三开/四开）逐路拆分与灯具映射**：
  - **墙壁开关每一路灯控独立映射为华为灯具 (`pid="002"`, `huawei_bridge_worker.py`)**：自动将单火/零火一开、二开、三开、四开智能墙壁开关上的每一路继电器及多路灯光面板拆分为独立华为「灯泡/灯具」并保留各自的房间归属与中文名称（对仅写“左键/中键/右键”的通道自动拼接面板名），既支持 App 独立开关，也支持呼叫“小艺小艺，打开客厅主灯 / 关闭客厅所有的灯”而不误关电视/路由器智能插座 (`pid="008"`)
  - **辅助配置开关与面板指示灯智能去噪**：自动剔除 `entity_category: config/diagnostic` 及面板背光灯、指示灯、童锁、转无线开关、凌动模式、断电记忆等非照明子实体，并自动清理旧版残留空壳设备

## 0.3.11 (2026-11-26)
- **华为「智慧生活」& 小艺场景一键触发、自动化双向启停与房间完整跟随同步**：
  - **场景 (`scene.*`) 自动映射为华为点动开关 (`huawei_bridge_worker.py`)**：支持在华为智慧生活 App 一键点击或对手机/音箱喊“小艺小艺，打开<场景名>”直接触发轻主机跨品牌场景，触发后 1.2 秒自动复位回待命状态
  - **自动化 (`automation.*`) 自动映射为华为双向状态开关 (`huawei_bridge_worker.py`)**：实时反映轻主机自动化的启用/停用状态，支持在华为 App 或通过小艺语音远程开启/暂停任意自动化，并与 HA 侧状态双向实时联动
  - **房间归属 (`area_id`) 智能回填与入口统一 (`huawei_bridge_worker.py` / `app.js`)**：自动将实体级房间归属回填至设备与虚拟场景/自动化；统一品牌接入卡片与顶部跨生态卡片的华为桥接入口，新增「立即同步设备/场景/自动化」与分项勾选开关

## 0.3.10 (2026-11-26)
- **华为鸿蒙智家反向网桥大快照缓冲与真实 C SDK 深度适配 + 阿里云杭州 ACR 极速预构建分发**：
  - **修复多设备环境下子进程 `Separator is not found, and chunk exceed the limit` 崩溃 (`huawei_bridge.py` / `huawei_bridge_worker.py`)**：将主子进程 JSON-Lines IPC 管道缓冲上限从默认 `64 KiB` 提升至 `32 MiB`，支持数千个 HA 实体全量快照秒级同步
  - **深度对齐上游 `ha_hwhomebridge` `v1.0.0` 原生 API (`huawei_bridge_worker.py`)**：内置零外部依赖 `aiofiles` / `psutil` / `homeassistant.config_entries` / `er.async_entries_for_device` 兼容层，真实调用 `start_hw_hilink_bridge` 与 `PINManager.generate_pin()` 联动 C 侧 `OnPINQueryCB` 回调校验，自动为无 `device_id` 的独立灯具/开关/风扇合成虚拟设备并实时回传已注册设备数与绑定状态
  - **修复 HA 配置/选项向导 `[value, label]` 二元组下拉框参数校验报错 (`onboarding_tools.py` / `app.js`)**：兼容 `vol.In({...})` 序列化出的二元数组选项，消除 `['pin_binding', 'PIN绑定']` 格式报错
  - **切换阿里云杭州公开 ACR 预构建镜像分发**：国内轻主机安装与更新无需现场构建或跨境拉取底座，10 秒直拉完成

## 0.3.9 (2026-11-25)
- **轻主机 Debian 原生 `glibc` 底座升级、内置独立子进程华为桥接引擎与远程隧道并发修复**：
  - **轻主机容器升级为 Debian 12 Bookworm (`Dockerfile` / `tools/export_binary_addon.py`)**：彻底解决 HAOS Alpine (`musl`) 缺少 `ld-linux-aarch64.so.1` 导致华为 `libhilink_bridge.so` 无法加载的问题
  - **内置独立子进程华为鸿蒙智家反向网桥 (`huawei_bridge.py` / `huawei_bridge_worker.py` / `location_ecosystem_tools.py` / `app.js`)**：驱动热更新目录 (`/data/huawei_bridge/driver`) 与配对凭证目录 (`/data/huawei_bridge/storage`) 彻底解耦，支持无需重启 HA Core 的一键下载/在线热更新、8 位 PIN 码获取、网卡自检与实时子进程日志
  - **修复 HA 远程页面 HTTP 与 WebSocket 并发配额冲突 (`bf3fac3`)**：解决远程访问 HA 首页资源间歇性 503 问题
  - **修复 HomeKit 二维码拉取触发 Supervisor 认证刷屏报错 (`ecosystem_bridge.py`)**：优先使用本地离线 `X-HM://` 渲染并绕过 `supervisor/core` 代理直连本机 `127.0.0.1:8123`

## 0.3.8 (2026-11-25)
- **华为「智慧生活」& 鸿蒙智家双向同步向导增强与双仓（Gitee + GitHub）同步发布**：
  - **支持 Options Flow 自动接续与翻译 (`client.py` / `onboarding_tools.py` / `app.js` / `index.html`)**：针对已接入的单实例集成（如 `hwhomebridge` 鸿蒙智家反向网桥与 `huawei_smarthome` 华为设备同步组件返回 `single_instance_allowed` / `already_configured`），点击配置自动无缝拉起其 `Options Flow`（实体勾同步与 PIN 绑定向导），并同步加载 `options` 中文翻译词典
  - **组件下载多分支镜像容错与 HA 重启友好提示 (`installer.py` / `onboarding_tools.py`)**：补齐 `ghfast` / `gh-proxy` 的 `HEAD`、`main`、`master` 多分支归档回退通道；当 HA Core 正在重启或后台安装组件 Python 依赖返回 `502/503` 时给出清晰的中文等待指引

## 0.3.7 (2026-11-25)
- **修复 Home Assistant 2026 Supervisor 加载项商店在线构建镜像兼容问题**：
  - 移除已废弃的 `build.yaml`（原单段镜像名 `"python:3.12-alpine"` 在新版 Supervisor 正则校验下回退至无 Python 的 `ghcr.io/home-assistant/base:latest`，触发 `python3: not found`），改为在 `Dockerfile` 首行直接锁定 HA 官方国内直连多架构基础镜像 `ghcr.io/home-assistant/base-python:3.12-alpine3.21`（不受 `--build-arg BUILD_FROM` 覆盖），并启用 `PIP_BREAK_SYSTEM_PACKAGES=1` 与 `CMD []` 适配 Alpine PEP 668 与 `qing-launcher` 守护入口

## 0.3.6 (2026-11-25)
- **全量兼容原 SA 统一云端体系（云端零改动，双通道直达 + 家庭端接口兼容）**：
  - **「进入 SA」直达轻主机 AI 助手界面 (`connector.py` / `server.py` / `app.js` / `index.html`)**：
    - 云端门户 (`https://cloud.tuojiayi.com/customer` 与 `/maintenance`) 点击 **「进入 HA」** (`target="ha"`) 直达本机 Home Assistant (`:8123`)；点击 **「进入 SA」** (`target="sa"`, `https://sa-<public_id>.<support_domain>/`) 通过进程级一次性随机隧道令牌 (`X-Qing-Tunnel-Token`) 直达本机「轻主机 AI 助手」工作台 (`:8099`)，同时支持 HTTP、长连接 SSE (`/api/v1/events`、`/api/v1/chat`) 与 WebSocket，无需先登录 HA 即可在外网直接使用 AI 助手
    - 本地云端管理弹窗同步提供 **「远程进入 HA」** 与 **「远程进入 AI 助手 (SA)」** 双通道一键新窗口启动按钮
  - **100% 兼容 SA 云端家庭端远程中继协议 (`type="request"` / `policy.py` 白名单)**：
    - 完整实现并对齐原 SA 家庭端契约白名单接口：`GET /api/v1/dashboard/summary`、`GET /api/v1/system/status`、`GET /api/v1/devices`（含 `projection=device_directory.v1` / `device_detail.v1` 与 `action_descriptors`）、`GET /api/v1/rooms`、`GET /api/v1/ai-scenes`、`POST /api/v1/ai-scenes/{scene_id}/trigger`（严格限定 `scene` 域并记录审计日志）、`GET /api/v1/events/recent` 与 `GET /api/v1/energy`，本地二次执行请求体 64 KiB、响应体预算与并发读限流校验，拒绝一切越界路径
    - 同时兼容 `/remote-gateway/{status,pairing/start,pairing/poll,revoke-local}` 原生本地配对接口与页内一键绑定 / `/bind#<pairing_code>` 扫码双绑定路径

## 0.3.5 (2026-11-25)
- **统一云端账号体系与零公网 IP 远程直连 Home Assistant 隧道（兼容 `https://cloud.tuojiayi.com`）**：
  - **共用云端账号与角色权限管理 (`connector.py` / `server.py` / `db.py` / `orchestrator.py`)**：
    - 对接 `POST /v1/auth/login`（家庭客户登录）、`GET /v1/account`（当前账号资料）、`PUT /v1/account/password`（修改密码）、`POST /v1/ops/login`（平台/经销商/运维人员登录）与 `GET /v1/ops/context`（运维角色及经销商成员归属）
    - 登录态 Bearer 令牌严格仅驻留本地进程内存（前端仅持 `HttpOnly` + `SameSite=Lax` 会话 Cookie，永不落盘或下发浏览器）；对话会话 (`chat_sessions.user_id`) 与安全审计日志统一关联云端 `user_id`，家庭成员 (`member`) 与户主/运维 (`owner`) 权限实时联动安全门禁
  - **零外部 C 依赖 Ed25519 X.509 证书链校验与直连 HA 加密隧道 (`connector.py` / `config.py`)**：
    - 内置纯 Python RFC 8032 Ed25519、PKCS#8/SPKI PEM 与 X.509 v3 DER 证书链验证器（无需额外 C 依赖，保持 25 个 `.so` 模块与 100% 离线打包体积）；支持页内一键家庭/经销商交付绑定与 `/bind#<pairing_code>` 扫码绑定
    - 建立出站 `wss://cloud.tuojiayi.com/v1/gateway/connect` 挑战签名隧道，直接将 `target="ha"` 的 HTTP 与 WebSocket 流量（含 >48KB 大帧自动分片重组）转发至本地 Home Assistant Core（无需独立 SA 中间层）；若在云端门户误点「进入 SA」，自动返回中文引导页提示点击「进入 HA」；收到云端 `revoke` 或 `4401`/`4403` 时立即销毁本地私钥并停止重连
  - **前端云端远程访问与账号工作台 (`index.html` / `app.js` / `styles.css` / `ecosystem_bridge.py`)**：
    - 顶栏新增云端状态胶囊按钮，快速接入中心新增「云端统一账号与手机远程访问 HA」卡片与配置弹窗（支持客户/经销商双模式登录、在线改密、一键绑定/解绑、签发单次票据一键外网打开 HA），并更新苹果 HomeKit / 华为生态桥接指引说明

## 0.3.4 (2026-11-24)
- **两轮全量深度审查闭环修复与移除虚拟测试沙箱（正式物理设备交付版）**：
  - **彻底移除测试期虚拟沙箱 (`qing_sim_lab` / `sim_tools`)**：删除模拟集成、沙箱工具及前端沙箱控件，成品二进制包实现 **100% 零业务 `.py` 源码文件**；历史旧机若残留空闲 `custom_components/qing_sim_lab` 目录将在启动时自动无感清退
  - **诊断中心、脱敏引擎与云端上报安全加固 (`diagnostics.py` / `net.py` / `server.py` / `app.js`)**：
    - 修复前端「实时运行日志」因 `log_tail` 字符串/数组类型判断不一致导致恒显示为空的问题，并修复 `pending_confirmation` 草稿调用在审计面板误标黄、`.seg-tabs` 样式冲突及缺失 `.chip-meta` / `--text-muted` 样式问题
    - 封堵 `upload_diagnostic_bundle` 的 HTTP `307` 重定向协议降级 SSRF、公网域名重绑定至 `127.0.0.1`/局域网（启用 `public_wan_only=True`）及响应体无上限读取风险；补齐 `recent_sessions.json` 中 `tool_calls`、混合单双引号密码、URL 内嵌账密、独立 JWT 与 HomeKit 8 位 PIN 的递归脱敏
    - 收紧 `POST /api/v1/diagnostics/client_error` 权限与 `context` 4KB 上限，将诊断 `.zip` 构建移入后台线程执行避免阻塞事件循环
  - **时光机恢复保护、AI 编排协议与设备/Zigbee 控制修复 (`gate.py` / `orchestrator.py` / `device_tools.py` / `zigbee.py` / `main.py` / `license.rs`)**：
    - 修复时光机「清理失效记录 (`mode="stale"`)」误删所有未回滚的“删除场景/自动化”恢复快照的缺陷
    - 修复对话达到 `MAX_TOOL_ROUNDS` 收尾总结在 DeepSeek / OpenAI 严格网关下报 HTTP 400 的消息序列问题，以及流式并行 `tool_calls` 同 `index` 重映射后续参数分片错位问题；修复删除流式会话竞态与停止容器时 `/api/v1/events` 长连接阻塞 `on_cleanup` 的问题
    - 支持 `call_service` 自动解析中文房间名及房间别名 `target.area_id`；打通全链路房间 `aliases` 检索；修复 Zigbee TCP 协调器首字节分包误判、在线网关探测发送 `ASH RST` 干扰及 `6638` 端口 EFR32 mDNS 主机名丢失误配问题
    - 修复配置页非法 `log_level` 持久化崩溃循环、Rust `qing-launcher` 多字节 UTF-8 字符串字节切片 Panic 及 `Dockerfile` / `build.yaml` `BUILD_FROM` 声明顺序

## 0.3.3 (2026-11-23)
- **全库函数签名与跨层接口契约终审收口**：
  - **修复前端 SSE 回调拼写不一致**：修复 `app.js` 在收到 `change.applied` / `change.rolled_back` 事件时调用 `loadScenesAndAutos()`（应为 `loadScenesAndAutomations()`）导致「场景与自动化」页不自动刷新的问题，并同步对齐 `index.html` 首屏静态版本占位符
  - **支持自动化/场景房间重置回「全屋通用」**：修复可视化工作台及 `update_automation` / `update_scene` 将已绑定房间的规则改回「全屋通用」（空字符串）时未向 HA 实体注册表清空 `area_id` 的问题
  - **补齐工具 JSON Schema 与非 UI 脱敏守卫**：为 `update_automation`（`area`）、`update_scene`（`icon`/`aliases`）、`capture_scene_from_current`（`domains`/`aliases`）、`search_entities`（`device_classes`）、`create_script`（`fields`）及 `stop_pairing`（`protocol`）补齐参数声明；为 `submit_flow_step` 与 `sync_huawei_bridge_cache` 补齐受信任 UI 通道保护与敏感字段脱敏
  - **Rust `qing-launcher` 隔离与自动回退完善**：子进程改用 `python3 -I -B -u` 完全隔离模式（免疫 `PYTHONPLATLIBDIR` 等外部环境变量干扰）并将 `stdin` 置为 `Stdio::null()` 消除交互式 TTY `SIGTTIN` 挂起风险，10 秒超时按 `-pid` 清理整个子进程组，OTA 静态校验失败时支持自动回退 `previous.txt`

## 0.3.2 (2026-11-22)
- **AI 主机外网隧道全兼容与 18 项深度审查闭环加固**：
  - **外网穿透隧道兼容与多层写接口防护（`server.py` + `app.js`）**：
    - 支持 AI 主机云端设备域名隧道 / FRP `host_header_rewrite` / 非标端口反代访问：优先信任浏览器 `Sec-Fetch-Site: same-origin` 同源证明与前端自定义请求头 `X-Qing-Client: webui`（强制触发跨域 CORS 预检阻断），同时严格拦截 `Sec-Fetch-Site: same-site`/`cross-site`、`Origin: null` 及所有携带非 `application/json` `Content-Type` 的 HTML `<form>` 写请求（含空请求体），修复畸形 IPv6 `Origin` 头导致的 500 异常
    - 兼容前置 SSO 反代自定义 `X-Remote-User-Groups` 组名，防止已通过 `panel_admin: true` 校验的管理员被误降级锁死；支持局域网免密本地模型（Ollama / vLLM）留空 API Key 直接对话；删除流式会话时立即中止对应后台 LLM 任务
  - **华为 Matter 与苹果 HomeKit 跨生态桥接稳定性升级（`ecosystem_bridge.py` + `app.js`）**：
    - 消除已装 `3fd9e6b0_hamh` (`v2.0.60`) 下的无效直连多地址轮询与启动预热锁阻塞（耗时从 >60s 降至秒级返回 Ingress 通道），新建 Matter 网桥自动选取空闲端口（默认 `5542` 起，避开官方 `core_matter_server` 占用的 `5540`）并自动修复端口冲突网桥，前端补齐 Ingress 建桥异常透出
    - 修复已绑定苹果 HomeKit 条目仍合成失效二维码或跨条目串用配对通知、以及未重置配对时误弹“二维码已就绪”提示的问题
  - **Rust `qing-launcher` 优雅停机、硬件指纹与离线打包加固（`supervisor.rs` / `ota.rs` / `fingerprint.rs` / `export_binary_addon.py`）**：
    - 修复信号处理双重发送 `SIGTERM` 打断 Python `on_cleanup` 导致 `code=143` 退出及 PID-1 `waitpid(-1)` 竞态误回滚 OTA 的问题；锁定 OTA `release_root` 顶层白名单防 `sitecustomize.py` 注入，剥离 `LD_LIBRARY_PATH` 并传入 `python3 -s` 与锁定 `DATA_DIR`
    - 硬件指纹仅采纳板载焊接 `eMMC`（`device/type=MMC`，排除外插 TF 卡）与内核永久 MAC `perm_addr`，提升 `amd64` `eno*`/`ens*` 有线网口优先级并降权 USB 网卡；离线导出包按架构自动隔离 `wheels` 镜像、收敛单架构 `config.yaml` 并补齐 `translations/en.yaml`
  - **安全门禁、时光机纯数据库清理与沙箱状态同步（`gate.py` / `client.py` / `db.py` / `sim_tools.py` / `ids.py`）**：
    - 时光机「清理失效记录」严格限定为纯本地数据库清理（不再触碰线上 HA 规则），区分 HTTP `404` 与瞬时 `5xx`/超时防误删回滚点，并覆盖已删对象的 `update_*` 记录；WS 闪断重连窗口对非可信通道回滚实行 Fail-Closed，扫描 `!secret` 标签与列表型场景实体；清除虚拟测试设备后实时推送 `draft.updated` SSE 灰化聊天残卡，审计日志补齐 Matter 驼峰配对码脱敏

## 0.3.1 (2026-11-21)
- **全量深度代码与商业化安全壳审查加固（22 项闭环修复）**：
  - **Rust 商业化安全壳 (`qing-launcher`) 与离线二进制分发加固**：
    - `fingerprint.rs`：修复无硬件特征回退分支读取 `/dev/urandom` 无上限阻塞导致容器无法启动的致命缺陷（改为定长 16 字节 `read_exact`），并严格校验 `/sys/class/net/<iface>/device` 物理网卡符号链接且排除 `02:42:` 容器虚拟 MAC，确保设备指纹 100% 稳定绑定宿主机物理硬件
    - `ota.rs` / `license.rs` / `supervisor.rs` / `main.rs`：OTA 包验签升级为递归统计完整目录树 SHA-256（拒绝软链接、校验 `arch` 与 `min_launcher_version`、启用 `verify_strict` 防签名延展性），`enforced` 授权模式强制锁死 `/data` 目录并剥离 `PYTHONSTARTUP`/`PYTHONHOME`/`LD_PRELOAD` 注入环境变量，补齐 PID 1 孤儿僵尸进程回收、修复 `SIGTERM` 竞态窗口并将 OTA 自动回退级数提升至 3 级（`current -> previous -> builtin`）；`license_tool.py` 新增 `ota-sign` 子命令
    - `export_binary_addon.py` / `minify_static.py` / `Dockerfile`：导出的商业零源码二进制安装包内置预下载 `aarch64` Python wheels（`--no-index --find-links`，客户盒子零公网依赖、零明文 HTTP 风险），静态资源自动注入内容哈希防缓存陈旧
  - **Ingress 单管理员门禁、CSRF/SSRF 防护与 SafetyGate L3 收口**：
    - `config.yaml` / `server.py` / `config.py`：显式声明 `panel_admin: true` 并结合 `X-Remote-User-Groups` 纵深校验管理员/成员/访客权限，拦截跨站 `Sec-Fetch-Site: cross-site` / `Origin` 与非 `application/json` 表单 CSRF 请求，拦截大模型 `base_url` 指向 `supervisor` / `172.30.32.0/23` 的内部控制面 SSRF，修复 `EventBus` 20s 心跳超时导致 SSE 事件流退订断连的缺陷及流式期间孤儿草稿重复恢复竞态
    - `gate.py` / `db.py`：回滚覆盖或删除 HA 现网规则前实时拉取现网配置复核 L3 风险（防借旧 L2 记录回滚抹除后期人工升级的安防规则），补齐 `xiaomi_home`/`esphome`/`automation.turn_on`/`homeassistant.set_location` L3 判定，豁免 `sun` 触发器 `event: sunset` 字段误报，按 `device_id` 配对合并前后型号保护真实设备记录，支持两趟清理「虚拟测试场景 + 调用该场景的测试自动化」
  - **HA 集成、跨生态桥接与前端体验完善**：
    - `client.py` / `engine.py` / `ecosystem_bridge.py`：新增兼容 `!secret`/`!input`/`!include` 的 `_HASafeLoader`，删除场景/自动化/脚本后自动清除 HA 实体注册表残留的 `restored: true` 僵尸项，分块校验完整 `</svg>` 读取 HomeKit 配对二维码并支持 Options Flow 更新同步品类，支持华为 Matter 网桥 `PUT` 动态更新过滤品类；前端补齐流式切会话 `AbortController`、弹窗 Promise 清理与移动端 `100dvh` 适配

## 0.3.0 (2026-11-20)
- **修复测试设备/场景清理后时光机回滚残留及点击回滚报 `HA 接口返回 400: Resource not found` 的问题**：
  - **一键清除测试沙箱全链路无痕清理**（`sim_tools.py` + `db.py`）：`cleanup_test_devices` 清理虚拟测试设备、测试场景与测试自动化（含结合 `sun.sun` 与虚拟传感器的纯测试联动）时，同步清理 SQLite `changes`（时光机变更记录）、`drafts` 与 `snapshots` 中的纯测试记录，同时完整保留真实物理设备的变更记录
  - **幂等容错回滚**（`client.py` + `gate.py`）：回滚新建场景/自动化/脚本或已卸载设备的批量整理时，若目标已在 HA 侧被提前删除（HA 返回 `400: Resource not found` 或 `404`），自动按幂等删除成功处理并标记为已回滚，不再抛错卡死
  - **时光机面板新增清理控件**（`server.py` + `index.html` + `app.js`）：新增 `🧹 清理失效记录`（一键清除已回滚及目标已删除的残留项）、`🗑 清空` 与单条记录右侧 `✕` 移除按钮

## 0.2.9 (2026-11-20)
- **最终轮全面审查收口加固**：
  - **场景 L3 门禁彻底对齐与防 500**：`gate.py` 将 `assess_scene_risk` 与 `apply_entities_live` 统一复用 `_entity_touches_high_risk`（封堵借场景重放停用 `automation.*` 或触发 `script.*`/`group.*` 绕过 L3 门禁），兼容手写 `scenes.yaml` 字符串简写，并将 `confirm_token` 的 `secrets.compare_digest` 升级为 UTF-8 字节对比以消除非 ASCII 字符 500
  - **配置容错与跨生态缓存收口**：`config.py` 提前 `reload()` 的非 dict 节规范化与 `provider` 字符串校验，并修复 `base_url: null` 误清 `api_key`；`ecosystem_bridge.py` 校验 `_last_working_ing_prefix` 必须属于当前会话有效候选前缀且在 `json.loads` 成功后再落缓存
  - **工具与运行时细节完善**：`device_tools.py` 前置域白名单校验并为停用安防实体保护补齐实体注册表 `device_class` 回退；`scene_tools.py` 的 `capture_scene_from_current` 补齐 `area`/`domains` 类型校验；`net.py` 捕获非法 IPv6 URL 的 `urlparse` 异常；`engine.py` 防御非序列实体能力属性切片；`main.py` 在 `ha.close()` 后补取消防抖刷新任务；`installer.py` 动态引用 `__version__`
  - **前端最终细节收口**：`app.js` 补齐 `renderDraftCard` 对 `create_script` 的互斥判定、拒绝 `_canRepresent*InVb` 中非 plain object 的模板 `data`/`target`、`addVbTriggerRow`/`addVbConditionRow` 按过滤后首实体匹配状态下拉、补齐 `#flowModal`/`#dialogModal` 代际防串台与会话/设置异步异常捕获；`styles.css` 修正浅色主题 3 处文本对比度

## 0.2.8 (2026-11-20)
- **第 4 轮全面核查收口加固与回归修复**：
  - **封堵 L3 草稿降级与权限门禁残留绕过**：
    - `scene_tools.py`：`test_scene` 禁止修改 `delete` 场景草稿与 `L3` 高危场景草稿、禁止降级已有 `L3` 风险等级，并对返回给模型的 `updated_draft` 统一剥离敏感确认令牌
    - `gate.py`：`homeassistant.turn_off`/`toggle` 指向 `automation.*`（含经 `group.*` 间接包含）及非字典模板 `target`/`data`/`data_template` 一律升级为 `L3`
    - `device_tools.py`：`call_service` 拦截非 UI 通道通过 `script.turn_on/off/toggle` 传入 `group.*` 等非 `script.*` 实体绕过逐个脚本扫描
    - `config.py`：封堵 `custom` 服务商先清空 `base_url` 再切换新地址分两步绕过自动清空旧 API Key 的漏洞，并校验 `/settings` 字段类型防配置损坏
    - `orchestrator.py`：`custom` 服务商未填 `base_url` 时直接阻断提示配置错误，避免将自定义密钥发往通义千问默认地址
  - **修复 3 处 v0.2.7 回归与边界健壮性**：
    - `zigbee.py`：修复 ZHA 发现流（`discovery_flow_id` 且无 `port_hint`）因空 `port` 误报 `INVALID_PARAMS` 的回归，并在诊断读取损坏 `configuration.yaml` 时安全容错
    - `ecosystem_bridge.py`：缓存首个成功的 Ingress API 前缀 `_last_working_ing_prefix`，修复 `POST` 建桥未走工作前缀导致 404 的回归；`location_ecosystem_tools.py` 同步校验 `comm.qrCode` / `bridge.qrCode` 必须符合 `MT:` 格式
    - `server.py` / `engine.py` / `db.py` / `main.py`：校验 `session_id` 字符串类型、统一 `apply_draft_handler` 使用 `_read_json_dict`、优化设备实体索引签名为 $O(1)$ 采样、清理退出时防抖刷新任务并避免吞掉 `CancelledError`
  - **前端可视化编辑器与交互细节收口**：
    - `app.js`：`renderDraftCard` 改为优先依据 `payload.kind`/`tool_name` 互斥识别卡片类型（修复名称含“场景”的自动化误判）；收紧 `_canRepresentSceneActInVb`/`_canRepresentDeviceActInVb` 顶层键白名单、服务域与实体域一致及空调参数完整性（防止 `homeassistant.turn_off` 对 `group.*`、未知场景或带 `enabled: false` 的动作失真）；修复 `applyVbQuickTemplate` 重置 `extraMeta`、空 `binEid` 回归与非 `light.*` 附加亮度问题；修复延迟字符串拼接与负数输入、关闭 L2 二次确认时的 UI 直达反馈、跨生态弹窗竞态防护、中文输入法 IME 回车防护与异步点击异常捕获

## 0.2.7 (2026-11-19)
- **第 3 轮对抗性深度审查全量加固**：
  - **封堵密钥回灌与配对码泄露**：修复 [config.py](app/config.py) 在 Web UI 切换服务商/接口地址或显式清除密钥后 `reload()` 被 `options.json`/环境变量旧密钥回填覆盖的漏洞；`get_ecosystem_bridges_status` / `setup_apple_home_bridge` / `setup_huawei_bridge` 对非 UI 通道全面脱敏 HomeKit PIN 与 Matter 配对码并禁止 AI 桥接门锁/安防设备；`submit_or_apply`、`orchestrator.py` 与 `cloud/connector.py` 彻底剥离发往 LLM、云端和聊天表的 `confirm_token`
  - **封堵 L3 门禁高级绕过与单轮自批**：`SafetyGate` 全面拦截 `scene.apply`/`scene.create` 模板 `entities` 与 `snapshot_entities`、`data`/`data_template` 广域目标、`entity_id: "all"`、`event` 发射动作、`zha`/`zwave_js`/`matter`/`recorder`/`pyscript` 等底层高危域、`automation.turn_off`/`toggle`/`reload`，并对 `scene.*`/`group.*` 执行忽略大小写递归展开与 Fail-Closed 校验；`orchestrator.py` 禁止单轮对话内自批刚生成的草稿；`call_service` 封堵 `entity_id` + `area_id` 并集目标绕过；`delete_automation`/`delete_scene`/`update_*` 同步审查原配置 (`before`) 风险，`delete_area` 与 `configure_zigbee_gateway` 限制为受信任人工 UI 操作，禁止 AI 停用安防实体或关闭高危自动化
  - **HA / Zigbee / 安装器 / 跨生态与基础层加固**：`zigbee.py` 封堵 `skip_tcp_check=True`、十六进制 IP（`0x...`）、公网域名、非 RFC1918 保留段与 DNS Rebinding（落盘直写已校验 IP），校验本地串口白名单与 `discovery_flow_id` 必须为 `zha`，修复 Z2M 2.x 写回覆盖 `!include`、空选项覆盖与 `_YamlTaggedScalar` JSON 序列化 500；`installer.py` 启用逐跳 HTTPS+可信域名白名单重定向校验、校验 `manifest.json` 的 `domain` 一致性并将目录计入条目上限防 inode 炸弹；`ecosystem_bridge.py` 加固 `pairingqr` 路径与禁重定向、升级 `sync_huawei_bridge_cache` 为 `owner` + `MT:` 格式校验、避免非幂等 `POST` 重复建桥、脱离请求 `ContextVar` 启动后台拉镜像任务并兼容 Supervisor 2026 `/apps`；`client.py` 强制 WS 握手 `auth_required`；`location.py` 钳位对跖点计算避免 `ValueError` 500；`sim_component` 支持 `EFFECT_OFF` 与数值型 `binary_sensor`
  - **事务一致性与并发稳定**：`db.py` 合并 `complete_draft_apply` 单事务提交、`claim_draft_applying` 原子返回最新草稿消解 TOCTOU、统一守卫 `expire_draft_if_pending` 与过滤过期 `list_drafts`；`engine.py` 在 `refresh_all` 窗口保留实时 `state_changed` 事件、加锁防抖设备注册表更新并全面防御脏 HA 实体属性；`ids.py` 线程安全化 `new_ulid()`、修复 `safe_int`/`safe_float` 的 `Infinity`/`bool` 边界并统一 `safe_str`/`safe_str_list` 防参数 500；`server.py` 统一校验 JSON 请求体并限制后台 SSE 队列上限；`main.py` 退出时先等待后台任务取消再关闭数据库
- **前端严重交互与编辑器保真修复**：
  - 提升 `#dialogModal` 层级（`z-index: 100` 并移至弹窗最末），彻底解决可视化编排保存 L3 自动化与苹果家庭重置时二次确认框被遮挡死锁的问题
  - 为自动化可视化编排器补全 trigger/condition/delay/scene 的严格无损可表达性校验（不再反转白天 `sun` 条件、不再把秒级/模板 `delay` 改成 5 分钟、保留顶层 `variables`/`max`/`description`、支持 `button.press` 与 `valve.*` 控件），修复 `update_automation` 草稿缺失 `automation_id` 与设置页未配密钥误报红色告警回归
  - 强化 `safeHref`/`safeImageSrc` 拦截 `/\` 与控制字符 WHATWG 协议相对绕过，优化设备筛选互斥、重命名保留筛选、华为轮询串行化与弹窗代际防串台、SSE 断线重连刷新会话与中文 IME 回车防护

## 0.2.6 (2026-11-19)
- **回归修复与对抗性安全加固（Fail-Closed 深度防御）**：
  - **修复外网报错回归缺陷**：修复 `orchestrator.py` 在大模型外网异常分支调用 `diagnose_wan_client_error` 时参数顺序颠倒且缺失 `await` 的严重回归，并按当前会话过滤待确认草稿提示、避免工具长输出被截断为非法 JSON
  - **全链路通道/角色默认拒绝 (Fail-Closed)**：统一 `TRUSTED_UI_CHANNELS = {"local_ui"}` 白名单，`ToolRegistry.call()` 对空串/大小写变形/未知通道一律拒绝调用 `expose_to_llm=False` 工具，缺失 `role` 统一降级为 `"guest"` 并下传至处理函数（封堵 `get_ecosystem_bridge_status` 未带角色时泄漏 HomeKit/Matter 配对码、非 UI 重置苹果配对、非 UI 回滚高危变更及非 UI 删除虚拟组件驱动等绕过）
  - **封堵 L3 安全门禁变形绕过**：在 `SafetyGate` 风险扫描前先做动作/触发归一化并保留 Jinja 模板原大小写，独立扫描 `action`/`service`/`service_template`、识别 `{%` 控制块及 `mqtt`/`hassio`/`shell_command`/`rest_command`/`python_script`/`script`/`automation.trigger`/`homeassistant.restart|stop` 与按 `area_id`/`floor_id`/`label_id`/`device_id` 广播控制；`test_scene` 在写库和推送 SSE 前拦截 L3 实体；`call_service`/`run_script`/`trigger_automation` 对非 UI 通道执行失败默认拦截
  - **消除安装器、Zigbee SSRF 与跨生态桥接风险**：`installer.py` 改为按实际解压写入字节流式校验并拒绝符号链接与非 HTTPS 重定向降级；`zigbee.py` 解包 `::ffff:*` IPv4-mapped IPv6、拦截 `supervisor.`/`core-*`/短数字 IP/公网 IP 并对主机名先解析校验再直连已校验 IP 防止 DNS Rebinding；收窄 `!secret` 去引号正则并保护顶层 `!include` 段；`ecosystem_bridge.py` 默认 HomeKit 桥接剔除 `lock` 门锁、仅管理 `bridge` 模式条目并修复重置删除失败时重复建桥的问题，Matter 本地插件默认 `allow_local_access: false`
- **稳定性、并发与前端体验修复**：
  - 数据库启动自动恢复崩溃遗留的 `applying` 草稿与半回滚记录，`apply_draft`/`rollback_change`/`discard_draft` 全面原子化并清理 `chat_messages` 历史上限；`ContextEngine` 引入 `device_id -> entities` 索引消除 $O(N^2)$ 扫描并防止高频事件防抖丢刷新；`config.py` 修复 `https -> http` 降级未清旧密钥与 `options.json` 空串覆盖 UI 密钥问题；`net.py` 改用 `secrets` 生成 DNS 事务 ID、循环读取完整 DoH 响应并限制 DNS 缓存上限
  - 前端修复 `safeHref`/`safeImageSrc` 拦截 `//` 协议相对链接及 `qrImg.src` 校验、弹窗样式类 `.modal-wide`、`.tool-trace-bar` 样式拼写、切换服务商清空旧密钥提示、Tab2 自动化动作测试拉取完整配置校验高危、可视化编辑器严格字段白名单保护、手动定位默认值及华为安装进度轮询定时器泄漏

## 0.2.5 (2026-11-19)
- **全模块安全加固（HA Ingress 专属隔离与人机权限分离）**：
  - **强制 HA 内部运行隔离**：在 HAOS 环境下优先仅监听 `hassio` 内部网桥地址（`172.30.32.1`），并由最外层中间件强制校验请求来源必须为 HA Supervisor Ingress（`172.30.32.2`），彻底封堵局域网外部直连 `:8099`；本地开发模式默认仅监听 `127.0.0.1` 回环；`ingress_session` 升级为单请求 `ContextVar` 隔离
  - **封堵 AI 自确认与高危绕过**：废除固定确认口令，升级为每份 L3 草稿独立签发一次性加密令牌且禁止大模型通道提交确认；`ToolRegistry` 强制拦截 `expose_to_llm=False` 工具调用与未知角色；补全 Device Action、`homeassistant.*`、模板服务与场景高危实体的 L3 风险识别；拦截 `install_custom_component` 自定义仓库越权安装并新增解压炸弹防护
  - **防止密钥外泄与隐私落盘**：切换大模型服务商或修改接口域名但未重填密钥时自动清空旧密钥；审计日志自动递归脱敏密码、令牌与验证码
- **数据保护与核心功能缺陷修复**：
  - 修复 Zigbee2MQTT `configuration.yaml` 含 `!secret` 自定义标签时重写丢失 `network_key` 与已配对子设备的问题（支持自定义标签原样保留、损坏中止保护、`.bak` 自动备份与原子落盘），并修正 SONOFF Dongle-E (`Dongle_Plus_V2`) 驱动识别与 `config_entries/disable` WebSocket 命令名
  - 修复前端定位手动校准经纬度参数反传、可视化自动化编辑器回存覆写复杂动作（新增 `vacuum.stop` 选项并对超范围动作自动切换原样保留）、二维码/外部链接安全协议白名单及弹窗关闭挂起问题
  - 开启容器 `init: true` 进程回收并恢复构建阶段 PyPI HTTPS 证书校验

## 0.2.4 (2026-11-19)
- 修复 HA Core 日志报告 `Failed to load services.yaml for integration: qing_sim_lab` 的错误：为内置虚拟测试沙箱组件补全标准 `services.yaml` 服务描述定义、`strings.json` 与 `translations/zh-Hans.json` / `en.json` 多语言元数据，并升级 `sync_sim_component_files` 递归同步 `.yaml` 与翻译子目录

## 0.2.3 (2026-11-17)
- 将「快速配网」页面及配置弹窗中的苹果「家庭」与华为「智慧生活」水果/花朵 Emoji 图标升级为高清官方品牌矢量 SVG Logo（适配深浅色双主题玻璃质感与底部按钮右对齐）

## 0.2.2 (2026-11-17)
- 修复 Apple 苹果「家庭 (Home)」配对弹窗在 HA Core `2026.x` 下误显示「已绑定成功」占位框的问题：
  - 新增解析并内联拉取 HA Core 官方受保护接口 `/api/homekit/pairingqr?<entry_id>-<secret>` 生成的原生 HomeKit 配对矢量二维码（转为离线 `data:image/svg+xml;base64,...`），并兼容 `homekit.<entry_id>.state` 裸字典状态与 `options.filter.include_domains` 结构
  - 当配对通知曾被关闭时自动重载 HomeKit 条目恢复二维码，前端仅在真实 `paired=true` 时才显示「已绑定成功」

## 0.2.1 (2026-11-17)
- 新增 **全主机出厂级国内零 GitHub 依赖 + 多源容器镜像加速引擎**（彻底根治新主机在国内网络环境下部署华为 Matter 网桥卡顿/超时问题）：
  - 挂载本地 `/addons` 目录并在启动时自动生成内置本地插件 `local_qing_matter_hub`（零 `github.com` `git clone` 依赖，即便外网不通 GitHub 也可秒级识别）
  - 内置 **南京大学官方国内高速镜像源 (`ghcr.nju.edu.cn`) → 国内毫秒镜像源 (`ghcr.1ms.run`) → GitHub 官方源 (`ghcr.io`)** 三级自动容灾切换，彻底绕开海外 `ghcr.io` 在国内无 Docker Hub 镜像加速导致的下载停滞问题，并实时刷新下载百分比
  - 新增后端 HA `ingress_session` 会话自动透传与前端同源 Ingress 双重通道，无论在图形弹窗还是对话聊天中均可无感穿越 HAMH `172.30.32.2` IP 白名单一键建桥并生成二维码

## 0.2.0 (2026-11-17)
- 修复华为「智慧生活」Matter 跨生态桥接首次部署时阻塞等待镜像拉取导致页面卡住的问题：升级为后台异步安装与 Supervisor 实时下载百分比轮询，自动开启 `allow_local_access` 与宿主机本地回环直连通道，消除多余的全局仓库重载阻塞，秒级创建网桥并渲染 `MT:...` 扫码二维码与 11 位数字配对码

## 0.1.9 (2026-11-17)
- 新增 **中国地理定位校准与精准日出日落引擎**（`LocationSunManager` + `get_location_sun_status` / `calibrate_location`）：自动检测 HA 海外出厂默认坐标（阿姆斯特丹 `52.37°N, 4.89°E`）与时区偏差，内置全国 100+ 省市标准 WGS-84 经纬度与海拔离线秒选库、高德/腾讯火星坐标 (`GCJ-02`) 与百度坐标 (`BD-09`) 自动纠偏转换、国内 IP 智能探测防代理污染保护，以及本地 NOAA 天文日出/日落/建议亮灯时间实时计算；同时在可视化自动化工作台新增「处于日落后天黑期间（含提前偏移）」条件
- 新增 **Apple 苹果「家庭 (Home)」App & 华为「智慧生活」App 跨生态一键智能桥接中心**（`EcosystemBridgeManager` + `setup_apple_home_bridge` / `setup_huawei_bridge` + 离线高清矢量二维码引擎 `qrcode_svg`）：
  - **苹果「家庭」与 Siri**：基于 HA 原生 `HomeKit Bridge` 一键配置勾选品类，自动从通知或 `.storage` 提取 `pincode` 与 `X-HM://` 载荷并离线生成高清配对二维码（支持随时找回与一键重置配对）
  - **华为「智慧生活」与小艺**：基于 Supervisor 自动挂载并启动 `Home Assistant Matter Hub` 跨生态网桥引擎，自动剔除 `diagnostic/config` 冗余噪音实体，一键生成标准 `MT:...` Matter 二维码与 11 位数字配对码供华为智慧生活扫码同步

## 0.1.8 (2026-11-17)
- 修复 HA Core 2025/2026 WebSocket `validate_config` 接口复数键名规范（`triggers` / `conditions` / `actions`，并兼容旧版单数键名回退），彻底解决 AI 创建自动化时因 `INVALID_FORMAT` 误报错导致的反复重试卡顿循环
- 修复阿里云百炼 MaaS / 代码模型流式工具调用中 `function.arguments` 参数截断或拼接导致次轮触发 `The "function.arguments" parameter of the code model must be in JSON format.` 的报错，新增参数 JSON 净化保障与 `data:` 流式错误解析
- 修复切换 Home Assistant 侧边栏/窗口后对话回复与草稿卡片丢失的问题：`chat_sse_handler` 升级为后台独立协程继续执行并实时增量落盘，完整还原历史工具调用轨迹、诊断报告与草稿卡片，自动找回未挂载的待确认草稿并自动更新「新对话」标题

## 0.1.7 (2026-11-17)
- 修复多模彩光灯具（同时支持色温 `color_temp_kelvin` 与全彩 `rgb_color` 的灯带/彩光灯）在「恢复试前状态 (`restore_snapshot`)」及直接服务调用时触发 HA Voluptuous `two or more values in the same group of exclusion 'Color descriptors'` 的冲突报错：快照按 `color_mode` 精准记录单一活动色彩模式，并在 `apply_entities_live` 与 `normalize_light_color_temp` 实施全链路互斥清洗（兼容旧快照无缝恢复）

## 0.1.6 (2026-11-17)
- 优化品牌接入向导完成弹窗与全局对话框 UI：采用自适应换行的 `.flow-result-card` 替换单行胶囊，彻底消除长文案裁剪与横向滚动条，清理双层括号冗余标题，并新增「前往全屋设备分房间」一键跳转按钮；同时优化全屋设备表格操作按钮单行紧凑排布
- 智能识别扫地机器人配套自清洁基站（`Dock`）：自动标注「配套基站」角标，支持给扫地机主机分配房间时自动同步归入配套基站，并在 AI 批量改名中支持将 `xxx Dock` 自动规范为 `xxx 自清洁基站`

## 0.1.5 (2026-11-17)
- 顶栏品牌区与系统配置页实时显示 **轻主机 AI 助手当前版本号 (`v0.1.5`)**，方便直观确认线上生效版本
- 修复虚拟测试沙箱 `qing_sim_lab` 配置流提交字段与 HA Core Voluptuous Schema (`devices: str`) 的严格类型对齐问题，完成全模块合并与回归校验

## 0.1.4 (2026-11-17)
- 新增 **🧪 虚拟测试设备沙箱**（`qing_sim_lab` 内置模拟集成 + `provision_test_devices` / `set_sim_sensor_state` / `cleanup_test_devices` 工具）：支持一键在 HA 中生成真实可控的**客厅吸顶主灯、氛围灯带(RGB)、防眩射灯、人在存在传感器(含光照度 lx)、温湿度计、智能窗帘、玄关门窗传感器与筒灯、主卧吸顶灯**，支持在全屋设备页一键模拟“有人/无人、开门/关门、暗光/明亮、高温/低温”真实触发自动化联动，并在测试结束后**一键无痕卸载清理**（可选连同纯测试场景/自动化一并删除）

## 0.1.3 (2026-11-17)
- 新增 **品牌扩展组件一键自动下载安装与平滑重启闭环**（`install_custom_component` / `restart_homeassistant`），内置米家官方 `xiaomi_home`、社区 `xiaomi_miot`、美的 `midea_ac_lan`、海尔 `haier`、追觅 `dreame_vacuum`、本地涂鸦 `localtuya` 多源国内加速通道下载、ZIP 安全解压校验、一键平滑重启 HA Core 并在恢复在线后自动接续打开品牌配网向导
- 全新升级 **自动化可视化编排工作台** 与 **可视化联动流程图卡片**：管理中心每条自动化直接展示「触发 WHEN ➔ 条件 IF ➔ 动作 THEN」中文流程图胶囊；新增无代码可视化新建/编辑自动化弹窗（支持常用联动一键模板、按房间选真实设备、空调温控/灯光调光滑块、窗帘/扫地机动作、时间段限制与实时自然语言逻辑预览）

## 0.1.2 (2026-11-17)
- 新增 **Zigbee 网关智能配置向导**（`configure_zigbee_gateway` / `test_zigbee_network_coordinator`），支持本地 USB 协调器自动匹配与局域网 TCP 网络网关（如涂鸦刷机有线网关 `:8888`、SLZB-06 `:6638`）测速直连，完美兼容 Zigbee2MQTT 2.x (`version: 5` / `onboarding` 引导态识别与清除) 及 ZHA 原生网关
- 升级品牌集成 **Config Flow 全流程深度汉化**，支持石头/米家/涂鸦等二维码提取渲染、多选家庭/设备列表、表单输入保留与去空格防呆，并自动过滤泛蓝牙信标噪音（`ibeacon` / `private_ble_device`）
- 新增房间区域的**编辑（改名 + 口语别名）**与**删除**能力（注册 `update_area`、`delete_area` 工具，全屋设备胶囊快捷编辑/删除 +「房间管理」集中弹窗）
- 优化草稿预览全中文设备名与状态呈现（`entity_names` 实时同步）及大模型接口异常（401/402/429/超时）中文可操作提示

## 0.1.1 (2026-11-16)
- 自动隐藏 HA 系统内置虚拟服务与硬件适配器（如 `Sun`、`Home Assistant Core/Supervisor/Host/OS`、`Backup`、`Matter Server` 等 Add-on 容器、宿主机蓝牙 `hci0`、语音 TTS 服务及无实体空壳项），净化全屋设备统计与 AI 上下文
- 优化大家电多子实体降噪：空调面板灯（`panel_light`）、指示灯、蜂鸣器等配置/附属开关不再混入「主控实体」，同时保留按需口语检索与设备级辅控能力关联
- 增强无型号编码设备（如格力局域网编码设备）的 AI 批量中文命名识别（自动结合关联实体域与品牌生成规范中文名）
- 全屋设备页面新增手动「隐藏 / 恢复显示」按钮与「显示已隐藏项」筛选开关，并注册 `set_item_hidden` 工具支持对话隐藏

## 0.1.0 (2026-11-15)
- 首发 V1 本地闭环版本
- 默认集成通义千问（Qwen）并支持任意 OpenAI 兼容接口
- 实现 HA 全品牌通用实体能力自省与物理设备级聚合降噪（支持米家、格力空调、石头扫地机、美的、涂鸦、HomeKit 等全生态设备）
- 实现场景创建、现场试光/试运行（带快照一键恢复）、实景抓拍建场景
- 实现自动化创建、手动触发测试、基于 HA Trace 的智能排错诊断
- 实现 Zigbee 全协调器硬件探测与 ZHA / Zigbee2MQTT 双栈兼容入网
- 实现局域网设备发现与全品牌 Config Flow 动态表单接入向导
- 实现草稿预览确认、历史快照一键回滚与审计日志
