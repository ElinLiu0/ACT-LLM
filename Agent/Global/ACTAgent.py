#Author: Elin
#Date: 2024-03-28 13:34:53
#Last Modified by:   Elin
#Last Modified time: 2024-03-28 13:34:53

from langchain.agents import (
    initialize_agent,
    Tool,
    AgentType,
    AgentExecutor
)
from langchain_openai import ChatOpenAI
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain.vectorstores.chroma import Chroma
from langchain.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from .Prompt import prompt
from utils.logger import logger


# 定义ACT智能体

class ACTGlobalAgent:
    def __init__(self,knowledge_base_path:str) -> None:
        try:
            logger.info(f"Initailizing knowledge base path {knowledge_base_path}.")
            self.knowledge_base_path = knowledge_base_path
            logger.info(f"Initailizing ChatOpenAI model.")
            self.llm = ChatOpenAI(
                temperature = 0
            )
            logger.info(f"Initailizing ChatOpenAI Embedding model.")
            self.embeddings = OpenAIEmbeddings()
            logger.info(f"Initailizing ACTAgent.")
            self.text_spliter = CharacterTextSplitter(
                chunk_size = 2000,
                chunk_overlap = 40
            )
            # 初始化ACT的知识库及QA链
            logger.info(f"Initalizing ACT's knowledge base and QA chain.")
            logger.info(f"Initalizing ACT Github issues document.")
            self.act_issues = JSONLoader(
                self.knowledge_base_path+"/Global/cleaned/ACT/"+'issues.json',
                jq_schema = ".[] | {title: .title,posttime: .postime,type: .type,chats: .chats}",
                text_content = False
            )
            logger.info(f"Loading ACT Github issues document.")
            self.act_doc = self.act_issues.load()
            logger.info(f"Splitting ACT Github issues document.")
            self.act_text = self.text_spliter.split_documents(self.act_doc)
            logger.info(f"Transfering ACT Github issues document to vector database via FAISS.")
            self.act_vdb = FAISS.from_documents(
                documents=self.act_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating ACT Q&A chain.")
            self.act_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type = "stuff",
                retriever = self.act_vdb.as_retriever()
            )
            # 初始化Cactbot的知识库及QA链
            logger.info(f"Initalizing Cactbot's knowledge base and QA chain.")
            logger.info(f"Initalizing Cactbot Github issues document.")
            self.cactbot_issuses = JSONLoader(
                self.knowledge_base_path+"/Global/cleaned/Cactbot/"+'issues.json',
                jq_schema = ".[] | {title: .title,posttime: .postime,type: .type,chats: .chats}",
                text_content = False
            )
            logger.info(f"Loading Cactbot Github issues document.")
            self.cactbot_doc = self.cactbot_issuses.load()
            logger.info(f"Splitting Cactbot Github issues document.")
            self.cactbot_text = self.text_spliter.split_documents(self.cactbot_doc)
            logger.info(f"Transfering Cactbot Github issues document to vector database via FAISS.")
            self.cactbot_vdb = FAISS.from_documents(
                documents=self.cactbot_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating Cactbot Q&A chain.")
            self.cactbot_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type = "stuff",
                retriever = self.cactbot_vdb.as_retriever()
            )
            # 初始化FFXIV_ACT_Plugin的知识库和QA链
            logger.info(f"Initalizing FFXIV_ACT_Plugin's knowledge base and QA chain.")
            self.ffxiv_act_plugin_issues = JSONLoader(
                self.knowledge_base_path+"/Global/cleaned/FFXIV_ACT_Plugin/"+'issues.json',
                jq_schema = ".[] | {title: .title,posttime: .postime,type: .type,chats: .chats}",
                text_content = False
            )
            logger.info(f"Loading FFXIV_ACT_Plugin Github issues document.")
            self.ffxiv_act_plugin_doc = self.ffxiv_act_plugin_issues.load()
            logger.info(f"Splitting FFXIV_ACT_Plugin Github issues document.")
            self.ffxiv_act_plugin_text = self.text_spliter.split_documents(self.ffxiv_act_plugin_doc)
            logger.info(f"Transfering FFXIV_ACT_Plugin Github issues document to vector database via FAISS.")
            self.ffxiv_act_plugin_vdb = FAISS.from_documents(
                documents=self.ffxiv_act_plugin_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating FFXIV_ACT_Plugin Q&A chain.")
            self.ffxiv_act_plugin_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type = "stuff",
                retriever = self.ffxiv_act_plugin_vdb.as_retriever()
            )
            # 初始化OverlayPlugin的知识库和QA链
            logger.info(f"Initalizing OverlayPlugin's knowledge base and QA chain.")
            self.overlay_plugin_issues = JSONLoader(
                self.knowledge_base_path+"/Global/cleaned/OverlayPlugin/"+'issues.json',
                jq_schema = ".[] | {title: .title,posttime: .postime,type: .type,chats: .chats}",
                text_content = False
            )
            logger.info(f"Loading OverlayPlugin Github issues document.")
            self.overlay_plugin_doc = self.overlay_plugin_issues.load()
            logger.info(f"Splitting OverlayPlugin Github issues document.")
            self.overlay_plugin_text = self.text_spliter.split_documents(self.overlay_plugin_doc)
            logger.info(f"Transfering OverlayPlugin Github issues document to vector database via FAISS.")
            self.overlay_plugin_vdb = FAISS.from_documents(
                documents=self.overlay_plugin_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating OverlayPlugin Q&A chain.")
            self.overlay_plugin_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type="stuff",
                retriever = self.overlay_plugin_vdb.as_retriever()
            )
            # 初始化设置(setup)文档及QA链
            logger.info(f"Initalizing Setup Guide Document and QA chain.")
            logger.info(f"Initalizing Setup Guide Document.")
            self.setup_guide = UnstructuredMarkdownLoader(
                self.knowledge_base_path+"/Global/cleaned/SETUP.md",
                text_content = False
            )
            logger.info(f"Loading Setup Guide Document.")
            self.setup_guide_doc = self.setup_guide.load()
            logger.info(f"Splitting Setup Guide Document.")
            self.setup_guide_text = self.text_spliter.split_documents(self.setup_guide_doc)
            logger.info(f"Transfering Setup Guide Document to vector database via FAISS.")
            self.setup_guide_vdb = FAISS.from_documents(
                documents=self.setup_guide_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating Setup Guide Document Q&A chain.")
            self.setup_guide_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type = "stuff",
                retriever = self.setup_guide_vdb.as_retriever()
            )
            # 初始化FAQ文档及QA链
            logger.info(f"Initalizing FAQ Document and QA chain.")
            self.faq_guide = UnstructuredMarkdownLoader(
                self.knowledge_base_path+"/Global/cleaned/FAQ.md",
                text_content = False
            )
            logger.info(f"Loading FAQ Document.")
            self.faq_guide_doc = self.faq_guide.load()
            logger.info(f"Splitting FAQ Document.")
            self.faq_guide_text = self.text_spliter.split_documents(self.faq_guide_doc)
            logger.info(f"Transfering FAQ Document to vector database via FAISS.")
            self.faq_guide_vdb = FAISS.from_documents(
                documents=self.faq_guide_text,
                embedding=self.embeddings,
            )
            logger.info(f"Creating FAQ Document Q&A chain.")
            self.faq_guide_chain = RetrievalQA.from_chain_type(
                llm = self.llm,
                chain_type = "stuff",
                retriever = self.faq_guide_vdb.as_retriever()
            )
            logger.info("Building tool sets for agent.")
            self.Tools = [
                Tool(
                    name = "ACTQAChain",
                    func = self.act_chain.run,
                    description = "useful for when you need answer questions about ACT docs."
                        "Input should be a fully formed question."
                ),
                Tool(
                    name = "CactbotQAChain",
                    func = self.cactbot_chain.run,
                    description = "useful for when you need answer questions about Cactbot docs."
                        "Input should be a fully formed question."
                ),
                Tool(
                    name = "FFXIVACTPluginQAChain",
                    func = self.ffxiv_act_plugin_chain.run,
                    description = "useful for when you need answer questions about FFXIV ACT Plugin docs."
                        "Input should be a fully formed question."
                ),
                Tool(
                    name = "OverlayPluginQAChain",
                    func = self.overlay_plugin_chain.run,
                    description = "useful for when you need answer questions about Overlay Plugin docs."
                        "Input should be a fully formed question."
                ),
                Tool(
                    name = "SetupGuideDocumentChain",
                    func = self.setup_guide_chain.run,
                    description = "useful for when you need answer questions about how to setup act,Overlay Plugin,etc."
                        "Input should be a fully formed question."
                ),
                Tool(
                    name = "FAQDocumentChain",
                    func = self.faq_guide_chain.run,
                    description = "useful for when you need answer questions about the problems during setup ACT and Overlay Plugin."
                        "Input should be a fully formed question."
                ),
            ]
            # 创建绑定工具集的LLM
            logger.info("Binding tools to LLM.")
            self.llm_with_tools = self.llm.bind_tools(self.Tools)
            # 初始化Agent
            logger.info("Initializing Agent.")
            self.agent = (
                {
                    "input":lambda x: x["input"],
                    "agent_scrathpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    )
                }
                | prompt
                | self.llm_with_tools
                | OpenAIToolsAgentOutputParser()
            )
            logger.info("Initializing Agent Executor.")
            # 初始化智能体执行器
            self.executor = AgentExecutor(
                agent=self.agent,
                tools = self.Tools,
                verbose = True
            )
        except Exception as e:
            logger.error(f"Error: {e} been raised at ACTAgent.__init__() at line {e.__traceback__.tb_lineno}.")
    
    def run(self,query:str) -> str:
        try:
            logger.info(f"Running ACTAgent with query: {query}.")
            result = self.executor.invoke({"input":query})
            return result["output"]
        except Exception as e:
            logger.error(f"Error: {e} been raised at ACTAgent.run() at line {e.__traceback__.tb_lineno}.")

