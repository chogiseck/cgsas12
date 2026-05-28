#!/usr/bin/env python3
"""
AI 뉴스 자동 수집 스크립트 — 세션 시작 시 실행
Google News RSS에서 AI 뉴스를 수집해 Obsidian 마크다운으로 저장합니다.
"""

import os
import sys
import datetime
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
import re
import html

PROJECT_DIR = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
TODAY = datetime.date.today().strftime("%Y-%m-%d")
DATE_KR = datetime.date.today().strftime("%Y년 %m월 %d일")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "AI뉴스")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{TODAY}.md")

# 오늘 파일이 이미 있으면 건너뜀 (멱등성)
if os.path.exists(OUTPUT_FILE):
    print(f"⏭️  오늘 뉴스 이미 저장됨: {OUTPUT_FILE}")
    sys.exit(0)

RSS_FEEDS = [
    "https://news.google.com/rss/search?q=OpenAI+Anthropic+Google+AI&hl=ko&gl=KR&ceid=KR:ko",
    "https://news.google.com/rss/search?q=인공지능+AI+최신&hl=ko&gl=KR&ceid=KR:ko",
    "https://news.google.com/rss/search?q=artificial+intelligence+2026&hl=en&gl=US&ceid=US:en",
]

RANK_ICONS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def clean(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_rss(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item"):
            title = clean(item.findtext("title", ""))
            desc = clean(item.findtext("description", ""))
            link = (item.findtext("link") or "").strip()
            pub = clean(item.findtext("pubDate", ""))
            if title:
                items.append({"title": title, "desc": desc[:250], "link": link, "pub": pub})
        return items
    except Exception as e:
        print(f"  ⚠️  RSS 수집 실패 ({url[:60]}...): {e}", file=sys.stderr)
        return []


print("📡 AI 뉴스 수집 중...")

all_items = []
for feed in RSS_FEEDS:
    fetched = fetch_rss(feed)
    print(f"  → {len(fetched)}개 수집")
    all_items.extend(fetched)

# 중복 제거 (제목 기준), 최대 10개
seen, unique = set(), []
for item in all_items:
    key = item["title"][:40]
    if key not in seen and len(unique) < 10:
        seen.add(key)
        unique.append(item)

if not unique:
    print("❌ 수집된 뉴스 없음. 네트워크를 확인하세요.", file=sys.stderr)
    sys.exit(1)

# ─── 마크다운 생성 ──────────────────────────────────────────────
lines = [
    f"""---
tags: [AI, 뉴스, 인공지능, daily]
date: {TODAY}
created: {TODAY}
---

# 🤖 AI 뉴스 브리핑 — {DATE_KR}

> *"오늘도 AI는 세상을 조용히, 그러나 격렬하게 바꾸고 있다."*

---
"""
]

for i, item in enumerate(unique):
    icon = RANK_ICONS[i] if i < len(RANK_ICONS) else f"{i+1}."
    lines.append(f"""## {icon} #{i+1} · {item['title']}

{item['desc']}

[🔗 원문 보기]({item['link']})

---
""")

lines.append(f"""## 📌 오늘의 한 줄 요약

> AI 기술은 오늘도 새로운 역사를 쓰고 있다. 놓치지 마세요.

---

*📡 자동 수집: Google News RSS | 🤖 정리: Claude AI 세션 훅*
*수집 일시: {TODAY}*
""")

# ─── 파일 저장 ──────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ 저장 완료: {OUTPUT_FILE}")

# ─── Git 커밋 & 푸시 ────────────────────────────────────────────
try:
    os.chdir(PROJECT_DIR)
    subprocess.run(["git", "config", "user.email", "claude-bot@auto.news"], check=False, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Claude AI 뉴스봇"], check=False, capture_output=True)
    subprocess.run(["git", "add", OUTPUT_FILE], check=True, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", f"feat: AI 뉴스 Top10 자동 저장 ({TODAY})"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        push = subprocess.run(
            ["git", "push", "origin", "HEAD"],
            capture_output=True, text=True
        )
        if push.returncode == 0:
            print("✅ GitHub 푸시 완료")
        else:
            print(f"⚠️  푸시 실패: {push.stderr.strip()}", file=sys.stderr)
    else:
        print(f"⚠️  커밋 실패: {result.stderr.strip()}", file=sys.stderr)
except Exception as e:
    print(f"⚠️  Git 오류: {e}", file=sys.stderr)

print("🎉 AI 뉴스 세션 훅 완료!")
