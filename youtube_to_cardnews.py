"""
YouTube → 카드뉴스 자동 생성기
- YouTube 영상 자막을 가져와 Claude API로 카드뉴스를 생성하고 Obsidian에 저장합니다.

사용법:
    python youtube_to_cardnews.py <YouTube_URL> [--vault-path /path/to/vault] [--folder Clippings]

환경변수:
    ANTHROPIC_API_KEY   : Claude API 키 (필수)
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# ── 의존성 설치 안내 ──────────────────────────────────────────────────────────
try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("youtube-transcript-api 가 설치되지 않았습니다.\n  pip install youtube-transcript-api")

try:
    import anthropic
except ImportError:
    sys.exit("anthropic 패키지가 설치되지 않았습니다.\n  pip install anthropic")

try:
    import requests
except ImportError:
    requests = None  # 영상 제목 조회 시 사용; 없어도 동작함


# ── 상수 ─────────────────────────────────────────────────────────────────────
DEFAULT_VAULT_PATH = Path.home() / "Obsidian Vault"
DEFAULT_FOLDER = "Clippings"
MODEL = "claude-sonnet-4-6"
DEFAULT_CARD_COUNT = 8


# ── YouTube 유틸 ──────────────────────────────────────────────────────────────
def extract_video_id(url: str) -> str:
    patterns = [
        r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:embed/)([A-Za-z0-9_-]{11})",
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    raise ValueError(f"유효한 YouTube URL이 아닙니다: {url}")


def get_video_title(video_id: str) -> str:
    """oEmbed API로 영상 제목 조회 (API 키 불필요)."""
    if requests is None:
        return video_id
    try:
        resp = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"},
            timeout=10,
        )
        if resp.status_code == 200:
            return resp.json().get("title", video_id)
    except Exception:
        pass
    return video_id


def get_transcript(video_id: str) -> tuple[str, str]:
    """
    자막 텍스트와 사용된 언어 코드를 반환합니다.
    한국어 → 영어 → 자동생성 순으로 시도합니다.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except Exception as e:
        raise RuntimeError(f"자막 목록 조회 실패: {e}")

    # 시도 순서: 수동 한국어 → 수동 영어 → 자동생성 한국어 → 자동생성 영어
    for lang, generated in [("ko", False), ("en", False), ("ko", True), ("en", True)]:
        try:
            if generated:
                t = transcript_list.find_generated_transcript([lang])
            else:
                t = transcript_list.find_manually_created_transcript([lang])
            entries = t.fetch()
            text = " ".join(e["text"] for e in entries)
            return text, t.language_code
        except Exception:
            continue

    # 위 모두 실패하면 첫 번째 자막 사용
    try:
        t = next(iter(transcript_list))
        entries = t.fetch()
        text = " ".join(e["text"] for e in entries)
        return text, t.language_code
    except Exception as e:
        raise RuntimeError(f"자막을 가져올 수 없습니다: {e}")


# ── Claude 카드뉴스 생성 ──────────────────────────────────────────────────────
SYSTEM_PROMPT = """당신은 유튜브 영상 내용을 분석해서 한국어 카드뉴스를 만드는 전문가입니다.
카드뉴스는 복잡한 정보를 간결하고 시각적으로 전달하는 포맷입니다.
반드시 JSON 형식으로만 응답하세요. 다른 텍스트는 출력하지 마세요."""

CARD_PROMPT_TEMPLATE = """\
다음은 YouTube 영상의 자막입니다. 이 내용을 분석해서 {card_count}장짜리 카드뉴스를 만들어주세요.

[영상 제목]
{title}

[자막 내용]
{transcript}

---
아래 JSON 형식으로 정확히 응답해주세요:

{{
  "summary": "영상의 핵심 내용을 2-3문장으로 요약",
  "keywords": ["핵심키워드1", "핵심키워드2", "핵심키워드3"],
  "cards": [
    {{
      "card_number": 1,
      "emoji": "카드 내용에 어울리는 이모지",
      "title": "카드 제목 (15자 이내, 임팩트 있게)",
      "subtitle": "부제목 (20자 이내)",
      "points": ["핵심 포인트 1 (25자 이내)", "핵심 포인트 2 (25자 이내)", "핵심 포인트 3 (25자 이내)"],
      "highlight": "이 카드의 가장 중요한 한 줄 메시지"
    }}
  ],
  "cta": "독자에게 전하는 행동 촉구 메시지 (Call to Action)"
}}

카드 구성 가이드:
- 카드 1: 훅(Hook) - 왜 이 내용이 중요한가?
- 카드 2~{card_count_minus1}: 핵심 내용을 논리적 순서로
- 카드 {card_count}: 결론 및 실천 방법
"""


def generate_card_news(title: str, transcript: str, api_key: str, card_count: int) -> dict:
    client = anthropic.Anthropic(api_key=api_key)

    prompt = CARD_PROMPT_TEMPLATE.format(
        card_count=card_count,
        card_count_minus1=card_count - 1,
        title=title,
        transcript=transcript[:8000],  # 토큰 절약을 위해 앞부분만 사용
    )

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # JSON 블록이 있으면 추출
    json_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", raw)
    if json_match:
        raw = json_match.group(1).strip()

    return json.loads(raw)


