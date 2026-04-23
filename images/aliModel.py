from openai import OpenAI
import os

def get_response(messages):
    client = OpenAI(
        # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        api_key="sk-2b64e6b552d74f23a4a70b306ba1aedc",
        # 填写DashScope服务的base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-max",
        messages=messages,
        temperature=0.8,
        top_p=0.8
        )
    return completion

messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
# 您可以自定义设置对话轮数，当前为3
for i in range(30):
    user_input = input("请输入：")
    # 将用户问题信息添加到messages列表中
    messages.append({'role': 'user', 'content': user_input})
    assistant_output = get_response(messages).choices[0].message.content
    # 将大模型的回复信息添加到messages列表中
    messages.append({'role': 'assistant', 'content': assistant_output})
    print(f'用户输入：{user_input}')
    print(f'模型输出：{assistant_output}')
    print('\n')