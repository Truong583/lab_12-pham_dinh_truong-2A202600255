import random
import time

def ask(question: str) -> str:
    """
    Mock LLM function for demonstration purposes.
    Simulates a response from an AI model.
    """
    responses = [
        "Chào bạn! Tôi có thể giúp gì cho bạn hôm nay?",
        "Đây là một câu trả lời giả định từ AI Agent.",
        "Tôi đã nhận được câu hỏi: '{}'. Rất thú vị!",
        "Agent đang hoạt động tốt! Hỏi thêm đi nhé.",
        "Thông tin bạn cần đang được xử lý..."
    ]
    
    # Simulate processing time
    time.sleep(1)
    
    # Return a random response, occasionally including the question
    res = random.choice(responses)
    if "{}" in res:
        return res.format(question)
    return res
