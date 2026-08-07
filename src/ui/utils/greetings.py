from datetime import datetime


def greeting():

    hour = datetime.now().hour

    if hour < 12:

        return (
            "☀️ Good Morning",
            "Ready to expand your knowledge base today?",
        )

    elif hour < 17:

        return (
            "🌤 Good Afternoon",
            "Continue exploring your documents.",
        )

    else:

        return (
            "🌙 Good Evening",
            "What would you like to discover tonight?",
        )
