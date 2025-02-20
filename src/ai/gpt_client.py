import openai


class GPTClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        openai.api_key = api_key
        openai.base_url = base_url
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def get_suggestion(self, messages):
        """Get suggestion from GPT based on chat messages"""
        try:
            response = self.client.chat.completions.create(
                model="azure_ptu",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant providing suggestions based on WeChat conversations.Respond in Chinese.",
                    },
                    {
                        "role": "user",
                        "content": f"Based on these messages, What should I reply: {messages}",
                    },
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting suggestion: {str(e)}"
