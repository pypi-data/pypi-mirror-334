# my_package/model_interface.py
class LLMInterface:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_text(self, prompt):
        raise NotImplementedError("子类必须实现此方法")


class QwenInterface(LLMInterface):
    def generate_text(self, prompt):
        # 模拟调用 Qwen 的 API
        return f"Qwen 生成的文本: {prompt}"


class GLMInterface(LLMInterface):
    def generate_text(self, prompt):
        # 模拟调用 GLM 的 API
        return f"GLM 生成的文本: {prompt}"