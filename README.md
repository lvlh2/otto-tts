# otto-tts

使用电棍otto活字印刷语音的中文文本转语音命令行工具

语音来自：<https://shuodedao.li/>

## 安装方式

### 从 PyPI 安装

```bash
pip install otto-tts
```

## 快速开始

### 基本使用

```bash
# 转换单个文本
otto-tts "你好，世界！"

# 转换多个文本
otto-tts "欧内的手" "好汉"
```

### 高级选项

```bash
# 指定输出目录和音频格式
otto-tts -O output -f wav "自定义文本"
```

## 完整用法

```bash
otto-tts [OPTIONS] TEXTS...
```

### 参数说明

- `TEXTS`：要转换的一个或多个中文文本（必需参数）

### 选项说明

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--output-dir` | `-O` | 当前目录 | 音频文件输出目录 |
| `--format` | `-f` | mp3 | 音频格式|
