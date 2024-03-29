# Author: Elin
# Date: 2024-03-25 14:50:30
# Last Modified by:   Elin
# Last Modified time: 2024-03-25 14:50:30

# from Agent.Text.ACTAgentInText import ACTAgentInText
import json
from Agent.Global.ACTAgent import ACTGlobalAgent
from utils.logger import logger

logger.info("Initializing the testing script")
logger.info("Initializing the vectorizer")

chaining = []

# agent = ACTAgentInText(document_path="./knowledge/data.txt")
logger.info("Initializing the agent")
agent = ACTGlobalAgent(knowledge_base_path="./knowledge/")
logger.info("Loading test cases")
cases = json.loads(open("./Cases.json","r").read())

index = 1

for case in cases:
    try:
        logger.info(f"Executing test case {index}")
        temp = {}

        temp["Question"] = case["Question"]

        temp["Answer"] = agent.run(case["Question"])

        chaining.append(temp)
        logger.info(f"Test case {index} executed.")
        index += 1
    except Exception as e:
        logger.error(f"Error in case {index}, error message is {e}")
        break

with open("./TestingResult.json","w") as f:
    json.dump(chaining,f,ensure_ascii=False,indent=4)
