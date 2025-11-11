# 练习24: ReAct Pattern 实践

## ReAct 循环

```
User: 分析main.py的错误

Thought: 需要先读取文件看代码
Action: read_file("main.py")
Observation: [文件内容，第15行有TypeError]

Thought: 看到TypeError，搜索类似模式
Action: grep("TypeError", ".")
Observation: [在utils.py找到类似错误]

Thought: 明白了模式，修复它
Action: write_file("main.py", [修正后内容])
Observation: 文件更新成功

Final Answer: 修复了TypeError，添加了类型检查
```

## 关键要素
1. Thought: 推理
2. Action: 行动
3. Observation: 观察
4. 循环直到得出答案
