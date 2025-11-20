import asyncio
from typing import List

class CrawledItem:
    def __init__(self, title: str, content: str, url: str):
        self.title = title
        self.content = content
        self.url = url

class NewsCrawler:
    async def crawl(self) -> List[CrawledItem]:
        # Mock data
        return [
            CrawledItem(
                "OpenAI Releases GPT-5",
                "OpenAI has announced the release of GPT-5, promising simpler reasoning and faster processing. The model is available now.",
                "https://example.com/gpt5"
            ),
            CrawledItem(
                "Google DeepMind's New AlphaFold",
                "DeepMind introduces the latest version of AlphaFold, capable of predicting protein structures with 99% accuracy.",
                "https://example.com/alphafold"
            ),
            CrawledItem(
                "Meta's Llama 4 is Open Source",
                "Meta has open-sourced Llama 4, a 400B parameter model that outperforms proprietary models on several benchmarks.",
                "https://example.com/llama4"
            ),
            CrawledItem(
                "AI in Healthcare: A Revolution",
                "New studies show AI diagnostics are reducing error rates in radiology by 30%. Hospitals are adopting the tech rapidly.",
                "https://example.com/ai-health"
            ),
            CrawledItem(
                "NVIDIA's New AI Chip",
                "NVIDIA reveals the H200 GPU, designed specifically for training massive language models with higher efficiency.",
                "https://example.com/nvidia"
            ),
            CrawledItem(
                "Apple Intelligence Features",
                "Apple integrates generative AI into iOS 19, offering smart replies and image generation on device.",
                "https://example.com/apple"
            ),
            CrawledItem(
                "Microsoft Copilot Updates",
                "Microsoft Copilot gets a major UI overhaul and deeper integration with Windows 12.",
                "https://example.com/microsoft"
            ),
            CrawledItem(
                "Anthropic's Claude 4",
                "Anthropic releases Claude 4 with a 1M token context window, making it ideal for analyzing entire codebases.",
                "https://example.com/claude"
            ),
            CrawledItem(
                "Tesla FSD v13",
                "Tesla's Full Self-Driving version 13 uses end-to-end neural networks for smoother city driving.",
                "https://example.com/tesla"
            ),
            CrawledItem(
                "AI Regulation Summit",
                "World leaders gather to discuss the future of AI regulation and safety standards.",
                "https://example.com/regulation"
            ),
        ]

class LLMSummarizer:
    async def summarize(self, text: str) -> str:
        # Mock summarization (just returning a fixed 3-line format for demo)
        # In a real scenario, this would call an LLM API.
        return f"Summary of: {text[:30]}...\nKey point 1: Major advancement in AI technology.\nKey point 2: Impact on industry is significant."