# ── Obsidian 마크다운 생성 ────────────────────────────────────────────────────
def build_obsidian_markdown(video_id: str, title: str, lang: str, data: dict) -> str:
    now = datetime.now()
    url = f"https://www.youtube.com/watch?v={video_id}"
    keywords_str = ", ".join(f"#{k.replace(' ', '_')}" for k in data.get("keywords", []))

    lines = [
        "---",
        f'title: "{title}"',
        f"source: {url}",
        f"created: {now.strftime('%Y-%m-%d')}",
        f"transcript_lang: {lang}",
        "tags:",
        "  - clippings",
        "  - 카드뉴스",
        "  - youtube",
        "---",
        "",
        f"# {title}",
        "",
        "> [!info] 영상 링크",
        f"> ![]({url})",
        "",
        "---",
        "",
        "## 📋 핵심 요약",
        "",
        f"> {data.get('summary', '')}",
        "",
        f"**키워드**: {keywords_str}",
        "",
        "---",
        "",
        "## 🃏 카드뉴스",
        "",
    ]

    for card in data.get("cards", []):
        num = card.get("card_number", "?")
        emoji = card.get("emoji", "📌")
        card_title = card.get("title", "")
        subtitle = card.get("subtitle", "")
        points = card.get("points", [])
        highlight = card.get("highlight", "")

        lines += [
            f"### Card {num}  {emoji} {card_title}",
            "",
            f"**{subtitle}**",
            "",
        ]
        for p in points:
            lines.append(f"- {p}")
        lines += [
            "",
            "> [!quote] 핵심 메시지",
            f"> {highlight}",
            "",
            "---",
            "",
        ]

    cta = data.get("cta", "")
    if cta:
        lines += [
            "## 🚀 Action",
            "",
            "> [!tip] 지금 바로 해보세요",
            f"> {cta}",
            "",
        ]

    lines += [
        "---",
        f"*생성일시: {now.strftime('%Y-%m-%d %H:%M')} | 모델: {MODEL}*",
    ]

    return "\n".join(lines)


# ── 파일 저장 ─────────────────────────────────────────────────────────────────
def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name)
    return name[:80].strip()


def save_to_obsidian(content: str, title: str, vault_path: Path, folder: str) -> Path:
    target_dir = vault_path / folder
    target_dir.mkdir(parents=True, exist_ok=True)

    date_prefix = datetime.now().strftime("%Y%m%d")
    safe_title = sanitize_filename(title)
    filename = f"{date_prefix} 카드뉴스 {safe_title}.md"
    file_path = target_dir / filename

    file_path.write_text(content, encoding="utf-8")
    return file_path


# ── 메인 ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="YouTube 영상을 Obsidian 카드뉴스로 변환")
    parser.add_argument("url", help="YouTube 영상 URL")
    parser.add_argument(
        "--vault-path",
        default=str(DEFAULT_VAULT_PATH),
        help=f"Obsidian 볼트 경로 (기본: {DEFAULT_VAULT_PATH})",
    )
    parser.add_argument(
        "--folder",
        default=DEFAULT_FOLDER,
        help=f"볼트 내 저장 폴더 (기본: {DEFAULT_FOLDER})",
    )
    parser.add_argument(
        "--cards",
        type=int,
        default=DEFAULT_CARD_COUNT,
        help=f"생성할 카드 수 (기본: {DEFAULT_CARD_COUNT})",
    )
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("환경변수 ANTHROPIC_API_KEY 를 설정해주세요.")

    vault_path = Path(args.vault_path).expanduser()

    print("[1/4] 영상 ID 추출 중...")
    video_id = extract_video_id(args.url)
    print(f"      Video ID: {video_id}")

    print("[2/4] 영상 제목 조회 중...")
    title = get_video_title(video_id)
    print(f"      제목: {title}")

    print("[3/4] 자막 다운로드 중...")
    transcript, lang = get_transcript(video_id)
    print(f"      언어: {lang} | 글자 수: {len(transcript):,}")

    print(f"[4/4] Claude로 카드뉴스 생성 중... (모델: {MODEL})")
    data = generate_card_news(title, transcript, api_key, args.cards)
    print(f"      카드 {len(data.get('cards', []))}장 생성 완료")

    md_content = build_obsidian_markdown(video_id, title, lang, data)
    saved_path = save_to_obsidian(md_content, title, vault_path, args.folder)

    print(f"\n완료! 저장 위치: {saved_path}")
    print("\n--- 카드뉴스 미리보기 ---")
    print(f"요약: {data.get('summary', '')[:100]}...")
    for card in data.get("cards", []):
        print(f"  Card {card['card_number']}: {card.get('emoji', '')} {card.get('title', '')}")


if __name__ == "__main__":
    main()
