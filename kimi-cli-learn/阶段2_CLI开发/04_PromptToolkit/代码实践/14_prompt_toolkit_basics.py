"""练习14: Prompt Toolkit 基础实践 - 交互式计算器"""
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.validation import Validator, ValidationError

class ExpressionValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            return
        try:
            eval(text, {"__builtins__": {}}, {})
        except Exception as e:
            raise ValidationError(message=f'无效表达式: {e}', cursor_position=len(text))

def main():
    print("交互式计算器 (Ctrl-D退出)\n")
    session = PromptSession(validator=ExpressionValidator(), validate_while_typing=False, history=InMemoryHistory())
    while True:
        try:
            prompt = HTML('<prompt>calc</prompt> >>> ')
            text = session.prompt(prompt)
            if not text.strip():
                continue
            result = eval(text, {"__builtins__": {}}, {})
            print(f"  = {result}\n")
        except KeyboardInterrupt:
            continue
        except EOFError:
            print("\n再见！")
            break

if __name__ == '__main__':
    main()
