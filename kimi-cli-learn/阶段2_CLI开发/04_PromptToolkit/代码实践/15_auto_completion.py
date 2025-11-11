"""练习15: 自动补全实践 - 文件管理器补全"""
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from pathlib import Path

class FileManagerCompleter(Completer):
    def __init__(self):
        self.commands = {'ls': 'List', 'cd': 'Change dir', 'cat': 'Display', 'exit': 'Exit'}
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if len(words) == 0 or (len(words) == 1 and not text.endswith(' ')):
            yield from self._complete_commands(words[0] if words else '')
        else:
            yield from self._complete_paths(words[-1] if words else '')
    
    def _complete_commands(self, prefix: str):
        for cmd, desc in self.commands.items():
            if cmd.startswith(prefix):
                yield Completion(cmd, start_position=-len(prefix), display_meta=desc)
    
    def _complete_paths(self, prefix: str):
        try:
            if '/' in prefix:
                directory = Path(prefix).parent
                file_prefix = Path(prefix).name
            else:
                directory = Path.cwd()
                file_prefix = prefix
            if directory.exists():
                for path in sorted(directory.iterdir()):
                    if path.name.startswith(file_prefix):
                        display = f"{path.name}/" if path.is_dir() else path.name
                        yield Completion(path.name, start_position=-len(file_prefix), display=display)
        except:
            pass

def main():
    print("文件管理器 (使用Tab补全)\n")
    session = PromptSession(completer=FileManagerCompleter(), complete_while_typing=True) # 创建 PromptSession 实例，启用自动补全
    current_dir = Path.cwd()
    while True:
        try:
            text = session.prompt(f"{current_dir.name}> ").strip()
            if text == 'exit':
                break
            print(f"执行: {text}")
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == '__main__':
    main()
