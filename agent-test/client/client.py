from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/agent/")
response = remote_chain.invoke({
    "input": "What is the lenght of the word 'abac'",
    "chat_history": []  # Providing an empty list as this is the first call
})

print(response)