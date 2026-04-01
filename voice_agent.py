import asyncio
import os
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.google import GoogleLLMService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.transports.services.daily import DailyParams, DailyTransport
from pipecat.vad.silero import SileroVADAnalyzer
from loguru import logger

async def main():
    transport = DailyTransport(
        os.environ["DAILY_ROOM_URL"],
        os.environ["DAILY_API_KEY"],
        "SmartCore Voice Agent",
        DailyParams(audio_out_enabled=True, vad_enabled=True, vad_analyzer=SileroVADAnalyzer())
    )
    stt = DeepgramSTTService(api_key=os.environ["DEEPGRAM_API_KEY"])
    tts = CartesiaTTSService(api_key=os.environ["CARTESIA_API_KEY"], voice_id="79a125e8-cd45-4c13-8a67-188112f4dd22")
    llm = GoogleLLMService(api_key=os.environ["GOOGLE_API_KEY"], model="gemini-2.0-flash")
    messages = [{"role": "system", "content": "You are SmartCore, a helpful and friendly AI voice assistant. Be concise and natural in your responses."}]
    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(context)
    pipeline = Pipeline([transport.input(), stt, context_aggregator.user(), llm, tts, transport.output(), context_aggregator.assistant()])
    task = PipelineTask(pipeline, PipelineParams(allow_interruptions=True))
    await PipelineRunner().run(task)

if __name__ == "__main__":
    asyncio.run(main())
