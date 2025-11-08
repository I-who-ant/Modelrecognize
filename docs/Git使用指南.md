# Git使用指南 - 老王特别版

## 🎯 快速开始

### 方式1: 使用快速提交脚本 (推荐!)

```bash
# 提交当天学习笔记
./scripts/quick_commit.sh "Day22" "Function Calling深度理解"

# 脚本会自动:
# 1. 检测改动文件
# 2. 添加到暂存区
# 3. 生成规范的commit message
# 4. 创建提交
# 5. 询问是否推送
```

### 方式2: 手动提交 (更灵活)

```bash
# 1. 查看改动
git status

# 2. 添加文件
git add "Prompt-Engineering-Learning/第二阶段_Techniques/"

# 3. 提交 (会自动加载模板)
git commit

# 4. 按照模板填写commit message

# 5. 推送到远程
git push origin main
```

---

## 📝 Commit Message 规范

### 基本格式

```
<emoji> <type>(<scope>): <subject>

<body>

<footer>
```

### Type类型说明

| Emoji | Type | 说明 | 示例 |
|-------|------|------|------|
| 📝 | docs | 文档/笔记更新 | 📝 docs(prompt-eng): 完成Day22学习 |
| ✨ | feat | 新功能 | ✨ feat(rag): 添加向量检索功能 |
| 🐛 | fix | Bug修复 | 🐛 fix(typo): 修复笔记中的错别字 |
| ♻️ | refactor | 代码重构 | ♻️ refactor: 优化笔记目录结构 |
| 🎨 | style | 格式调整 | 🎨 style: 统一Markdown格式 |
| ⚡ | perf | 性能优化 | ⚡ perf: 优化Git仓库大小 |
| 🎉 | release | 阶段完成 | 🎉 release: 完成第二阶段学习 |

### Scope范围说明

- `prompt-eng`: Prompt Engineering学习笔记
- `video-note`: 视频学习笔记
- `deepseek`: DeepSeek相关
- `project`: 项目代码
- `tools`: 工具脚本

---

## 💪 最佳实践示例

### 示例1: 单日学习笔记

```
📝 docs(prompt-eng): 完成Day22 Function Calling学习

🎯 本次提交内容:
- ✅ Day22主笔记: Function Calling完整机制
- ✅ 深度扩展1: 函数定义与类型系统
- ✅ 深度扩展2: 工具集成最佳实践
- ✅ 实践代码: 3个完整示例

📊 数据统计:
- 新增笔记: 3个
- 代码示例: 3个
- 总字数: ~8000字

💡 核心突破:
- 理解函数调用的底层机制
- 掌握OpenAI function calling API
- 实现工具链自动调用

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 示例2: 多日批量更新

```
📝 docs(prompt-eng): 完成Day22-24应用阶段学习

🎯 本次提交内容:
- ✅ Day22: Function Calling
  - 函数定义与调用机制
  - 工具集成最佳实践
  - 3个实战示例

- ✅ Day23: Generating Data
  - 数据生成策略
  - 质量控制方法
  - 多样性保证技术

- ✅ Day24: Generating Code
  - 需求到代码转换
  - 代码质量评估
  - 自动优化技术

📊 数据统计:
- 新增主笔记: 3个
- 深度扩展: 7个
- 实践代码: 12个
- 总字数: ~25000字

💪 学习深度: ⭐⭐⭐⭐⭐

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 示例3: 阶段性总结

```
🎉 release(prompt-eng): 完成第二阶段Techniques学习

🎯 阶段成就:
- ✅ 完成16天核心技术学习
- ✅ 掌握23种提示工程技术
- ✅ 创建50+深度扩展笔记
- ✅ 编写100+实践代码示例

📊 学习统计:
- 学习时长: 120小时
- 主笔记: 16个
- 深度扩展: 52个
- 实践项目: 8个
- 总字数: ~120000字

💡 核心掌握技术:
1. Zero/Few-Shot Prompting ⭐⭐⭐⭐⭐
2. Chain-of-Thought ⭐⭐⭐⭐⭐
3. Tree of Thoughts ⭐⭐⭐⭐⭐
4. ReAct Prompting ⭐⭐⭐⭐⭐
5. RAG (检索增强) ⭐⭐⭐⭐⭐
6. PAL (程序辅助) ⭐⭐⭐⭐⭐
7. Multimodal CoT ⭐⭐⭐⭐

🚀 下一步计划:
- 第三阶段: Applications (5天)
- 第四阶段: Prompt Hub (11天)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## 🚫 反面示例 (别这么写!)

### ❌ 太笼统
```
🎉 完成大量学习资料更新
```
**问题**: 看不出具体更新了什么

### ❌ 太简单
```
update
```
**问题**: 完全没有信息量

### ❌ 太啰嗦
```
今天我学习了Function Calling，感觉特别有收获，
理解了很多东西，然后写了一些笔记，还写了代码，
感觉很不错，明天继续加油...
```
**问题**: 废话太多，没有重点

---

## 🔧 Git别名配置 (可选)

在 `~/.gitconfig` 中添加:

```ini
[alias]
    # 查看美化的提交日志
    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit

    # 查看文件改动统计
    stat = status --short

    # 快速提交 (会加载模板)
    cm = commit

    # 快速添加并提交
    ac = !git add -A && git commit

    # 撤销最后一次提交 (保留改动)
    undo = reset --soft HEAD^

    # 查看最近5次提交
    last = log -5 --oneline

    # 推送当前分支
    push-current = push origin HEAD
```

使用示例:
```bash
git lg        # 查看美化日志
git stat      # 查看改动
git cm        # 提交 (加载模板)
git last      # 查看最近5次提交
```

---

## 💡 老王的建议

### 提交频率
- ✅ **每完成一个Day就提交一次** (推荐)
- ✅ **每天晚上提交当天所有学习内容**
- ⚠️ 避免攒很多天才提交一次

### 提交粒度
- ✅ **单日学习**: 一个commit
- ✅ **多日批量**: 一个commit (但要详细列出每天内容)
- ✅ **阶段完成**: 单独一个总结commit

### Commit Message要点
1. **第一行简明扼要** (50字内)
2. **空行后写详细内容**
3. **使用emoji增加可读性**
4. **记录数据统计**
5. **突出核心亮点**

### 推送时机
- ✅ 每天学习结束后推送
- ✅ 完成重要笔记后立即推送
- ⚠️ 避免长时间不推送 (容易丢失)

---

## 🎯 总结

**记住老王的口诀**:
```
Commit要勤快，Message要清楚
统计要详细，亮点要突出
Push要及时，备份不用愁
```

艹，崽芽子！按照老王这套规范来，你的Git历史会清晰得像艺术品一样！💪

---

**更新日期**: 2025-11-08
**作者**: 老王 + Claude Code
