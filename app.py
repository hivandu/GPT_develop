'''
Author: Hivan Du
mail: 
LastEditors: Hivan Du
LastEditTime: 2023-05-13 23:55:57
'''
import openai
import gradio as gr
import os

openai.api_key = "OPENAI_API_KEY"

class Conversation:
    def __init__(self, prompt, num_of_round):
        self.prompt = prompt
        self.num_of_round = num_of_round
        self.messages = []
        self.messages.append({"role": "system", "content": self.prompt})

    def ask(self, question):
        try:
            self.messages.append( {"role": "user", "content": question})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.messages,
                temperature=0.5,
                max_tokens=2048,
                top_p=1,
            )
        except Exception as e:
            print(e)
            return e

        message = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": message})
        
        if len(self.messages) > self.num_of_round*2 + 1:
            del self.messages[1:3]
        return message
    

prompt = """
你是一个律师，用中文回答一些法律的问题。你的回答需要满足以下要求:
1. 你的回答必须是中文
2. 回答限制在100个字以
"""

conv = Conversation(prompt, 5)

def predict(input, history=[]):
    history.append(input)
    response = conv.ask(input)
    history.append(response)
    responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
    return responses, history

with gr.Blocks(css="#chatbot{height:350px} .overflow-y-auto{height:500px}") as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)

    txt.submit(predict, [txt, state], [chatbot, state])

demo.launch()