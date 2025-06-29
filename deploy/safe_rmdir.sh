export REMOVEDIR=${1}
mpremote fs  rm -rf "${REMOVEDIR}" 2> /dev/null || true