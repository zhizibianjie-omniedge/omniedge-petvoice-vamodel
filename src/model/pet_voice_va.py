"""
PetVoice Multi-Task Model
宠物情感识别多任务学习模型

基于论文 "Beyond Discrete Categories: Multi-Task Valence-Arousal Modeling for Pet Vocalization Analysis"
arXiv:2510.12819

主要功能:
- Audio Transformer音频特征提取
- VA连续情感空间预测
- 多任务学习（情感分类、品种分类、场景分类）
- 动态权重调整

作者: Junyao Huang, Rumin Situ
团队: 智子边界 (OmniEdge) 团队
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Optional, Tuple, List
import logging

from .audio_transformer import AudioTransformerEncoder
from .va_head import VARegressionHead
from .classification_head import ClassificationHead

# 配置日志
logger = logging.getLogger(__name__)


class PetVoiceMultiTaskModel(nn.Module):
    """
    宠物情感识别多任务学习模型

    该模型实现了论文中描述的多任务学习框架，包含：
    1. 共享的Audio Transformer编码器
    2. VA回归头（主任务）
    3. 情感分类头（辅助任务）
    4. 品种分类头（辅助任务）
    5. 场景分类头（辅助任务）
    """

    def __init__(
        self,
        audio_config: Optional[Dict] = None,
        shared_hidden_dim: int = 512,
        num_emotions: int = 8,
        num_breeds: int = 15,
        num_scenes: int = 5,
        dropout_rate: float = 0.2,
        task_weights: Optional[Dict[str, float]] = None,
    ):
        """
        初始化多任务模型

        Args:
            audio_config: 音频编码器配置
            shared_hidden_dim: 共享隐藏层维度
            num_emotions: 情感类别数量
            num_breeds: 品种类别数量
            num_scenes: 场景类别数量
            dropout_rate: Dropout比率
            task_weights: 任务权重配置
        """
        super().__init__()

        # 默认音频配置
        if audio_config is None:
            audio_config = {
                'sample_rate': 16000,
                'n_fft': 1024,
                'hop_length': 512,
                'n_mels': 128,
                'hidden_size': 768,
                'num_layers': 12,
                'num_heads': 12,
                'dropout': 0.1,
            }

        # 1. 共享音频编码器
        self.audio_encoder = AudioTransformerEncoder(**audio_config)

        # 2. 共享特征层
        self.shared_layers = self._build_shared_layers(
            self.audio_encoder.output_dim,
            shared_hidden_dim,
            dropout_rate
        )

        # 3. 任务专用头
        self.va_head = VARegressionHead(shared_hidden_dim // 4)
        self.emotion_head = ClassificationHead(
            shared_hidden_dim // 4, num_emotions, task_name='emotion'
        )
        self.breed_head = ClassificationHead(
            shared_hidden_dim // 4, num_breeds, task_name='breed'
        )
        self.scene_head = ClassificationHead(
            shared_hidden_dim // 4, num_scenes, task_name='scene'
        )

        # 4. 任务权重
        if task_weights is None:
            task_weights = {
                'va': 1.0,      # 主任务权重最高
                'emotion': 0.6, # 辅助任务权重
                'breed': 0.3,
                'scene': 0.3
            }
        self.task_weights = task_weights

        # 5. 模型信息
        self.model_info = {
            'version': '1.0.0',
            'paper': 'arXiv:2510.12819',
            'authors': 'Junyao Huang, Rumin Situ',
            'team': 'OmniEdge'
        }

        logger.info(f"PetVoice多任务模型初始化完成: {self._get_model_summary()}")

    def _build_shared_layers(
        self,
        input_dim: int,
        hidden_dim: int,
        dropout_rate: float
    ) -> nn.Sequential:
        """
        构建共享特征层

        Args:
            input_dim: 输入维度
            hidden_dim: 隐藏层维度
            dropout_rate: Dropout比率

        Returns:
            共享特征层
        """
        return nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.LayerNorm(hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),

            nn.Linear(hidden_dim // 2, hidden_dim // 4),
            nn.LayerNorm(hidden_dim // 4),
            nn.ReLU(),
            nn.Dropout(dropout_rate)
        )

    def forward(
        self,
        audio_input: torch.Tensor,
        task_weights: Optional[Dict[str, float]] = None,
        return_features: bool = False
    ) -> Dict[str, torch.Tensor]:
        """
        前向传播

        Args:
            audio_input: 音频输入张量 [batch_size, sequence_length]
            task_weights: 任务权重（可选，用于推理时动态调整）
            return_features: 是否返回中间特征

        Returns:
            包含各任务预测结果的字典
        """
        # 1. 音频特征提取
        audio_features = self.audio_encoder(audio_input)

        # 2. 共享特征处理
        shared_features = self.shared_layers(audio_features)

        # 3. 多任务预测
        outputs = {}
        outputs['va'] = self.va_head(shared_features)
        outputs['emotion'] = self.emotion_head(shared_features)
        outputs['breed'] = self.breed_head(shared_features)
        outputs['scene'] = self.scene_head(shared_features)

        # 4. 可选：返回中间特征
        if return_features:
            outputs['audio_features'] = audio_features
            outputs['shared_features'] = shared_features

        return outputs

    def compute_loss(
        self,
        predictions: Dict[str, torch.Tensor],
        targets: Dict[str, torch.Tensor],
        task_weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, torch.Tensor]:
        """
        计算多任务损失

        Args:
            predictions: 模型预测结果
            targets: 目标标签
            task_weights: 任务权重（可选）

        Returns:
            包含总损失和各任务损失的字典
        """
        if task_weights is None:
            task_weights = self.task_weights

        total_loss = torch.tensor(0.0, device=predictions['va']['valence'].device)
        task_losses = {}

        # VA回归损失（主任务）
        va_loss = self.va_head.compute_loss(predictions['va'], targets['va'])
        task_losses['va'] = va_loss
        total_loss += task_weights['va'] * va_loss

        # 情感分类损失
        if 'emotion' in targets:
            emotion_loss = self.emotion_head.compute_loss(
                predictions['emotion'], targets['emotion']
            )
            task_losses['emotion'] = emotion_loss
            total_loss += task_weights['emotion'] * emotion_loss

        # 品种分类损失
        if 'breed' in targets:
            breed_loss = self.breed_head.compute_loss(
                predictions['breed'], targets['breed']
            )
            task_losses['breed'] = breed_loss
            total_loss += task_weights['breed'] * breed_loss

        # 场景分类损失
        if 'scene' in targets:
            scene_loss = self.scene_head.compute_loss(
                predictions['scene'], targets['scene']
            )
            task_losses['scene'] = scene_loss
            total_loss += task_weights['scene'] * scene_loss

        return {
            'total_loss': total_loss,
            'task_losses': task_losses
        }

    def predict_va(self, audio_input: torch.Tensor) -> Dict[str, float]:
        """
        预测VA值

        Args:
            audio_input: 音频输入

        Returns:
            VA预测结果字典
        """
        self.eval()
        with torch.no_grad():
            predictions = self.forward(audio_input)
            va_pred = predictions['va']

            return {
                'valence': va_pred['valence'].item(),
                'arousal': va_pred['arousal'].item(),
                'confidence': self._calculate_confidence(va_pred)
            }

    def _calculate_confidence(self, va_prediction: Dict[str, torch.Tensor]) -> float:
        """
        计算VA预测的置信度

        Args:
            va_prediction: VA预测结果

        Returns:
            置信度值 [0, 1]
        """
        # 基于预测值的稳定性计算置信度
        valence_var = torch.var(va_prediction['valence']).item()
        arousal_var = torch.var(va_prediction['arousal']).item()

        # 方差越小，置信度越高
        confidence = 1.0 / (1.0 + valence_var + arousal_var)
        return float(confidence)

    def _get_model_summary(self) -> str:
        """获取模型摘要信息"""
        total_params = sum(p.numel() for p in self.parameters())
        trainable_params = sum(p.numel() for p in self.parameters() if p.requires_grad)

        return (
            f"总参数: {total_params:,}, "
            f"可训练参数: {trainable_params:,}, "
            f"任务: VA回归 + 情感分类 + 品种分类 + 场景分类"
        )

    @classmethod
    def from_pretrained(cls, model_path: str, **kwargs):
        """
        从预训练模型加载

        Args:
            model_path: 预训练模型路径
            **kwargs: 额外参数

        Returns:
            加载的模型实例
        """
        model = cls(**kwargs)
        checkpoint = torch.load(model_path, map_location='cpu')

        # 处理不同的checkpoint格式
        if 'state_dict' in checkpoint:
            model.load_state_dict(checkpoint['state_dict'])
        else:
            model.load_state_dict(checkpoint)

        logger.info(f"成功加载预训练模型: {model_path}")
        return model

    def save_checkpoint(self, filepath: str, epoch: int, optimizer_state: Optional[Dict] = None):
        """
        保存模型检查点

        Args:
            filepath: 保存路径
            epoch: 当前epoch
            optimizer_state: 优化器状态（可选）
        """
        checkpoint = {
            'epoch': epoch,
            'state_dict': self.state_dict(),
            'model_info': self.model_info,
            'task_weights': self.task_weights,
        }

        if optimizer_state is not None:
            checkpoint['optimizer_state'] = optimizer_state

        torch.save(checkpoint, filepath)
        logger.info(f"模型检查点已保存: {filepath}")


# 工厂函数
def create_pet_voice_model(
    model_size: str = "base",
    num_emotions: int = 8,
    num_breeds: int = 15,
    num_scenes: int = 5,
    **kwargs
) -> PetVoiceMultiTaskModel:
    """
    创建PetVoice模型实例

    Args:
        model_size: 模型大小 ('small', 'base', 'large')
        num_emotions: 情感类别数量
        num_breeds: 品种类别数量
        num_scenes: 场景类别数量
        **kwargs: 其他参数

    Returns:
        模型实例
    """
    # 根据模型大小设置配置
    size_configs = {
        "small": {
            "audio_config": {
                "hidden_size": 384,
                "num_layers": 6,
                "num_heads": 6,
            },
            "shared_hidden_dim": 256,
        },
        "base": {
            "audio_config": {
                "hidden_size": 768,
                "num_layers": 12,
                "num_heads": 12,
            },
            "shared_hidden_dim": 512,
        },
        "large": {
            "audio_config": {
                "hidden_size": 1024,
                "num_layers": 24,
                "num_heads": 16,
            },
            "shared_hidden_dim": 768,
        }
    }

    config = size_configs.get(model_size, size_configs["base"])
    config.update(kwargs)

    return PetVoiceMultiTaskModel(
        num_emotions=num_emotions,
        num_breeds=num_breeds,
        num_scenes=num_scenes,
        **config
    )


if __name__ == "__main__":
    # 测试模型创建
    model = create_pet_voice_model("base")
    print(f"模型创建成功: {model._get_model_summary()}")

    # 测试前向传播
    batch_size, seq_len = 2, 16000  # 1秒音频，16kHz采样率
    dummy_audio = torch.randn(batch_size, seq_len)

    with torch.no_grad():
        outputs = model(dummy_audio)
        print(f"VA预测形状: valence={outputs['va']['valence'].shape}, arousal={outputs['va']['arousal'].shape}")
        print(f"情感预测形状: {outputs['emotion']['logits'].shape}")
        print(f"品种预测形状: {outputs['breed']['logits'].shape}")
        print(f"场景预测形状: {outputs['scene']['logits'].shape}")