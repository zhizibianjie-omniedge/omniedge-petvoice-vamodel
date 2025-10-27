"""
PetVoice VA Model Package
宠物情感识别VA模型包

基于论文 "Beyond Discrete Categories: Multi-Task Valence-Arousal Modeling for Pet Vocalization Analysis"
arXiv:2510.12819

主要功能:
- 宠物发声的VA情感空间建模
- 多任务学习框架
- 音频特征提取和处理
- 模型训练和推理

作者: Junyao Huang, Rumin Situ
团队: 智子边界 (OmniEdge) 团队
论文: https://arxiv.org/abs/2510.12819
"""

__version__ = "1.0.0"
__author__ = "Junyao Huang, Rumin Situ"
__email__ = "team@omniedge.ai"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 智子边界 (OmniEdge) 团队"

# 核心模块导入
from .model import PetVoiceMultiTaskModel
from .utils import AudioProcessor, VAEmotionSpace
from .data import PetVoiceDataset, DataLoader

__all__ = [
    "PetVoiceMultiTaskModel",
    "AudioProcessor",
    "VAEmotionSpace",
    "PetVoiceDataset",
    "DataLoader",
]