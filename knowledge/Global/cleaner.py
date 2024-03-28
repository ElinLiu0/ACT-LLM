#Author: Elin
#Date: 2024-03-28 13:02:48
#Last Modified by:   Elin
#Last Modified time: 2024-03-28 13:02:48

import json
from pydantic import BaseModel
import bs4
import pathlib
from typing import List,Dict
import os
from tqdm.auto import tqdm

class SimpleGithubExtractBody(BaseModel):
    title: str
    posttime: str
    type: str
    chats: List[Dict[str,str]]

def extract_github_issue(html_path:str,type:str) -> SimpleGithubExtractBody:
    print(f"Extracting {html_path} as {type}")
    with open(html_path, 'r') as f:
        html = f.read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    title = soup.find("bdi").text
    posttime = soup.find("relative-time")["datetime"]
    chats = []
    for chat in soup.find_all("div", class_="timeline-comment-group"):
        user = chat.find("a", class_="author").text
        content = chat.find("div", class_="edit-comment-hide").text.replace("\n","").replace("\r","").replace("\t","").replace("  ","")
        chats.append({"user":user,"content":content})
    print(f"Extracted {len(chats)} chats")
    return SimpleGithubExtractBody(title=title,posttime=posttime,type=type,chats=chats)

sub_paths = pathlib.Path(".").rglob("*.html")


# ACT_Issues = []
# Cactbot_Issues = []
FFIXV_ACT_Plugin_Issues = []
# OverlayPlugin_Issues = []

Unparsed = []

for sub_path in tqdm(sub_paths):
    try:
        splits = str(sub_path).split("/")[1]
        # if "ACT" in splits:
        #     ACT_Issues.append(extract_github_issue(sub_path,"ACT"))
        # elif "Cactbot" in splits:
        #     Cactbot_Issues.append(extract_github_issue(sub_path,"Cactbot"))
        if "FFXIV_ACT_Plugin" in splits:
            FFIXV_ACT_Plugin_Issues.append(extract_github_issue(sub_path,"FFXIV_ACT_Plugin")) # 用于测试，因此将其他类型的文档进行注释
        # elif "OverlayPlugin" in splits:
        #     OverlayPlugin_Issues.append(extract_github_issue(sub_path,"OverlayPlugin"))
    except:
        Unparsed.append(sub_path)
# Saving the extracted data
# with open("./cleaned/ACT/issues.json","w") as f:
#     f.write(json.dumps([issue.dict() for issue in ACT_Issues],indent=4))

# with open("./cleaned/Cactbot/issues.json","w") as f:
#     f.write(json.dumps([issue.dict() for issue in Cactbot_Issues],indent=4))

with open("./cleaned/FFXIV_ACT_Plugin/issues.json","w") as f:
    f.write(json.dumps([issue.dict() for issue in FFIXV_ACT_Plugin_Issues],indent=4))

# with open("./cleaned/OverlayPlugin/issues.json","w") as f:
#     f.write(json.dumps([issue.dict() for issue in OverlayPlugin_Issues],indent=4))
print(f"Below {len(Unparsed)} files were not parsed")
print(Unparsed)
print("Done")
