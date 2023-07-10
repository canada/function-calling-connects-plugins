from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import AIPluginTool
from langchain.agents.mrkl import prompt
from langchain.callbacks import StdOutCallbackHandler

#import langchain; langchain.debug = True
import os

# .envからAPIキーを読み込む
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")

plugin_urls = ["http://localhost:5000/.well-known/ai-plugin.json"]

tools = load_tools(["requests_all"])
tools += [AIPluginTool.from_plugin_url(url) for url in plugin_urls]

SUFFIX = """'
When you asnwer to Human, pretend if you are the great travel assistant AI and be polite every messages.
'Answer should be in Japanese. Use http instead of https for endpoint.
When you specify URL into Action Input, just show URL ONLY! ex: Action Input: https://www.google.com/
Use "-key: value" list to display detail information.
"""

# デバッグ用のコールバックハンドラ
handler = StdOutCallbackHandler()

# エージェントの初期化
agent_chain = initialize_agent(tools,
                            llm,
                            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True,
                            agent_kwargs=dict(suffix=SUFFIX + prompt.SUFFIX,
                            callbacks=[handler],
                        ))

# 質問からAIの返答を取得する
# initialize_agent
def get_answer(question):
    answer = agent_chain.run(question)
    return answer

if __name__ == "__main__":
    while True:
        question = input(">> ")
        answer = get_answer(question)
        print(answer)
