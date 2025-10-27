"""
Model Module - 模型实现模块

包含PetVoice VA模型的核心实现：
- Audio Transformer编码器
- 多任务学习框架
- VA回归头
- 分类任务头
"""

from .pet_voice_va import PetVoiceMultiTaskModel
from .audio_transformer import AudioTransformerEncoder
from .va_head import VARegressionHead
from .classification_head import ClassificationHead

__all__ = [
    "PetVoiceMultiTaskModel",
    "AudioTransformerEncoder",
    "VARegressionHead",
    "ClassificationHead",
]