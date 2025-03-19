from atai_gemma3_tool.regex_filter import setup_logging_filter
import argparse
import threading
import asyncio
from PIL import Image
from transformers import AutoProcessor, Gemma3ForConditionalGeneration, TextIteratorStreamer
import torch
import requests
from io import BytesIO

setup_logging_filter()

async def stream_tokens_async(inputs, processor, model):
    """
    Async generator that streams tokens using an asyncio queue,
    """
    # Create a streamer that yields decoded tokens.
    streamer = TextIteratorStreamer(processor, skip_prompt=True, skip_special_tokens=True)

    # Start model generation in a separate thread.
    def generate():
        model.generate(**inputs, max_new_tokens=8000, do_sample=False, streamer=streamer)
    threading.Thread(target=generate).start()

    # Set up an asyncio queue and a helper thread to enqueue tokens.
    loop = asyncio.get_running_loop()
    q = asyncio.Queue()

    def enqueue_tokens():
        for token in streamer:
            loop.call_soon_threadsafe(q.put_nowait, token)
        loop.call_soon_threadsafe(q.put_nowait, None)  # Sentinel to signal completion.
    threading.Thread(target=enqueue_tokens).start()

    # Yield tokens from the queue as they become available.
    while True:
        token = await q.get()
        if token is None:
            break
        yield token

async def generate_text_from_image_async(image_path: str, prompt: str, stream_output: bool):
    model_id = "google/gemma-3-4b-it"

    # Load the image from a URL or a local file.
    if image_path.startswith("http://") or image_path.startswith("https://"):
        try:
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Error fetching image from URL {image_path}: {e}")
            return
    else:
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Error opening image {image_path}: {e}")
            return  

    print("Loading model and processor. This may take a few minutes...")
    model = Gemma3ForConditionalGeneration.from_pretrained(
        model_id, device_map="auto", torch_dtype=torch.bfloat16
    ).eval()
    processor = AutoProcessor.from_pretrained(model_id) # Temp, Current do not support:use_fast=True

    # Build the chat payload using the provided prompt.
    payload = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}]
        },
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image},
                {"type": "text", "text": prompt}
            ]
        }
    ]

    # Preprocess the payload for generation.
    inputs = processor.apply_chat_template(
        payload,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt"
    ).to(model.device, dtype=torch.bfloat16)

    # Stream tokens asynchronously and print them as they arrive.
    if stream_output:
        # Streaming output: print tokens as they arrive.
        async for token in stream_tokens_async(inputs, processor, model):
            print(token, end="", flush=True)
        print()
    else:
        # Non-streaming: collect all tokens and print them at once.
        tokens = []
        async for token in stream_tokens_async(inputs, processor, model):
            tokens.append(token)
        final_output = "".join(tokens)
        print(final_output)

def main():
    parser = argparse.ArgumentParser(
        description="atai-gemma3-tool: Generate text from an image using the Gemma 3 model."
    )
    parser.add_argument("image_path", help="Path to your local image file")
    parser.add_argument(
        "--prompt",
        type=str,
        default="Describe this image in detail.",
        help="Optional prompt to use for generation"
    )
    parser.add_argument(
        "--no-stream",
        action="store_false",
        dest="stream",
        help="Disable streaming output (collect and print complete text at the end)"
    )
    args = parser.parse_args()
    asyncio.run(generate_text_from_image_async(args.image_path, args.prompt, args.stream))

if __name__ == "__main__":
    main()
