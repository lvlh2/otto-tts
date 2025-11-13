import time
from pathlib import Path

import click
import httpx

from .lib import get_pinyin_list, to_audio


@click.command()
@click.option("--output-dir", "-O", type=str, default=".", help="Output directory")
@click.option(
    "--format", "-f", type=str, default="mp3", help="Output format (default: mp3)"
)
@click.argument("texts", type=str, nargs=-1)
def otto_tts(output_dir: str, format: str, texts: tuple[str]) -> None:
    """
    otto TTS - 使用电棍otto活字印刷语音的中文文本转语音工具

    可将中文文本转换为otto语音的音频文件，支持在单次命令中处理多个文本以及多种输出格式

    TEXTS: 要转换为音频的一个或多个中文文本，每个文本将保存为单独的音频文件

    使用示例:

      # 基本用法：转换多个文本

      otto-tts "你好" "世界" "测试"

      # 自定义输出目录和格式

      otto-tts -O ./output -f wav "自定义文本"

      输出文件名为 "0000.wav", "0001.wav" 等格式
    """
    if output_dir != ".":
        Path(output_dir).mkdir(exist_ok=True)

    for i, text in enumerate(texts):
        pinyin_list = get_pinyin_list(text)

        with httpx.Client() as client:
            result = to_audio(client, pinyin_list)

        click.echo(f'Converting "{text}" to audio...')
        result.export(Path(output_dir) / f"{i:>04}.{format}")
        time.sleep(2)


if __name__ == "__main__":
    otto_tts()
