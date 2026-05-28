#!/usr/bin/env python3
"""
AI 뉴스 자동 수집 스크립트
GitHub Actions에서 매일 실행되어 RSS로 AI 뉴스를 수집하고
Obsidian 마크다운으로 저장합니다.
"""

import os
import sys
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html
import re

TODAY = datetime.date.today().strftime("%Y-%m-%d")
DATE_KR = datetime.date.today().strftime("%Y년 %m월 %d일")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "AI뉴스")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{TODAY}.md")

RANK_ICONS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

# 한국어 RSS URL은 퍼센트 인코딩 필요
RSS_FEEDS = [
    (
        "Google News (영문 AI)",
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode({
            "q": "OpenAI Anthropic Google AI 2026",
            "hl": "en",
            "gl": "US",
            "ceid": "US:en",
        })
    ),
    (
        "Google News (한국 AI)",
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode({
            "q": "인공지능 AI 최신",
            "hl": "ko",
            "gl": "KR",
            "ceid": "KR:ko",
        })
    ),
    (
        "TechCrunch AI",
        "https://techcrunch.com/category/artificial-intelligence/feed/"
    ),
    (
        "MIT Technology Review",
        "https://www.technologyreview.com/feed/"
    ),
    (
        "The Verge AI",
        "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
    ),
    (
        "VentureBeat AI",
        "https://venturebeat.com/category/ai/feed/"
    ),
]


def clean(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_rss(name: str, url: str) -> list:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
        root = ET.fromstring(raw)
        items = []
        for item in root.findall(".//item"):
            title = clean(item.findtext("title", ""))
            desc = clean(item.findtext("description", ""))
            link = (item.findtext("link") or "").strip()
            if title and len(title) > 5:
                items.append({"title": title, "desc": desc[:300], "link": link})
        print(f"  ✅ {name}: {len(items)}개")
        return items
    except Exception as e:
        print(f"  ⚠️  {name} 실패: {e}", file=sys.stderr)
        return []


def main():
    if os.path.exists(OUTPUT_FILE):
        print(f"⏭️  오늘 뉴스 이미 저장됨 ({TODAY}). 건너뜁니다.")
        return

    print(f"📡 AI 뉴스 수집 시작 ({TODAY})...")

    all_items = []
    for name, url in RSS_FEEDS:
        all_items.extend(fetch_rss(name, url))

    # 중복 제거 (제목 앞 50자 기준)
    seen, unique = set(), []
    for item in all_items:
        key = item["title"][:50].lower()
        if key not in seen and len(unique) < 10:
            seen.add(key)
            unique.append(item)

    if not unique:
        print("❌ 수집된 뉴스가 없습니다.", file=sys.stderr)
        sys.exit(1)

    print(f"📰 총 {len(unique)}개 뉴스 수집 완료")

    # ── 마크다운 생성 ──────────────────────────────────
    sections = [
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
        desc = item["desc"] if item["desc"] else "*요약 정보 없음*"
        sections.append(f"""## {icon} #{i+1} · {item['title']}

{desc}

[🔗 원문 보기]({item['link']})

---
""")

    sections.append(f"""## 📌 마무리

> 오늘의 AI 뉴스 {len(unique)}선이었습니다.
> 내일도 새로운 소식으로 찾아옵니다. 🚀

---

*📡 출처: Google News · TechCrunch · MIT Technology Review · The Verge · VentureBeat*
*🤖 자동 수집: GitHub Actions | 저장: {TODAY}*
""")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(sections))

    print(f"✅ 저장 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
