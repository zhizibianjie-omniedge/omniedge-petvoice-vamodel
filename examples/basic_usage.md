# 基础使用教程 | Basic Usage Tutorial

[![Getting Started](https://img.shields.io/badge/Getting_Started-Basic_Usage-green.svg)](../README.md)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](../requirements.txt)
[![Examples](https://img.shields.io/badge/Examples-Ready-orange.svg)](./)

## 🎯 快速开始 | Quick Start

本教程将带您快速上手 PetVoice VA Model，包括环境配置、模型加载、基础预测等操作。

### 📋 前置要求 | Prerequisites

- Python 3.8+
- PyTorch 2.0+
- 依赖库（见 requirements.txt）

## 🚀 安装 | Installation

### 📦 从源码安装
```bash
# 克隆仓库
git clone https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel.git
cd omniedge-petvoice-vamodel

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装项目
pip install -e .
```

### 📥 直接安装（发布版本）
```bash
pip install omniedge-petvoice-vamodel
```

## 🎵 基础使用 | Basic Usage

### 📝 简单预测示例
```python
import torch
from omniedge_petvoice import PetVoiceMultiTaskModel, AudioProcessor

# 1. 加载预训练模型
model = PetVoiceMultiTaskModel.from_pretrained(
    "models/petvoice_va_model.pth"
)
model.eval()

# 2. 初始化音频处理器
processor = AudioProcessor(sample_rate=16000)

# 3. 加载和预处理音频
audio_path = "examples/audio/happy_dog.wav"
audio_waveform = processor.load_audio(audio_path)
audio_features = processor.extract_features(audio_waveform)

# 4. 预测VA值
with torch.no_grad():
    batch_features = torch.unsqueeze(audio_features, 0)  # 添加batch维度
    va_prediction = model.predict_va(batch_features)

print(f"效价 (Valence): {va_prediction['valence']:.3f}")
print(f"唤醒度 (Arousal): {va_prediction['arousal']:.3f}")
print(f"置信度 (Confidence): {va_prediction['confidence']:.3f}")

# 5. 情感解读
emotion = processor.interpret_va(
    va_prediction['valence'],
    va_prediction['arousal']
)
print(f"预测情感: {emotion}")
```

### 🎭 情感分类示例
```python
import numpy as np
from omniedge_petvoice import VAEmotionSpace

# 创建VA情感空间
va_space = VAEmotionSpace()

# 解析VA预测结果
valence = 0.73
arousal = 0.45

# 获取情感分类
emotion_class = va_space.classify_emotion(valence, arousal)
print(f"情感类别: {emotion_class}")

# 获取情感强度
intensity = va_space.calculate_intensity(valence, arousal)
print(f"情感强度: {intensity:.3f}")

# 可视化VA空间
va_space.visualize_emotion_space(valence, arousal)
```

## 🎧 音频处理 | Audio Processing

### 📊 特征提取
```python
from omniedge_petvoice import AudioProcessor
import librosa
import matplotlib.pyplot as plt

# 初始化处理器
processor = AudioProcessor(
    sample_rate=16000,
    n_fft=1024,
    hop_length=512,
    n_mels=128
)

# 加载音频
audio_path = "examples/audio/cat_meow.wav"
audio, sr = librosa.load(audio_path, sr=processor.sample_rate)

# 提取多种特征
features = {}

# 1. 梅尔频谱图
mel_spectrogram = processor.extract_mel_spectrogram(audio)
features['mel_spectrogram'] = mel_spectrogram

# 2. MFCC特征
mfcc = processor.extract_mfcc(audio, n_mfcc=13)
features['mfcc'] = mfcc

# 3. 音高特征
pitch = processor.extract_pitch(audio)
features['pitch'] = pitch

# 4. 能量特征
energy = processor.extract_energy(audio)
features['energy'] = energy

# 5. 零交叉率
zcr = processor.extract_zero_crossing_rate(audio)
features['zcr'] = zcr

print(f"特征形状:")
for name, feature in features.items():
    print(f"  {name}: {feature.shape}")

# 可视化梅尔频谱图
plt.figure(figsize=(12, 8))
plt.subplot(2, 3, 1)
plt.imshow(mel_spectrogram, aspect='auto', origin='lower')
plt.title('Mel Spectrogram')
plt.colorbar()

plt.subplot(2, 3, 2)
plt.plot(mfcc[0])
plt.title('MFCC Coefficients')

plt.subplot(2, 3, 3)
plt.plot(pitch)
plt.title('Pitch Contour')

plt.subplot(2, 3, 4)
plt.plot(energy)
plt.title('Energy')

plt.subplot(2, 3, 5)
plt.plot(zcr)
plt.title('Zero Crossing Rate')

plt.tight_layout()
plt.show()
```

### 🔧 批量处理
```python
import os
from glob import glob
from tqdm import tqdm

# 批量处理音频文件
def batch_process_audio(audio_dir, output_dir):
    """批量处理音频文件"""
    processor = AudioProcessor()

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有音频文件
    audio_files = glob(os.path.join(audio_dir, "*.wav"))

    results = []

    for audio_file in tqdm(audio_files, desc="处理音频文件"):
        try:
            # 加载音频
            audio = processor.load_audio(audio_file)

            # 提取特征
            features = processor.extract_features(audio)

            # 预测VA值
            va_pred = model.predict_va(torch.unsqueeze(features, 0))

            # 保存结果
            result = {
                'file': os.path.basename(audio_file),
                'valence': va_pred['valence'],
                'arousal': va_pred['arousal'],
                'confidence': va_pred['confidence']
            }
            results.append(result)

            # 保存单个结果
            output_file = os.path.join(
                output_dir,
                os.path.splitext(os.path.basename(audio_file))[0] + "_va.json"
            )
            import json
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)

        except Exception as e:
            print(f"处理失败 {audio_file}: {e}")

    return results

# 使用示例
results = batch_process_audio(
    "data/audio/",
    "results/va_predictions/"
)

print(f"成功处理 {len(results)} 个音频文件")
```

## 🎯 模型推理 | Model Inference

### 🔄 单样本推理
```python
def single_sample_inference(audio_path, model, processor):
    """单个样本推理"""
    try:
        # 加载和预处理音频
        audio = processor.load_audio(audio_path)
        features = processor.extract_features(audio)

        # 模型推理
        with torch.no_grad():
            batch_features = torch.unsqueeze(features, 0)
            outputs = model(batch_features)

        # 解析结果
        va_result = outputs['va']
        emotion_result = outputs['emotion']
        breed_result = outputs['breed']
        scene_result = outputs['scene']

        return {
            'file': audio_path,
            'va': {
                'valence': va_result['valence'].item(),
                'arousal': va_result['arousal'].item()
            },
            'emotion': {
                'prediction': torch.argmax(emotion_result['probabilities']).item(),
                'probabilities': emotion_result['probabilities'].squeeze().tolist()
            },
            'breed': {
                'prediction': torch.argmax(breed_result['probabilities']).item(),
                'probabilities': breed_result['probabilities'].squeeze().tolist()
            },
            'scene': {
                'prediction': torch.argmax(scene_result['probabilities']).item(),
                'probabilities': scene_result['probabilities'].squeeze().tolist()
            }
        }

    except Exception as e:
        return {'error': str(e), 'file': audio_path}

# 使用示例
result = single_sample_inference(
    "examples/audio/dog_bark.wav",
    model,
    processor
)

if 'error' not in result:
    print(f"文件: {result['file']}")
    print(f"VA预测: Valence={result['va']['valence']:.3f}, Arousal={result['va']['arousal']:.3f}")
    print(f"情感预测: {result['emotion']['prediction']} (置信度: {max(result['emotion']['probabilities']):.3f})")
else:
    print(f"推理失败: {result['error']}")
```

### 📊 批量推理
```python
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def batch_inference(audio_files, model, processor, max_workers=None):
    """批量推理"""
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()

    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        futures = [
            executor.submit(single_sample_inference, audio_file, model, processor)
            for audio_file in audio_files
        ]

        # 收集结果
        for future in tqdm(futures, desc="批量推理"):
            result = future.result()
            if 'error' not in result:
                results.append(result)

    return results

# 使用示例
audio_files = glob("data/test_audio/*.wav")[:10]  # 处理前10个文件
batch_results = batch_inference(audio_files, model, processor)

# 转换为DataFrame进行分析
df = pd.DataFrame([
    {
        'file': r['file'],
        'valence': r['va']['valence'],
        'arousal': r['va']['arousal'],
        'emotion': r['emotion']['prediction'],
        'emotion_conf': max(r['emotion']['probabilities']),
        'breed': r['breed']['prediction'],
        'scene': r['scene']['prediction']
    }
    for r in batch_results
])

print("批量推理结果统计:")
print(df.describe())

# 保存结果
df.to_csv("results/batch_inference_results.csv", index=False)
```

## 📈 结果可视化 | Results Visualization

### 🎨 VA空间可视化
```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_va_space(results, title="宠物情感VA空间分布"):
    """可视化VA空间分布"""
    valences = [r['va']['valence'] for r in results]
    arousals = [r['va']['arousal'] for r in results]

    plt.figure(figsize=(10, 8))

    # 创建散点图
    scatter = plt.scatter(
        valences, arousals,
        c=[r['emotion']['prediction'] for r in results],
        cmap='viridis', alpha=0.6, s=50
    )

    # 添加颜色条
    plt.colorbar(scatter, label='情感类别')

    # 添加网格和标签
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='--', alpha=0.3)
    plt.xlabel('效价 (Valence)')
    plt.ylabel('唤醒度 (Arousal)')
    plt.title(title)
    plt.grid(True, alpha=0.3)

    # 添加情感区域标签
    emotion_labels = {
        'excited': (0.7, 0.7, '兴奋'),
        'happy': (0.7, 0.2, '开心'),
        'calm': (0.2, -0.7, '平静'),
        'sad': (-0.7, -0.7, '悲伤'),
        'angry': (-0.7, 0.7, '愤怒'),
        'fearful': (-0.2, 0.7, '恐惧'),
        'relaxed': (0.2, -0.7, '放松'),
        'content': (0.7, -0.7, '满足')
    }

    for (x, y, label) in emotion_labels.values():
        plt.annotate(label, (x, y), fontsize=12, ha='center')

    plt.tight_layout()
    plt.show()

# 使用示例
plot_va_space(batch_results)
```

### 📊 情感分布图
```python
def plot_emotion_distribution(results):
    """绘制情感分布图"""
    emotions = [r['emotion']['prediction'] for r in results]
    emotion_counts = pd.Series(emotions).value_counts()

    plt.figure(figsize=(12, 6))

    # 条形图
    plt.subplot(1, 2, 1)
    emotion_counts.plot(kind='bar')
    plt.title('情感类别分布')
    plt.xlabel('情感类别')
    plt.ylabel('数量')
    plt.xticks(rotation=45)

    # 饼图
    plt.subplot(1, 2, 2)
    emotion_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title('情感类别比例')
    plt.ylabel('')

    plt.tight_layout()
    plt.show()

# 使用示例
plot_emotion_distribution(batch_results)
```

## 🔧 高级配置 | Advanced Configuration

### ⚙️ 自定义模型配置
```python
from omniedge_petvoice import create_pet_voice_model

# 创建自定义模型
custom_model = create_pet_voice_model(
    model_size="base",
    num_emotions=10,  # 自定义情感类别数
    num_breeds=20,    # 自定义品种数
    num_scenes=8,     # 自定义场景数
    task_weights={
        'va': 1.0,
        'emotion': 0.8,
        'breed': 0.4,
        'scene': 0.4
    }
)

# 自定义音频处理器
custom_processor = AudioProcessor(
    sample_rate=16000,
    n_fft=2048,
    hop_length=512,
    n_mels=128,
    n_mfcc=20,
    fmin=50,
    fmax=8000
)

print(f"自定义模型参数: {custom_model._get_model_summary()}")
```

### 🎯 实时处理
```python
import sounddevice as sd
import numpy as np

def real_time_audio_processing():
    """实时音频处理"""
    processor = AudioProcessor()

    def audio_callback(indata, frames, time, status):
        """音频回调函数"""
        if status:
            print(f"音频流状态: {status}")

        # 转换音频数据
        audio = indata.flatten()

        # 处理音频
        try:
            features = processor.extract_features(torch.from_numpy(audio))
            va_pred = model.predict_va(torch.unsqueeze(features, 0))

            emotion = processor.interpret_va(
                va_pred['valence'],
                va_pred['arousal']
            )

            print(f"实时VA: Val={va_pred['valence']:.2f}, "
                  f"Aro={va_pred['arousal']:.2f}, "
                  f"情感: {emotion}")

        except Exception as e:
            print(f"处理错误: {e}")

    # 启动音频流
    try:
        with sd.InputStream(
            callback=audio_callback,
            channels=1,
            samplerate=16000,
            blocksize=1024
        ):
            print("实时音频处理已启动，按 Ctrl+C 停止...")
            while True:
                sd.sleep(1000)

    except KeyboardInterrupt:
        print("实时处理已停止")

# 使用示例（需要安装 sounddevice: pip install sounddevice）
# real_time_audio_processing()
```

## 🚨 常见问题 | Troubleshooting

### ❓ 问题1: 模型加载失败
```python
# 解决方案：检查模型路径和格式
try:
    model = PetVoiceMultiTaskModel.from_pretrained("models/model.pth")
except FileNotFoundError:
    print("模型文件不存在，请检查路径")
except RuntimeError as e:
    print(f"模型加载失败: {e}")
    print("尝试使用CPU模式:")
    model = PetVoiceMultiTaskModel.from_pretrained(
        "models/model.pth",
        map_location='cpu'
    )
```

### ❓ 问题2: 音频格式不支持
```python
# 解决方案：转换音频格式
def convert_audio_format(input_path, output_path, target_sr=16000):
    """转换音频格式"""
    import librosa

    # 加载音频
    audio, sr = librosa.load(input_path, sr=target_sr)

    # 保存为目标格式
    sf.write(output_path, audio, target_sr)
    print(f"音频已转换: {input_path} -> {output_path}")

# 使用示例
convert_audio_format("input.mp3", "output.wav")
```

### ❓ 问题3: 内存不足
```python
# 解决方案：降低批处理大小
def memory_efficient_inference(audio_files, batch_size=1):
    """内存友好的推理"""
    results = []

    for i in range(0, len(audio_files), batch_size):
        batch = audio_files[i:i+batch_size]
        batch_results = batch_inference(batch, model, processor)
        results.extend(batch_results)

        # 清理GPU内存
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    return results
```

## 📚 下一步 | Next Steps

- 📖 查看[数据预处理教程](data_preprocessing.md)
- 🎯 学习[模型训练流程](training_pipeline.md)
- 🚀 了解[部署指南](deployment_guide.md)
- 📊 探索更多[高级示例](../examples/)

---

**需要帮助？**
📞 联系智子边界团队: **15915756011**
📧 技术支持: [通过微信获取]
🌐 GitHub Issues: [提交问题](https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel/issues)

---

*最后更新: 2025年10月27日 | Last Updated: October 27, 2025*