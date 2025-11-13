import io

import httpx
from pydub import AudioSegment
from tqdm import tqdm

from .constants import (
    BASE_URL,
    FULL_DICT,
    NON_CHINESE_MAPPER,
    NON_CHINESE_PAT,
    ORIGINAL_SOUND_MAPPER,
    SPLIT_PAT,
    STRIP_PAT,
)


def replace_non_chinese(text: str) -> str:
    """
    Replace non-chinese characters with specific characters in `NON_CHINESE_MAPPER`

    :param text: Input text
    :type text: str
    :return: Text with non-chinese characters replaced
    :rtype: str
    """
    return NON_CHINESE_PAT.sub(lambda m: f"[{NON_CHINESE_MAPPER[m.group()]}]", text)


def replace_original_sound(text_pinyin: str) -> str:
    """
    Replace original sound characters in `ORIGINAL_SOUND_MAPPER`

    :param text_pinyin: Text with original sound characters
    :type text_pinyin: str
    :return: Text with original sound characters replaced
    :rtype: str
    """
    for pat, replacement in ORIGINAL_SOUND_MAPPER.items():
        text_pinyin = text_pinyin.replace(pat, f"<{replacement}>")

    return text_pinyin


def get_pinyin(char: str) -> str:
    """
    Get pinyin for a character

    :param char: Character
    :type char: str
    :return: Pinyin
    :rtype: str
    """
    for key, value in FULL_DICT.items():
        if char in value:
            return key.capitalize()

    return ""


def to_pinyin(text: str) -> str:
    """
    Convert text to pinyin

    :param text: Text
    :type text: str
    :return: Pinyin
    :rtype: str
    """
    result = ""

    for char in text:
        # Check if `char` is a Chinese character
        if "\u4e00" <= char <= "\u9fff":
            pinyin = get_pinyin(char)
            if pinyin:
                result += pinyin
        else:
            result += char

    return result


def get_pinyin_list(text: str) -> list[str]:
    """
    Get pinyin list

    :param text: Text
    :type text: str
    :return: Pinyin list
    :rtype: list[str]
    """
    text = replace_non_chinese(text)

    text_pinyin = to_pinyin(text)

    text_pinyin = replace_original_sound(text_pinyin)

    text_pinyin = STRIP_PAT.sub("", text_pinyin)

    return [pinyin.lower() for pinyin in SPLIT_PAT.split(text_pinyin) if pinyin]


def to_audio(client: httpx.Client, pinyin_list: list[str]) -> AudioSegment:
    """
    Convert pinyin list to audio

    :param client: HTTP client
    :type client: httpx.Client
    :param pinyin_list: Pinyin list
    :type pinyin_list: list[str]
    :return: Audio
    :rtype: AudioSegment
    """
    original_sounds = set(ORIGINAL_SOUND_MAPPER.values())

    concatenated = AudioSegment.empty()
    for pinyin in tqdm(pinyin_list):
        if pinyin in original_sounds:
            url = f"{BASE_URL}/ysddTokens//{pinyin}.mp3"
        else:
            url = f"{BASE_URL}/tokens//{pinyin}.wav"

        response = client.get(url)
        if response.status_code == 404:
            continue

        response.raise_for_status()

        audio = AudioSegment.from_file(io.BytesIO(response.content))
        concatenated += audio

    return concatenated
