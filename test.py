import openai
openai.api_key = "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"

prompt = "Hello, my name is John and I am a software engineer."
model = "text-davinci-003"
response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

generated_text = response.choices[0].text
print(generated_text)