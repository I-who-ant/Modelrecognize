"""练习25: Function Calling 基础实践"""
import json

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file contents",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "File path"}
                },
                "required": ["file_path"]
            }
        }
    }
]

class ToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, name: str, func):
        self.tools[name] = func
    
    def execute(self, name: str, **kwargs):
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")
        return self.tools[name](**kwargs)

def read_file(file_path: str) -> str:
    with open(file_path) as f:
        return f.read()

def main():
    registry = ToolRegistry()
    registry.register("read_file", read_file)
    print(f"可用工具: {list(registry.tools.keys())}")

if __name__ == '__main__':
    main()
