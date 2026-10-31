"""
sync_docs.py - one-way sync of canonical rule/guide files to their duplicate copies.

Canonical (edit ONLY these)                         ->  copy (never edit by hand)
  korean-stock-analyzer/SKILL.md                    ->  update/skill.md
  GEMINI.md                                         ->  update/gemini.md
  이용방법.md                                        ->  update/이용방법.md

    python sync_docs.py --check   # exit 1 if any copy has drifted (no writes)
    python sync_docs.py           # overwrite copies from canonical

Copies are overwritten byte-for-byte; nothing is ever deleted.
"""
import filecmp
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAIRS = [
    (os.path.join("korean-stock-analyzer", "SKILL.md"), os.path.join("update", "skill.md")),
    ("GEMINI.md", os.path.join("update", "gemini.md")),
    ("이용방법.md", os.path.join("update", "이용방법.md")),
]


def main(check_only):
    drift = 0
    for src_rel, dst_rel in PAIRS:
        src, dst = os.path.join(ROOT, src_rel), os.path.join(ROOT, dst_rel)
        if not os.path.exists(src):
            print(f"[skip] canonical missing: {src_rel}")
            continue
        same = os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False)
        if same:
            print(f"[ok]   {dst_rel}")
            continue
        drift += 1
        if check_only:
            print(f"[DRIFT] {dst_rel} differs from {src_rel}")
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            print(f"[sync] {src_rel} -> {dst_rel}")
    return 1 if (check_only and drift) else 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv[1:]))
