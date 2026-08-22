from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen3:4b",
    temperature=0
    #consistent responses
)

response = llm.invoke(
    "hi."
)

print(response.content)