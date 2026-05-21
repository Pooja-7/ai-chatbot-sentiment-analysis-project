from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class SentimentBot(ActivityHandler):
    def __init__(self, endpoint, api_key):
        self.client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )

    async def on_members_added_activity(
        self,
        members_added: [ChannelAccount],
        turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Hello! 👋 I am a sentiment analysis chatbot.\n"
                    "Type a message and I will analyze its sentiment."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        user_text = turn_context.activity.text

        try:
            response = self.client.analyze_sentiment(
                documents=[user_text]
            )[0]

            sentiment = response.sentiment
            confidence = response.confidence_scores

            reply = (
                f"🧠 **Sentiment Analysis Result**\n\n"
                f"Sentiment: **{sentiment.upper()}**\n"
                f"Positive: {confidence.positive:.2f}\n"
                f"Neutral: {confidence.neutral:.2f}\n"
                f"Negative: {confidence.negative:.2f}"
            )

        except Exception:
            reply = "⚠️ Sorry, I couldn't analyze that message."

        await turn_context.send_activity(reply)
