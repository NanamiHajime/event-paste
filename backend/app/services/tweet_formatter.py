from __future__ import annotations

import re
import sys

from backend.app.models.event import Event


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
    if event.djs and any(dj.strip() for dj in event.djs):
        lines.append("🎧️DJ")
        for dj in event.djs:
            if dj.strip():
                lines.append(f"{dj}")
    if event.vjs and any(vj.strip() for vj in event.vjs):
        lines.append("📺️VJ")
        for vj in event.vjs:
            if vj.strip():
                lines.append(f"{vj}")
    if event.host:
        lines.append(f"👤 主催: {event.host}")

    return "\n".join(lines)