from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Knock Knock"
        },
        {
            "role": "assistant",
            "content": "Who's there?"
        },
        {
            "role": "assistant",
            "content": "Lettuce."
        },
        {
            "role": "user",
            "content": "Lettuce who?"
        },

    ]
)

print(completion.choices[0].message)