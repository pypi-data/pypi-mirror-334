"""
OpenAI Streamer module for streaming text completion using OpenAI's Responses API
"""
import sys
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenAIStreamer:
    """
    A class for generating text completion using OpenAI's Responses API with streaming
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the OpenAIStreamer
        
        Args:
            api_key (str, optional): OpenAI API key. If None, will use from environment.
        """
        self.client = OpenAI(api_key=api_key)
    
    def stream_completion(self, prompt, model="gpt-4o", instructions=None, delay=0.01):
        """
        Generate text completion using OpenAI's Responses API with streaming
        
        Args:
            prompt (str): The input text to complete
            model (str): The model to use for completion
            instructions (str, optional): System instructions for the model
            delay (float, optional): Small delay between tokens to make streaming visible
            
        Returns:
            str: The complete generated text
        """
        full_response = ""
            
        try:
            # Create a streaming completion using the Responses API
            stream = self.client.responses.create(
                model=model,
                input=prompt,
                instructions=instructions,
                stream=True  # Enable streaming
            )
            
            # Process and display the streaming response
            print("\nStreaming Response:")
            print("-" * 50)
            
            for event in stream:
                # Print the event data without a newline to simulate continuous text
                if hasattr(event, 'delta') and event.delta:
                    sys.stdout.write(event.delta)
                    sys.stdout.flush()
                    full_response += event.delta
                    time.sleep(delay)  # Small delay to make streaming visible
            
            print("\n" + "-" * 50)
            return full_response
            
        except Exception as e:
            print(f"Error during API call: {e}")
            return None

def stream_completion(prompt, model="gpt-4o", instructions=None, api_key=None):
    """
    Convenience function to generate text completion using OpenAI's Responses API with streaming
    
    Args:
        prompt (str): The input text to complete
        model (str): The model to use for completion
        instructions (str, optional): System instructions for the model
        api_key (str, optional): OpenAI API key. If None, will use from environment.
        
    Returns:
        str: The complete generated text
    """
    streamer = OpenAIStreamer(api_key=api_key)
    return streamer.stream_completion(prompt, model, instructions)
