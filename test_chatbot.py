import chatgui

response = chatgui.chatbot_response("Hello there")
assert isinstance(response, str) and len(response) > 0
print("chatbot_response ok:", response)
