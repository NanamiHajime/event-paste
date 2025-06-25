from __future__ import annotations

import re
import sys

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(BASE_DIR))

from backend.app.models.event import Event

_ASCII = re.compile(r"^[\x00-\x7F]$")
_URL = re.compile(r"https?://\S+")
URL_WEIGHT = 23
MAX_TWEET_LENGTH = 280


def _count_tweet_text_length(text: str) -> int:
    """Twitterの文字カウントでの文字数を返す
    - ASCII 1 文字 = 1
    - CJK 全角 1 文字 = 2
    - URL は上のカウント通りだが 投稿後は変換されて常に23文字

    Args:
        text(str): 整形するテキスト
    Returns:
        int: Twitterの文字カウントでの文字数
    """
    length = 0
    text = str(text)
    if "\n" in text:
        raise ValueError("改行はできません")
    for char in text:
        length += 1 if _ASCII.match(char) else 2
    return length


def _format_to_tweet(event: Event) -> str:
    """ツイート向けにイベント情報を整形する。"""
    lines = []
    if event.name:
        lines.append(f"🎶 イベント名: {event.name}")
    if event.start_date and event.start_at:
        lines.append(f"📅 日時: {event.start_date.strftime('%Y-%m-%d')} {event.start_at.strftime('%H:%M')}")
    if event.venue:
        lines.append(f"📍 会場: {event.venue}")
    if event.address:
        lines.append(f"📍 住所: {event.address}")
    if event.price is not None:
        lines.append(f"💰 料金: ¥{event.price}{'（1D込）' if event.with_1d else ' +1D'}")
    if event.hashtag:
        lines.append(f"#{event.hashtag}")
    if event.description:
        lines.append(f"📝 内容: {event.description}")
    if event.djs:
        lines.append("🎧️DJ")
        for _, dj in enumerate(event.djs):
            lines.append(f"{dj}")
    if event.vjs:
        lines.append("📺️VJ")
        for _, vj in enumerate(event.vjs):
            lines.append(f"{vj}")
    if event.host:
        lines.append(f"👤 主催: {event.host}")

    return "\n".join(lines)