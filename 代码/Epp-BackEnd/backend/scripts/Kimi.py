import openai

openai.api_base = "https://api.moonshot.cn/v1"
openai.api_key = 'sk-yXyyuuFBxj3m8v0baMatcFATSB0XxjJYInNMOr5lPKGDyPAA'

if __name__ == '__main__':
    history = []
    while True:
        user_input = input("用户：")
        history.append({"role": "user", "content": user_input})
        if user_input.lower() == "exit":
            break
        response = openai.ChatCompletion.create(
            model="moonshot-v1-8k",
            messages=history,
            stream=False
        )
        print(response.choices[0].message.content)