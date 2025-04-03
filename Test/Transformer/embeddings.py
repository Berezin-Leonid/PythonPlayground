from transformers import GPT2Tokenizer

# Загрузка предобученного токенизатора GPT-2
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Пример токенизации с более сложными словами
#text = "unhappiness is a complex word."
text = "Hello my friend."
tokens = tokenizer.tokenize(text)
print(tokens)