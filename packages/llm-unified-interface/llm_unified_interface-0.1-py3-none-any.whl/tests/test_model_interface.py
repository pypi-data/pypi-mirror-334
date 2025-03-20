# tests/test_model_interface.py
import unittest
from my_package.model_interafce import   QwenInterface, GLMInterface

class TestLLMInterface(unittest.TestCase):
    def test_qwen(self):
        qwen = QwenInterface("Qwen")
        result = qwen.generate_text("你好")
        self.assertEqual(result, "Qwen 生成的文本: 你好")

    def test_glm(self):
        glm = GLMInterface("GLM")
        result = glm.generate_text("你好")
        self.assertEqual(result, "GLM 生成的文本: 你好")

if __name__ == "__main__":
    unittest.main()