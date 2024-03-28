# Author: Elin
# Date: 2024-03-25 14:50:30
# Last Modified by:   Elin
# Last Modified time: 2024-03-25 14:50:30

# from Agent.Text.ACTAgentInText import ACTAgentInText
import json
from Agent.Global.ACTAgent import ACTGlobalAgent

chaining = []

# agent = ACTAgentInText(document_path="./knowledge/data.txt")

agent = ACTGlobalAgent(knowledge_base_path="./knowledge/")

cases = open("./Cases.txt","r").readlines()

for case in cases:
    temp = {}

    temp["Question"] = case

    temp["Answer"] = agent.run(case)

    chaining.append(temp)

with open("./TestingResult.json","w") as f:
    json.dump(chaining,f,ensure_ascii=False,indent=4)