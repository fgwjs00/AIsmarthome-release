ARG BUILD_FROM="python:3.12-alpine"
FROM ${BUILD_FROM}
ARG BUILD_VERSION="0.3.5"
ARG BUILD_ARCH

LABEL org.opencontainers.image.title="轻主机 AI 助手" \
      org.opencontainers.image.description="全品牌设备快速接入与 AI 场景/自动化创建调试助手" \
      org.opencontainers.image.version="${BUILD_VERSION}"

ENV LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /opt/qing_ai_hub

COPY requirements.txt /tmp/requirements.txt
COPY wheels /tmp/wheels
RUN python3 -m pip install --no-cache-dir --no-index --find-links=/tmp/wheels --root-user-action=ignore -r /tmp/requirements.txt && \
    rm -rf /tmp/wheels /tmp/requirements.txt

COPY bin/qing-launcher /usr/local/bin/qing-launcher
COPY app /opt/qing_ai_hub/app

RUN chmod 755 /usr/local/bin/qing-launcher

ENTRYPOINT ["/usr/local/bin/qing-launcher"]
