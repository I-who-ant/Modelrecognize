#!/bin/bash

# 智能笔记提交脚本
# 用法: ./quick_commit.sh "Day22" "Function Calling深度理解"

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数: 打印带颜色的信息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查参数
if [ $# -lt 1 ]; then
    print_error "用法: $0 <Day编号> [描述]"
    echo "示例: $0 Day22 'Function Calling深度理解'"
    exit 1
fi

DAY=$1
DESCRIPTION=${2:-"学习笔记更新"}

print_info "开始提交 $DAY 的学习笔记..."

# 检查是否有改动
if [ -z "$(git status --porcelain)" ]; then
    print_warning "没有检测到任何改动"
    exit 0
fi

# 显示改动文件
print_info "检测到以下改动:"
git status --short

# 统计信息
NEW_FILES=$(git status --short | grep "^??" | wc -l)
MODIFIED_FILES=$(git status --short | grep "^ M" | wc -l)

print_info "统计: 新增 $NEW_FILES 个文件, 修改 $MODIFIED_FILES 个文件"

# 添加所有改动
print_info "添加所有改动到暂存区..."
git add "Prompt-Engineering-Learning/第二阶段_Techniques/" 2>/dev/null || true
git add "Prompt-Engineering-Learning/第三阶段_Applications/" 2>/dev/null || true
git add "VideoLearningNote/" 2>/dev/null || true

# 生成commit message
COMMIT_MSG="📝 docs(prompt-eng): 完成${DAY}${DESCRIPTION}

🎯 本次提交内容:
- ✅ ${DAY}: ${DESCRIPTION}

📊 数据统计:
- 新增文件: ${NEW_FILES}个
- 修改文件: ${MODIFIED_FILES}个

💪 学习进度持续推进中!

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 提交
print_info "创建提交..."
git commit -m "$COMMIT_MSG"

print_success "提交成功!"

# 询问是否推送
read -p "是否立即推送到远程? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "推送到远程仓库..."
    git push origin main
    print_success "推送完成!"
else
    print_warning "已跳过推送，记得稍后执行 git push"
fi

print_success "所有操作完成! 🎉"
