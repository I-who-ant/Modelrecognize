"""练习22: Few-Shot Learning 实践"""

class FewShotPromptBuilder:
    def __init__(self, task_description: str):
        self.task = task_description
        self.examples = []
    
    def add_example(self, input_text: str, output_text: str, explanation: str = ""):
        self.examples.append({'input': input_text, 'output': output_text, 'explanation': explanation})
    
    def build_prompt(self, user_input: str) -> str:
        prompt = f"{self.task}\n\n# Examples\n\n"
        for i, ex in enumerate(self.examples, 1):
            prompt += f"## Example {i}\nInput: {ex['input']}\nOutput: {ex['output']}\n"
            if ex['explanation']:
                prompt += f"Explanation: {ex['explanation']}\n"
            prompt += "\n"
        prompt += f"# Your Task\nInput: {user_input}\nOutput:"
        return prompt

def demo_code_generation():
    builder = FewShotPromptBuilder("Task: Generate Python function")
    builder.add_example("Function to check if even", "def is_even(n: int) -> bool:\n    return n % 2 == 0")
    builder.add_example("Function to reverse string", "def reverse_string(s: str) -> str:\n    return s[::-1]")
    prompt = builder.build_prompt("Function to calculate factorial")
    print(prompt)

if __name__ == '__main__':
    demo_code_generation()
