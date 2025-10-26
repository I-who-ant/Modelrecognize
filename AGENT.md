# 仓库使用说明

## 目标定位
- 将本仓库作为深度学习自学与推理实验的主场，聚焦理解 DeepSeek 系列模型的架构与推理流程。
- 在 `DeepSeek-V3-main/VideoLearningNote/` 中维护结构化笔记，记录学习体会、疑问以及后续行动。
- 对上游镜像（`DeepSeek-V3-main`、`DeepSeek-OCR-ForLearning`）默认只读，除非实验明确需要修改。

## 目录速览
- `DeepSeek-V3-main/`：DeepSeek-V3 官方发布仓库。阅读 `LEARNING_GUIDE.md`、`COURSE_LEARNING_GUIDE.md` 及 `inference/` 中的脚本获取基线说明。
- `DeepSeek-V3-main/VideoLearningNote/`：学习笔记主目录，遵循 `CLAUDE.md` 约定的模板，并使用 `QA_快速查询.md` 建立概念索引。
- `DeepSeek-OCR-ForLearning/`：DeepSeek-OCR 相关资料，按照 README 搭建 vLLM 或 Transformers 推理环境。
- `.spec-workflow/`：Spec 工作流产物，除非需要扩展模板，否则保持目录结构不动。

## 推荐工作流
1. **学习阶段**：在进入新主题前，先阅读 `DeepSeek-V3-main` 内的官方指南与论文。
2. **记录阶段**：每完成一个概念，按 `VideoLearningNote/` 中的 Markdown 模板补充笔记；出现新关键词时同步更新 `QA_快速查询.md`。
3. **实践阶段**：如需代码实验，使用独立分支或建立 `experiments/` 子目录，避免污染上游镜像。
4. **复盘阶段**：定期回顾 `CLAUDE.md` 的进度追踪，优先推进 Attention 与 Transformer 相关主题。

## 维护原则
- 坚持 KISS/YAGNI：保持笔记简洁，清理过期草稿，避免为未来需求预留冗余结构。
- 遵循 DRY：各处引用同一概念时，通过链接指向原始笔记，避免重复维护。
- 修改官方代码前先制定清晰方案与记录，优先通过附加脚本或外层目录实现。
- Markdown 默认使用 ASCII；如需添加图示或特殊字符，确认文件已有相应用法。

## 后续提示
- 补全 `VideoLearningNote/` 中 Attention 与 Transformer 章节的核心条目。
- 当开始推理或 Benchmark 实验时，创建 `experiments/` 目录集中管理脚本与日志。

> 每次开始学习前先阅读本文件，可快速恢复仓库上下文。
