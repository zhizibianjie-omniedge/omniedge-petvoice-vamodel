# 贡献指南 | Contributing Guidelines

[![Contributors Welcome](https://img.shields.io/badge/Contributors-Welcome-brightgreen.svg)](https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel)
[![License MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PR Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel/pulls)

## 🌟 欢迎贡献 | Welcome to Contribute

感谢您对 **PetVoice VA Model** 项目的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 **Bug修复** | **Bug Fixes**
- ✨ **新功能开发** | **Feature Development**
- 📚 **文档改进** | **Documentation Improvement**
- 🧪 **测试用例** | **Test Cases**
- 🎨 **UI/UX优化** | **UI/UX Enhancement**
- 🌐 **多语言支持** | **Multi-language Support**
- 🔧 **性能优化** | **Performance Optimization**

## 📋 开始之前 | Before You Start

### 🎯 了解项目
请先阅读以下文档以了解项目背景：

- 📖 **[项目README](README.md)** - 项目概览和快速开始
- 📄 **[论文原文](https://arxiv.org/abs/2510.12819)** - 了解技术原理
- 👥 **[团队介绍](docs/business/omni-edge-team.md)** - 了解我们的团队
- 📊 **[数据集介绍](docs/dataset/pet-vocalization-dataset.md)** - 了解数据资源

### 🤝 联系我们
在开始大规模贡献之前，建议先联系我们：

**微信**: **15915756011**
**邮件**: [通过微信获取]

这样我们可以：
- 讨论您的想法和计划
- 确保贡献方向与项目目标一致
- 提供必要的技术支持和指导

## 🚀 快速开始 | Quick Start

### 📋 环境准备
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
```

### 🔧 开发设置
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装pre-commit钩子
pre-commit install

# 运行测试确保环境正常
python -m pytest tests/
```

## 📝 贡献流程 | Contribution Process

### 🎯 第一步：创建Issue
在开始工作之前，请创建或查找相关的Issue：

- **新功能**: 创建 `feature request` issue
- **Bug报告**: 创建 `bug` issue
- **文档改进**: 创建 `documentation` issue
- **其他**: 创建合适的issue类型

### 🌿 第二步：Fork和分支
```bash
# Fork仓库到您的GitHub账户

# 克隆您的fork
git clone https://github.com/YOUR_USERNAME/omniedge-petvoice-vamodel.git
cd omniedge-petvoice-vamodel

# 添加上游仓库
git remote add upstream https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel.git

# 创建新分支
git checkout -b feature/your-feature-name
# 或 git checkout -b fix/your-bug-fix
```

### 💻 第三步：开发工作
1. **遵循代码规范** (见下方)
2. **编写测试用例**
3. **更新相关文档**
4. **确保所有测试通过**

### ✅ 第四步：提交和推送
```bash
# 添加文件
git add .

# 提交（遵循提交信息规范）
git commit -m "feat: add new feature description"

# 推送到您的fork
git push origin feature/your-feature-name
```

### 🎉 第五步：创建Pull Request
1. 在GitHub上创建Pull Request
2. 填写PR模板（见下方）
3. 等待代码审查
4. 根据反馈进行修改

## 📏 代码规范 | Code Standards

### 🐍 Python代码风格
我们使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查
- **pytest**: 单元测试

```bash
# 格式化代码
black src/ tests/ examples/

# 排序导入
isort src/ tests/ examples/

# 代码检查
flake8 src/ tests/ examples/

# 类型检查
mypy src/

# 运行测试
pytest tests/
```

### 📝 命名规范
- **变量和函数**: `snake_case`
- **类名**: `PascalCase`
- **常量**: `UPPER_SNAKE_CASE`
- **文件名**: `snake_case.py`

### 📚 文档规范
- **docstring**: 使用Google风格
- **类型注解**: 所有公共函数必须包含
- **注释**: 解释复杂逻辑，而非简单描述

```python
def predict_va(self, audio_features: torch.Tensor) -> Dict[str, float]:
    """预测音频的效价-唤醒度值

    Args:
        audio_features: 提取的音频特征张量

    Returns:
        包含valence和arousal预测值的字典

    Raises:
        ValueError: 当输入特征维度不匹配时
    """
    pass
```

## 📋 提交信息规范 | Commit Message Guidelines

我们遵循[Conventional Commits](https://www.conventionalcommits.org/)规范：

### 🎯 格式
```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

### 📝 类型说明
- **feat**: 新功能
- **fix**: Bug修复
- **docs**: 文档更新
- **style**: 代码格式调整
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建或辅助工具变动

### 💡 示例
```bash
feat(model): add multi-task learning support

- Add emotion classification head
- Implement dynamic weight adjustment
- Update training pipeline

Fixes #123
```

## 🧪 测试指南 | Testing Guidelines

### 📊 测试覆盖率
- **目标覆盖率**: 85%+
- **关键代码**: 95%+
- **示例代码**: 100%

### 🎯 测试类型
1. **单元测试**: 测试单个函数/类
2. **集成测试**: 测试组件交互
3. **端到端测试**: 测试完整流程
4. **性能测试**: 测试模型性能

### 📝 测试文件结构
```
tests/
├── unit/           # 单元测试
│   ├── test_model.py
│   ├── test_data.py
│   └── test_utils.py
├── integration/    # 集成测试
│   ├── test_pipeline.py
│   └── test_training.py
├── e2e/           # 端到端测试
│   └── test_full_workflow.py
└── performance/   # 性能测试
    └── test_model_performance.py
```

### 🚀 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_model.py

# 查看覆盖率
pytest --cov=src tests/

# 生成覆盖率报告
pytest --cov=src --cov-report=html tests/
```

## 📚 文档贡献 | Documentation Contributions

### 📖 文档类型
1. **API文档**: 代码中的docstring
2. **用户指南**: examples/目录下的教程
3. **技术文档**: docs/technical/目录
4. **论文文档**: docs/paper/目录

### ✍️ 写作规范
- **语言**: 中文为主，重要文档提供英文版本
- **格式**: 使用Markdown格式
- **结构**: 清晰的层次结构
- **图片**: 适当使用图表和示例

### 🎯 文档优先级
1. **高优先级**: README、API文档、核心教程
2. **中优先级**: 技术详解、使用案例
3. **低优先级**: 博客文章、FAQ

## 🔍 Pull Request指南 | Pull Request Guidelines

### 📋 PR模板
请使用以下模板创建PR：

```markdown
## 📋 变更描述 | Description
简要描述本次变更的内容和目的

## 🎯 变更类型 | Type of Change
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 🧪 测试 | Testing
- [ ] 添加了新的测试用例
- [ ] 所有现有测试通过
- [ ] 测试覆盖率达标

## 📚 文档 | Documentation
- [ ] 更新了相关文档
- [ ] 添加了使用示例
- [ ] 更新了README

## ✅ 检查清单 | Checklist
- [ ] 代码符合项目规范
- [ ] 提交信息符合规范
- [ ] 没有引入新的警告
- [ ] 通过了所有CI检查

## 🔗 相关Issue | Related Issues
关联的Issue编号：#

## 📷 截图 (如适用)
如果适用，请添加截图

## 📝 其他说明 | Additional Notes
其他需要说明的内容
```

### 🎯 PR审查流程
1. **自动检查**: CI/CD自动运行测试
2. **代码审查**: 维护者进行人工审查
3. **反馈修改**: 根据反馈进行修改
4. **合并**: 审查通过后合并

## 🏷️ 发布管理 | Release Management

### 📋 版本规范
我们使用[语义化版本](https://semver.org/)：
- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 🎯 发布流程
1. **准备发布**: 更新版本号和CHANGELOG
2. **创建标签**: 创建Git标签
3. **自动发布**: GitHub Actions自动发布
4. **通知更新**: 通知相关方

## 🤝 社区准则 | Community Guidelines

### 😊 行为准则
- **尊重他人**: 保持友善和专业
- **建设性反馈**: 提供建设性的意见
- **包容性**: 欢迎不同背景的贡献者
- **专注技术**: 讨论聚焦技术内容

### 🚫 禁止行为
- 人身攻击或不当言论
- 垃圾信息或无关内容
- 恶意代码或安全漏洞
- 侵犯他人知识产权

## 🎁 贡献者认可 | Contributor Recognition

### 🏆 贡献者权益
- **署名权**: 在README中列名
- **技术分享**: 参与技术讨论和决策
- **优先合作**: 商业合作优先考虑
- **推荐机会**: 工作和学习机会推荐

### 📊 贡献统计
我们会在以下方面统计贡献：
- **代码贡献**: 提交数量和质量
- **文档贡献**: 文档改进和新内容
- **Issue处理**: 问题解决和讨论
- **社区影响**: 对社区的积极影响

## 🆘 获取帮助 | Getting Help

### 💬 联系方式
- **微信**: 15915756011
- **Issue**: [GitHub Issues](https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel/issues)
- **Discussion**: [GitHub Discussions](https://github.com/zhizibianjie-omniedge/omniedge-petvoice-vamodel/discussions)

### 📚 学习资源
- **项目文档**: [docs/](docs/)
- **示例代码**: [examples/](examples/)
- **论文原文**: [arXiv:2510.12819](https://arxiv.org/abs/2510.12819)
- **相关技术**: 音频处理、深度学习、情感计算

## 📄 许可证 | License

通过贡献代码，您同意您的贡献将在[MIT许可证](LICENSE)下发布。

---

<div align="center">

## 🌟 感谢您的贡献！🌟

**PetVoice VA Model 项目因您的参与而更加完善**

**智子边界 (OmniEdge) 团队**

</div>

---

*最后更新: 2025年10月27日 | Last Updated: October 27, 2025*