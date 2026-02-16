# from google.adk.agents.llm_agent import LlmAgent
# from google.adk.agents.sequential_agent import SequentialAgent
# from google.adk.runners import InMemoryRunner
# import asyncio
# import json
# import os

# agent_model = 'gemini-2.5-flash'
# LOCAL_FILE_FALLBACK = "file:///mnt/data/My First Board (2).pdf"


# # ============================================================
# # 1. REFINER AGENT
# # ============================================================
# refiner = LlmAgent(
#     model=agent_model,
#     name="refiner_agent",
#     description="Refines user request into structured JSON.",
#     instruction=f"""
# You MUST output ONLY a single JSON object:

# {{
#   "refined_request": "<cleaned agent-friendly requirement>",
#   "website_link": "<url or default file URL if missing>",
#   "time_duration": "<requested duration>"
# }}

# Rules:
# - If no URL is given, set website_link to "{LOCAL_FILE_FALLBACK}".
# - Output must be valid JSON only.
#     """,
#     output_key="refiner_output"
# )


# # ============================================================
# # 2. READER AGENT
# # Uses: json.refiner_output.refined_request
# #       json.refiner_output.website_link
# # ============================================================
# reader = LlmAgent(
#     model=agent_model,
#     name="reader_agent",
#     description="Reads documentation and creates study plan.",
#     instruction="""
# You are given:

# refined_request = {json.refiner_output.refined_request}
# website_link    = {json.refiner_output.website_link}
# time_duration   = {json.refiner_output.time_duration}

# Task:
# 1. Read the documentation at website_link.
# 2. Extract important concepts.
# 3. Produce a full plan to master the technology within time_duration.

# Output ONLY:

# {
#   "plan": "<full learning plan>"
# }
# """,
#     output_key="reader_output"
# )


# # ============================================================
# # 3. NOTES AGENT
# # Uses: json.reader_output.plan
# # ============================================================
# notes_agent = LlmAgent(
#     model=agent_model,
#     name="notes_agent",
#     description="Creates detailed Markdown learning notes.",
#     instruction="""
# Use the plan created by reader:

# plan = {json.reader_output.plan}

# Produce detailed Markdown notes for the user. Include:
# - Weekly breakdown
# - Practical tasks
# - Examples
# - Complete theory + practice coverage

# Output JSON ONLY:

# {
#   "notes_md": "<markdown file content>"
# }
# """,
#     output_key="learning_notes"
# )


# # ============================================================
# # 4. MAIN PIPELINE
# # ============================================================
# root_agent = SequentialAgent(
#     name='DocumentationAssistantAgent',
#     sub_agents=[refiner, reader, notes_agent],
#     description='Pipeline: refine → read → generate notes'
# )


# # ============================================================
# # 5. RUNNER WITH VARIABLE ASSIGNMENT + SAVE MARKDOWN
# # ============================================================
# runner = InMemoryRunner(agent=root_agent)


# async def main():
#     user_input = "i want to master google agent development kit in 3 months, website_link=https://google.github.io/adk-docs/"

#     # ---- Run pipeline ----
#     result = await runner.run_debug(user_input)

#     print("\n=== RAW PIPELINE RESULT ===")
#     print(result)

#     # ----------------------------------------------------------
#     # EXTRACT VARIABLES (THIS IS WHAT YOU ASKED FOR)
#     # ----------------------------------------------------------
#     # All outputs from an agent are available under:
#     #
#     #     result["json"]["<output_key>"]
#     #
#     # Example: result["json"]["refiner_output"]["refined_request"]

#     refiner_output = result["json"]["refiner_output"]
#     reader_output = result["json"]["reader_output"]
#     notes_output = result["json"]["learning_notes"]

#     print("\n=== REFINER VARIABLE ===")
#     print(refiner_output)

#     print("\n=== READER VARIABLE ===")
#     print(reader_output)

#     print("\n=== NOTES VARIABLE ===")
#     print(notes_output)

#     # ----------------------------------------------------------
#     # SAVE NOTES TO .md FILE
#     # ----------------------------------------------------------
#     notes_md = notes_output["notes_md"]
#     output_path = "output.md"

#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(notes_md)

#     print(f"\nMarkdown notes saved to: {output_path}")


# # Run the async main method
# # asyncio.run(main())




from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools import google_search
from google.adk.runners import InMemoryRunner

agent_model='gemini-2.5-flash'
refiner=LlmAgent(
    model=agent_model,
    name="refiner_agent",
    description="""you are an excellently understand natural language of human, your task is to refine the user request to make it more precise and clear.""",
    instruction="""you are a help full agent.your job is, convert user query from natural language to agent understandable request.

    output formate:            
    refiner_output =    {
    "refined_request": "<string - refined version of user, that other agent can easily understand>",
    "website_link": "<string - use given url in the query>",
    "time_duration": "<string -user define time duration to master the technology>"
    }
    os dictionary  must be in json formate.

    Rules:
    - Use only the provided user input and the provided website link.
    - website_link must be a valid URL (https://google.github.io/adk-docs/)
    - Output MUST be parsable JSON; do NOT add any explanation or commentary.
    - if user not define you can split this learning process in to multiple phases.
    - if user, not give website link you can use google search tool to find the best website link for given user request.
    """,
    output_key="refined_request")
    #"website_link": "<string - use given url in the query>",
#i want master google agent development kit , website_link=https://google.github.io/adk-docs/

reader=LlmAgent(
    #print("hi"),
    model=agent_model,
    name="reader_agent",
    description="""you are an excellent web scrapper, you want to extraxt all content from user given website.""",
    instruction="""you are help full agent, your specific goal is full fill user request {refiner_output.refined_request} . user can give the website link, you job is to extract the all content from the given {refiner_output.website_link}.
                this is the website link for a documentation  of an specific technology.
                you can read the entire website and make {refiner_output.time_duration} plan for master this technology.
                
                output formate:
                reader_output =    {
                "plan": "<string - detail plan to master the given technology in given time duration>"
                 }""",
    output_key="plan"
    )

notes_agent= LlmAgent(
    model=agent_model,
    name="notes_agent",
    description="""you are a 20 years experience professor working in harward univercity for last 15 year. 
                   you recieved 3 nobel prize for teaching excellence. 
                   you are a pro in creating detail learning notes for student to master any technology. 
                   many scientist and engineer around the world follow your notes to master any technology.
                   """,
    instruction="""you are a help full agent, your job is to create detail learning notes by using the documentation link {refiner_output.website_link} for user to master the given technology based on the plan {reader_output.plan} created by reader agent.

    output formate:            
    {
    save as amrkdown file.
    }


    Rules:
    - that notes must alligned with the paln {reader_output.paln}, that means give youe notes for entire week plan.
    - that notes is must contain practical and theoretical knowldge to master the given technology.
    - the must contain all topic described in the plan {reader_output.plan}.
    """,
    output_key="learning_notes")


root_agent = SequentialAgent(
    #print("hi"),
    name='DocumentationAssistantAgent',
    sub_agents=[refiner,reader,notes_agent],
    description='A helpful assistant for user full dill the user request.'  
)
#from google.adk.agents.sequential_agent import SequentialAgent
# runner = InMemoryRunner(agent=root_agent)

# async def main():
#     response = await runner.run_debug(
#         "i want to master google agent development kit in 3 monthe, website_link=https://google.github.io/adk-docs/"
#     )
#     print(response)
#i want master google agent development kit, website_link=https://google.github.io/adk-docs/
#/Users/nirmalkumarvelu/Documents/project/glADKagent/bas_doc_agent/doc_agent/output.md
