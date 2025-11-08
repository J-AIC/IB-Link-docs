#!/usr/bin/env python3
import os
import re
import requests
import sys
import pathlib

DEEPL_KEY = os.getenv("DEEPL_API_KEY")
# Proは https://api.deepl.com/v2/translate
API_URL = os.getenv("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")


def split_md(md: str):
    # ```fence``` と `inline` を保護して分割
    pattern = re.compile(r"(```[\s\S]*?```|`[^`]+`)")
    parts, last = [], 0
    for m in pattern.finditer(md):
        if m.start() > last:
            parts.append(("text", md[last:m.start()]))
        parts.append(("code", m.group(0)))
        last = m.end()
    if last < len(md):
        parts.append(("text", md[last:]))
    return parts


def deepl_batch(texts, source="JA", target="EN"):
    out, batch, chars = [], [], 0

    def flush():
        nonlocal out, batch, chars
        if not batch:
            return
        data = [("text", s) for s in batch]
        data += [("source_lang", source), ("target_lang", target)]
        headers = {"Authorization": f"DeepL-Auth-Key {DEEPL_KEY}"}
        r = requests.post(API_URL, data=data, headers=headers, timeout=60)
        r.raise_for_status()
        out += [t["text"] for t in r.json()["translations"]]
        batch, chars = [], 0

    for t in texts:
        if not t.strip():
            out.append("")
            continue
        batch.append(t)
        chars += len(t)
        if chars > 4000 or len(batch) >= 50:
            flush()
    flush()
    return out


def main(src="docs/index.md", dst="docs/index.en.md"):
    if not DEEPL_KEY:
        print("ERROR: DEEPL_API_KEY is not set", file=sys.stderr)
        sys.exit(1)
    text = pathlib.Path(src).read_text(encoding="utf-8")
    parts = split_md(text)
    src_texts = [p[1] for p in parts if p[0] == "text"]
    tr_texts = deepl_batch(src_texts, "JA", "EN")
    it = iter(tr_texts)
    buf = []
    for kind, content in parts:
        if kind == "code":
            buf.append(content)
        else:
            buf.append(next(it))
    pathlib.Path(dst).write_text("".join(buf), encoding="utf-8")
    print(f"Translated -> {dst}")


if __name__ == "__main__":
    main()


