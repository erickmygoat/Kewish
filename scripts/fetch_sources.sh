#!/usr/bin/env bash
# Clone the two public source repositories this toolkit reads.
# Neither is vendored: they are large, and keeping them external makes it
# obvious that the page data is upstream's, not ours.
set -euo pipefail

DEST="${1:-$HOME}"

clone() {
  local url="$1" path="$2"
  if git -C "$path" rev-parse HEAD >/dev/null 2>&1; then
    echo "present: $path"
  else
    GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 "$url" "$path"
  fi
}

clone https://github.com/rtkd/iddqd              "$DEST/rtkd/iddqd"
clone https://github.com/relikd/LiberPrayground  "$DEST/relikd/LiberPrayground"

# Optional: the full 2012-2017 puzzle archive (~1.3 GB). Needed only for
# RESEARCH.md's primary sources, not for any analysis script.
if [ "${WITH_ARCHIVE:-0}" = "1" ]; then
  clone https://github.com/cicada-solvers/the-complete-cicada3301-archive \
        "$DEST/cicada-solvers/the-complete-cicada3301-archive"
fi

echo
echo "Sources ready. Verify the toolkit with:"
echo "  python3 -I scripts/verify_ground_truth.py --sources $DEST/relikd/LiberPrayground"
