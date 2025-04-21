from gradio_client import Client
promt = 'Придумай описание команды "Аналитики" для соревнований по программированию, дисциплина - "продуктовое программирование". Описание должен быть лаконичным и передавать название команды. Напиши одно описание и больше никакого текста'
client = Client("openfree/Deepseek-v3-0324-Research")
result = client.predict(
		message=promt,
		history=[],
		use_deep_research=False,
		api_name="/query_deepseek_streaming"
)
message,_ = result

print(message[0][-1].replace('*',''))