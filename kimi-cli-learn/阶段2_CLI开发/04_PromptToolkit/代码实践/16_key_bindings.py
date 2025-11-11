"""练习16: 快捷键绑定实践"""
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.enums import EditingMode
import datetime

bindings = KeyBindings()

@bindings.add('c-t')
def _(event):
    """Ctrl+T: 插入时间戳"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    event.current_buffer.insert_text(timestamp)

def main():
    print("文本编辑器 (Ctrl+T插入时间, Ctrl+D退出)\n")
    session = PromptSession(key_bindings=bindings, multiline=False) #
    while True:
        try:
            text = session.prompt('> ')
            if text.strip():
                print(f"输入: {text}")
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == '__main__':
    main()



