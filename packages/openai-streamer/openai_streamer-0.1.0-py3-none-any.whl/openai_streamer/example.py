"""
Example usage of the OpenAI Streamer package
"""
from openai_streamer.streamer import OpenAIStreamer, stream_completion

def main():
    # Example 1: Using the convenience function
    prompt = "Write a short poem about artificial intelligence."
    instructions = "You are a creative poet with a technical background."
    
    print("Example 1: Using the convenience function")
    response = stream_completion(prompt, instructions=instructions)
    
    # Example 2: Using the class
    print("\n\nExample 2: Using the class")
    streamer = OpenAIStreamer()
    prompt = "Explain quantum computing in simple terms."
    instructions = "You are a science educator explaining complex topics to beginners."
    
    response = streamer.stream_completion(prompt, instructions=instructions)

if __name__ == "__main__":
    main()
