
server_ip = '172.17.62.88'
url = f'http://172.17.62.88:20005'
            
from openai import OpenAI
 
client = OpenAI(
    api_key="none",
    base_url="http://{server_ip}:20005/v1",
)
 
completion = client.chat.completions.create(
  model="chatglm3-6b",
  messages=[
    {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
    {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
  ],
  temperature=0.3,
)
 
print(completion.choices[0].message)