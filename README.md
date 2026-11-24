# 轻主机 AI 助手 (`qing_ai_hub`) — 官方发布仓库

面向 **PK3566 / RK3566 (`aarch64`) Home Assistant OS 主机** 的全品牌智能家居 AI 助手成品加载项（Add-on）发布仓。

- **当前版本**：`v0.3.4`
- **目标架构**：`aarch64` (`linux/arm64`)
- **交付形态**：零源码原生二进制成品包（Rust `qing-launcher` 守护外壳 + 25 个脱符号 Cython `.so` 原生模块 + 前端混淆压缩 + 内置全量离线 Python 依赖包，支持无外网纯离线安装构建，开箱免激活直接运行）

---

## 安装方式

### 方式一：通过 Home Assistant 加载项商店在线安装（推荐）

1. 进入 Home Assistant 后台 **设置 → 加载项 → 加载项商店**。
2. 点击右上角 `⋮` → **仓库 (Repositories)**，填入本发布仓地址并添加：
   ```text
   https://github.com/fgwjs00/AIsmarthome-release
   ```
3. 刷新页面后找到 **轻主机 AI 助手**，点击 **安装**，勾选 **在侧边栏中显示** 并点击 **启动**。
4. 点击左侧边栏 **AI 助手** → 进入顶部「⚙️ 模型与回滚」填入大模型 API Key（默认支持阿里云通义千问 DashScope）即可立即使用。

### 方式二：纯离线目录部署

将本仓库中的 `qing_ai_hub` 目录完整拷贝至 Home Assistant 主机的 `/addons/qing_ai_hub`，在加载项商店右上角点击 **检查更新** 后即可离线安装（包内已内置全部预编译 `musllinux_aarch64` `.whl` 依赖，无需访问公网 PyPI）。
