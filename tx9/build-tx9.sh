#!/usr/bin/env bash
# Builds the Free My TV APK for the TX9 box (Android 7.1.2) and, with --install, puts it on the TV.
#
#   ./tx9/build-tx9.sh             build only
#   ./tx9/build-tx9.sh --install   build, install on 192.168.0.232 and leave the box free for the switch
#
# Two things about this machine:
#   - the paths below are Windows-style on purpose: Git Bash rewrites POSIX paths in javac's
#     -bootclasspath and the lambda stubs stop being found ("Unable to find method metafactory");
#   - JDK 17 is needed: d8 8.2.2 (build-tools 34) can't read the classes that JDK 21's javac writes.
set -euo pipefail
cd "$(dirname "$0")/.."

TV_IP="${TX9_IP:-192.168.0.232}"
ADB="${ADB:-$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe}"

# The SDK with build-tools 34.0.0 and platform android-34 (the same as CI); falls back to the default one.
if [ -z "${ANDROID_HOME:-}" ]; then
  if [ -d "$(cygpath -u "$LOCALAPPDATA")/Android/Sdk34/build-tools/34.0.0" ]; then
    ANDROID_HOME="C:/Users/Fabio/AppData/Local/Android/Sdk34"
  else
    ANDROID_HOME="C:/Users/Fabio/AppData/Local/Android/Sdk"
  fi
fi
export ANDROID_HOME

# JDK 17 (d8 8.2.2 can't read the classes that JDK 21's javac writes).
is_jdk17() {
  [ -x "$1/bin/javac.exe" ] || return 1
  "$1/bin/java" -version 2>&1 | head -1 | grep -q '"17'
}
local_dir="$(cygpath -u "$LOCALAPPDATA")"
found=""
for j in "${JAVA_HOME:-/nonexistent}" "$local_dir"/Android/jdk17/*/ "/c/Program Files/Eclipse Adoptium"/jdk-17* "/c/Program Files/Java"/jdk-17*; do
  p="$(cygpath -u "$j" 2>/dev/null || echo "$j")"
  if is_jdk17 "$p"; then found="$(cygpath -w "$p")"; break; fi
done
[ -n "$found" ] || { echo "JDK 17 not found: set JAVA_HOME to a JDK 17" >&2; exit 1; }
JAVA_HOME="$found"
export JAVA_HOME
echo "JDK: $JAVA_HOME"
echo "SDK: $ANDROID_HOME"

./build.sh --generic --min-sdk=25
cp FreeMyTV.apk tx9/FreeMyTV-tx9.apk
echo "APK: tx9/FreeMyTV-tx9.apk ($(du -h tx9/FreeMyTV-tx9.apk | cut -f1))"

if [ "${1:-}" = "--install" ]; then
  echo "installing on $TV_IP"
  "$ADB" connect "$TV_IP:5555"
  "$ADB" install -r tx9/FreeMyTV-tx9.apk
  # The box's adbd answers one client at a time: let go of it, or the app's own ADB won't get an answer.
  "$ADB" disconnect "$TV_IP:5555"
  "$ADB" kill-server
  echo
  echo "On the TV: Free My TV -> Inicio -> Free My TV -> OK. Wait for it to finish."
fi
