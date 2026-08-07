import time

from google.genai.errors import ServerError

from src.llm.gemini_provider import GeminiProvider
from src.llm.groq_provider import GroqProvider

class ProviderManager:

    def __init__(self):

        self.providers = [
            ("Groq", GroqProvider()),
            ("Gemini", GeminiProvider())
        
        ]

    def invoke(self, prompt):

        last_exception = None

        for provider_name, provider in self.providers:

            print(f"\nUsing {provider_name}...")

            retries = 2

            while retries >= 0:

                try:

                    return provider.invoke(prompt)

                except ServerError as e:

                    last_exception = e

                    print(
                        f"{provider_name} ServerError. Retrying..."
                    )

                    retries -= 1

                    time.sleep(2)

                except Exception as e:

                    last_exception = e

                    print(f"{provider_name} failed.")

                    break

            print(
                f"Switching provider..."
            )

        raise RuntimeError(
            f"All providers failed.\n\n{last_exception}"
        )


_provider = None

def get_llm():
    global _provider

    if _provider is None:
        _provider = ProviderManager()

    return _provider