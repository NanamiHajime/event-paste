import os
import sys
import pytest
from pydantic import ValidationError

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BASE_DIR))

from backend.app.models.event import Event
from backend.app.services.tweet_formatter import (
    _count_tweet_text_length,
    MAX_TWEET_LENGTH,
)

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
    print("debug:", event_data[disallow_newline])
    with pytest.raises(TypeError, match=f"型または値が不正です"):
        Event(event_data)


@pytest.mark.parametrize(
    "list_disallow_newline",
    [
        "djs",
        "vjs",
    ],
)
def test_list_disallow_newline(list_disallow_newline, event_data):
    """リストの要素ごとに改行を含むことを許可しない"""
    input_data = event_data[list_disallow_newline]
    event_data[list_disallow_newline][0] = [input_data[0] + "\n"]
    with pytest.raises(TypeError, match=f"改行はできません"):
        Event(**input_data)


@pytest.mark.parametrize(
    "disallow_input_type",
    [None, 10, ["イベントA開催！", "会場: Bar txalaparta"], {}, []],
)
def test_split_for_twitter_disallow_types_check(disallow_input_type):
    """入力の型が正しくない"""
    with pytest.raises(TypeError):
        _split_for_twitter(disallow_input_type, match="型または値が不正です")


@pytest.mark.parametrize("field, valid_int", [("price", 0), ("price", 99999)])
def test_price_limits_valid(field, valid_int, event_data):
    """価格の文字数制限の境界値テスト(valid)"""
    event_data[field] = valid_int
    _split_for_twitter(event_data)


@pytest.mark.parametrize("field, invalid_int", [("price", -1), ("price", 100000)])
def test_price_limits_invalid(field, invalid_int, event_data):
    """価格の文字数制限の境界値テスト(invalid)"""
    # 最大値を超えた際にエラーが発生するか
    event_data[field] = invalid_int
    with pytest.raises(TypeError, match="型または値が不正です"):
        _split_for_twitter(event_data)


# テストするフィールドと許容可能な文字数(max_len以下)
STR_LIMIT = [
    ("name", 140),
    ("venue", 140),
    ("address", 140),
    ("hashtag", 100),
    ("description", 120),
    ("host", 100),
]

LIST_LIMIT_PER_ELEMENT = [
    ("djs", 100),
    ("vjs", 100),
]


@pytest.mark.parametrize("field, max_len", STR_LIMIT)
def test_str_length_limits_valid(field, max_len, event_data):
    """各フィールドの文字数制限の境界値テスト(valid)"""
    valid = "a" * max_len

    # 何もエラーが起こらず完了するか
    event_data[field] = valid
    _split_for_twitter(event_data)


@pytest.mark.parametrize("field, max_len", STR_LIMIT)
def test_str_length_limits_invalid(field, max_len, event_data):
    """各フィールドの文字数制限の境界値テスト(invalid)"""
    invalid = "a" * (max_len + 1)

    event_data[field] = invalid
    with pytest.raises(TypeError, match="型または値が不正です"):
        _split_for_twitter(event_data)


@pytest.mark.skip(reason="DJ/VJリストは後で実装するため")
@pytest.mark.parametrize("field, max_len", LIST_LIMIT_PER_ELEMENT)
def test_list_length_per_element_valid(field, max_len):
    """リストの要素ごとの文字数制限の境界値テスト(valid)"""
    valid = ["a" * max_len, "b" * (max_len - 1)]
    event_data[field] = valid
    _split_for_twitter(event_data)


@pytest.mark.skip(reason="DJ/VJリストは後で実装するため")
@pytest.mark.parametrize("field, max_len", LIST_LIMIT_PER_ELEMENT)
def test_list_length_per_element_invalid(field, max_len):
    """リストの要素ごとの文字数制限の境界値テスト(invalid)"""
    invalid = ["a" * (max_len), "b" * (max_len + 1)]
    event_data[field] = invalid
    with pytest.raises(ValueError):
        _split_for_twitter(event_data)


@pytest.mark.parametrize("disallow_character", ["#", "＃"])
def test_disallow_hashtag_character(disallow_character, event_data):
    """ハッシュタグに「＃」「#」が含まれていないか"""
    event_data["hashtag"] = disallow_character + event_data["hashtag"]

    with pytest.raises(
        TypeError,
        match="型または値が不正です",
    ):
        _split_for_twitter(event_data)


def test_split_for_twitter_basic():
    """文字数制限に引っかからず1ツイートで収まる場合のチェック"""
    event_data = {
        "name": "event",
        "start_date": "2024-03-20",
        "start_at": "19:00",
        "price": 2,
        "with_1d": False,
        "venue": "here",
        "address": "here",
        "hashtag": "aaa",
        "description": "aaa",
        "host": "あ(@a)",
    }
    tweets = _split_for_twitter(event_data)
    # すべての要素が短いので1ツイートにまとまるか
    assert len(tweets) == 1
    # データが欠落していないか
    # event_values = "".join(str(v) for v in event_data.values())
    # tweet_content = "".join(tweets)
    # assert event_values == tweet_content
    # 280文字以下になっているか
    assert len(_split_for_twitter(tweets[0])) <= MAX_TWEET_LENGTH


def test_split_for_twitter_multiple_tweets():
    """各要素は短いが、全部まとめると280文字を超える場合のチェック"""
    event_data = {
        "name": "イベント",
        "start_date": "2024-03-20",
        "start_at": "19:00",
        "price": 2,
        "with_1d": False,
        "venue": "a" * 100,
        "address": "a" * 100,
        "hashtag": "あ",
        "description": "a" * 100,
        "host": "あ(@a)",
    }
    tweets = _split_for_twitter(event_data)
    # 2ツイート以上になるはず
    assert len(tweets) >= 2


COUNT2_CHARACTERS = ["a", "A", "1", "!", "#"]


@pytest.mark.parametrize("count2_character", COUNT2_CHARACTERS)
def test_two_count(count2_character):
    """英数字が1カウントされるか"""
    symbol_counted = _count_tweet_text_length(count2_character)
    assert symbol_counted == 1


COUNT2_CHARACTERS = ["★", "💫", "あ", "ア", "阿"]


@pytest.mark.parametrize("count2_character", COUNT2_CHARACTERS)
def test_two_count(count2_character):
    """絵文字や特殊文字、全角が2カウントされるか"""
    symbol_counted = _count_tweet_text_length(count2_character)
    assert symbol_counted == 2
