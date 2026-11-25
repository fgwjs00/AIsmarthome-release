# 轻主机 AI 助手 (`qing_ai_hub`) — 官方发布仓库

面向 **PK3566 / RK3566 (`aarch64`) Home Assistant OS 主机** 的全品牌智能家居 AI 助手成品加载项（Add-on）发布仓。

- **当前版本**：`v0.3.9`
- **目标架构**：`aarch64` (`linux/arm64`，Debian 12 原生 `glibc` 底座)
- **交付形态**：零源码原生二进制成品包（Rust `qing-launcher` 守护外壳 + 27 个脱符号 Cython `.so` 原生模块 + 内置子进程隔离华为鸿蒙智家反向网桥引擎 + 前端混淆压缩 + 内置全量离线 Python 依赖包，原生兼容 Home Assistant 2026+ Supervisor 加载项商店一键安装更新，全量兼容 `cloud.tuojiayi.com` 统一云端：「进入 HA」直达 HA，「进入 SA」直达轻主机 AI 助手）

---

## 安装方式

### 方式一：通过 Home Assistant 加载项商店在线安装（推荐）

1. 进入 Home Assistant 后台 **设置 → 加载项（或“应用”） → 加载项商店**。
2. 点击右上角 `⋮` → **仓库 (Repositories)**，填入以下任一官方发布仓地址并添加：
   - **国内高速镜像源（Gitee，推荐国内主机使用）**：
     ```text
     https://gitee.com/fgwjs/aismarthome-release
     ```
   - **国际发布源（GitHub）**：
     ```text
     https://github.com/fgwjs00/AIsmarthome-release
     ```
3. 刷新页面后找到 **轻主机 AI 助手**，点击 **安装**，勾选 **在侧边栏中显示** 并点击 **启动**。
4. 点击左侧边栏 **AI 助手**：
   - 进入顶部「⚙️ 模型与回滚」填入大模型 API Key（默认支持阿里云通义千问 DashScope）；
   - 在生态接入卡片可一键在线下载并启动内置 **华为鸿蒙智家双向桥接引擎**（8 位 PIN 码直出，升级不掉绑定）；
   - 点击顶部「☁️ 云端远程」绑定 `https://cloud.tuojiayi.com` 统一账号，即可在外网通过「进入 HA」访问 Home Assistant、通过「进入 SA」直接打开轻主机 AI 助手。

### 方式二：纯离线目录部署

将本仓库中的 `qing_ai_hub` 目录完整拷贝至 Home Assistant 主机的 `/addons/qing_ai_hub`（或 `/addons/local/qing_ai_hub`），在加载项商店右上角点击 **检查更新** 后即可离线安装（包内已内置全部预编译 `manylinux_aarch64` `.whl` 依赖，无需访问公网 PyPI）。
