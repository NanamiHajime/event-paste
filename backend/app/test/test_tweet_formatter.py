import pytest
from pydantic import ValidationError

from backend.app.models.event import Event

BASE_EVENT_DATA = {
    "name": "イベントA開催！",
    "start_date": "2023-10-13",
    "start_at": "17:30",
    "price": 0,
    "with_1d": False,
    "venue": "イベント会場",
    "address": "東京都千代田区1-1-1",
    "hashtag": "イベント",
    "description": "イベントの説明文",
    "djs": [
        "DJ1",
        "DJ2",
        "DJ3",
    ],
    "vjs": ["VJ1", "VJ2", "VJ3"],
    "host": "主催(@syusai_test)",
    "reply_url": "https://x.com/test/status/1111111111111111111",
}


@pytest.fixture(scope="function")
def event_data():
    return BASE_EVENT_DATA.copy()


@pytest.mark.parametrize(
    "disallow_newline",
    [
        "name",
        "venue",
        "address",
        "hashtag",
        "host",
    ],
)
def test_disallow_newline(disallow_newline, event_data):
    """改行が含むことを許可しない"""
    test_data = event_data[disallow_newline]
    event_data[disallow_newline] = test_data[0] + "\n" + test_data[1:]
    with pytest.raises(ValidationError, match="改行はできません"):
        Event(**event_data)


@pytest.mark.parametrize(
    "list_disallow_newline",
    [
        "djs",
        "vjs",
    ],
)
def test_disallow_list_newline(list_disallow_newline, event_data):
    """リストの要素ごとに改行を含むことを許可しない"""
    original_data = event_data[list_disallow_newline][0]
    event_data[list_disallow_newline][0] = original_data + "\n"
    with pytest.raises(ValidationError, match="改行はできません"):
        Event(**event_data)


@pytest.mark.parametrize("disallow_character", ["#", "＃"])
def test_disallow_hashtag_character(disallow_character, event_data):
    """ハッシュタグに「＃」「#」が含まれていないか"""
    event_data["hashtag"] = event_data["hashtag"] + disallow_character

    with pytest.raises(
        ValidationError,
        match="'#'や'＃'はハッシュタグの先頭に自動的に追加されます。",
    ):
        Event(**event_data)