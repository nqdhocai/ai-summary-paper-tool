import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GG_API_KEY"])

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 35,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-002",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

prompt = """
Đọc kỹ bài báo và tóm tắt lại với các thông tin chính sau và trả về dưới dạng markdown và trong ngôn ngữ tiếng việt nhưng giữ nguyên title là tiếng anh:

1.Vấn đề nghiên cứu (Research Problem):

 - Mục tiêu chính của nghiên cứu là gì?
 - Vấn đề hoặc câu hỏi nào bài báo đang cố gắng giải quyết?
2.Giả thuyết hoặc câu hỏi nghiên cứu (Hypothesis/Research Questions):

 - Các giả thuyết chính hoặc câu hỏi nghiên cứu mà bài báo đặt ra là gì?
3.Phương pháp nghiên cứu (Methods):

 - Phương pháp tiếp cận mà tác giả sử dụng để giải quyết vấn đề là gì?
 - Các công cụ, dữ liệu và quy trình cụ thể đã được áp dụng trong nghiên cứu?
4.Kết quả (Results):

 - Những kết quả quan trọng mà nghiên cứu thu được là gì?
 - Các số liệu hoặc thông tin cụ thể nào minh chứng cho những kết quả đó?
5.Thảo luận và phân tích (Discussion & Analysis):

 - Kết quả có ý nghĩa gì trong bối cảnh rộng hơn?
 - Tác giả có phân tích thêm hoặc đưa ra những kết luận quan trọng nào?
6.Kết luận và đề xuất (Conclusion & Recommendations):

 - Kết luận chính của bài báo là gì?
 - Có đề xuất gì cho nghiên cứu tương lai hoặc ứng dụng thực tiễn?
7.Hạn chế của nghiên cứu (Limitations):

 - Những hạn chế hoặc vấn đề chưa được giải quyết trong nghiên cứu là gì?
 
##Paper##
"""


def summarize_text(paper_path):
    paper_file = genai.upload_file(paper_path)
    return model.generate_content([prompt, paper_file]).text


class ChatSession:
    def __init__(self, history=[
      {
        "role":"user",
        "parts":[
          "Luôn đưa câu trả lời trong tiếng việt, nếu được yêu cầu viết code thì đưa ra đoạn code trong python theo yêu cầu"
        ]
      }
    ], model=model):
        self.history = history
        self.model = model

    def _updateHis(self, chat_turn):
        # chat_turn kiểu: {"role": "user" | "model", "parts": [...]}
        self.history.append(chat_turn)
        if len(self.history) >= 10:
            system_role = self.history[:2]  # Giữ lại 2 lượt đầu
            system_role.extend(self.history[-10:])  # Giữ lại 10 lượt cuối
            self.history = system_role

    def get_response(self, input):
        # Bắt đầu một phiên trò chuyện mới
        chat_session = model.start_chat(
            history=self.history
        )
        response = chat_session.send_message(input)  # Gửi tin nhắn
        self._updateHis({
            "role": "user",
            "parts": [input]
        })
        self._updateHis({
            "role": "model",
            "parts": [response.text]
        })
        return response.text
