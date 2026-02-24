import os
import sys
import asyncio
from colorama import init, Fore, Style
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage


#-----------------COLORAMA INIT---------------------
init(autoreset=True)

#----------------CRITICAL: ADD PROJECT ROOT TO PYTHONPATH--------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PROJECT_ROOT)

#--------------------ABSOLUTE import ONLY----------------------------
from mandate_agent.agent import get_mandate_agent


# ======================
# LLM
# ======================

llm = ChatOpenAI(
    model="NPCI_Greviance",
    base_url="http://183.82.7.228:9519/v1",
    api_key="sk-api",
    temperature=0.1,
)

# ======================
# ASYNC CHAT LOOP
# ======================


async def main():
    print(Fore.CYAN + "\n Initializing Mandate MCP Agent...")
    agent = get_mandate_agent(llm)
    print(Fore.GREEN + " Agent ready!\n")

    while True:
        user_input = input(Fore.YELLOW + " User: " + Style.RESET_ALL).strip()

        if user_input.lower() in {"exit", "quit", "q"}:
            print(Fore.CYAN + "\n Goodbye!")
            break

        if not user_input:
            continue

        try:
            initial_state = {
                "messages": [HumanMessage(content=user_input)]
            }

            result = await agent.ainvoke(initial_state)

            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage):
                    print(
                        Fore.GREEN + "\n AI:\n" +
                        Style.RESET_ALL + msg.content
                    )
                    break

        except Exception as e:
            print(Fore.RED + f"\n Error: {e}\n")

# ======================
# BOOT
# ======================

if __name__ == "__main__":
    asyncio.run(main())