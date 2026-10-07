#!/usr/bin/env bash
# 本地预览：挂载 assets/ 与 nginx.conf 到容器，改文件后刷新浏览器即可，无需重建。
# 用法：deploy/preview.sh [start|stop|restart]   默认 start；端口用 PORT 环境变量覆盖（默认 18000）；BIND 覆盖监听地址（默认 0.0.0.0，局域网可访问）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME=ui-unify-preview
PORT="${PORT:-18000}"
BIND="${BIND:-0.0.0.0}"

stop() { docker rm -f "$NAME" >/dev/null 2>&1 || true; }
start() {
  docker run -d --name "$NAME" \
    -e TZ=Asia/Shanghai \
    -p "${BIND}:${PORT}:80" \
    -v "$ROOT/assets:/usr/share/nginx/html:ro" \
    -v "$ROOT/deploy/nginx.conf:/etc/nginx/conf.d/default.conf:ro" \
    nginx:alpine >/dev/null
  echo "预览已启动：http://$(ip -4 route get 1 2>/dev/null | awk '{print $7; exit}'):${PORT}/  （单文件版 /demo.standalone.html）"
}
case "${1:-start}" in
  start) stop; start ;;
  stop) stop; echo "已停止" ;;
  restart) stop; start ;;
  *) echo "用法: $0 [start|stop|restart]"; exit 1 ;;
esac
