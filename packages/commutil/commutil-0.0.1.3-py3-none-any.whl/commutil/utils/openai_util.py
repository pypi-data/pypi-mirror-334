import os
import asyncio
from tqdm.asyncio import tqdm_asyncio
from openai import AsyncOpenAI, RateLimitError, APITimeoutError, APIError
import sys


class StreamingOpenAIChat:
    def __init__(
            self,
            client=None,
            base_url=None,
            api_key=None,
            model_name="gpt-3.5-turbo",
            max_tokens=128,
            temperature=1,
            top_p=1,
            max_concurrency=20,
            retry_limit=10,
            initial_retry_delay=0.5,
            timeout=30.0,
            stream_callback=None
    ):
        """
        Initialize the OpenAI Chat client for streaming completions.

        Args:
            client: Optional pre-configured OpenAI client
            base_url: API base URL
            api_key: OpenAI API key
            model_name: Model to use for completions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_concurrency: Maximum concurrent requests
            retry_limit: Maximum number of retries per request
            initial_retry_delay: Initial delay between retries (exponential backoff)
            timeout: HTTP request timeout in seconds
            stream_callback: Function to call for each chunk of streaming content
        """
        self.client = client
        if self.client is None:
            if api_key is None:
                api_key = os.environ.get("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is required.")

            if base_url is None:
                base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

        # Request parameters
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

        # Control parameters
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.retry_limit = retry_limit
        self.initial_retry_delay = initial_retry_delay

        # Stream handling
        self.stream_callback = stream_callback or self._default_stream_handler

    def _default_stream_handler(self, request_id, content, finished=False):
        """
        Default handler for streaming content.

        Args:
            request_id: Identifier for the request
            content: Content chunk from the stream
            finished: Whether this is the final call for this request
        """
        if content:
            # print(f"[{request_id}] {content}", end="", flush=True)
            print(f"{content}", end="", flush=True)
        if finished:
            # print(f"\n[{request_id}] Complete")
            print(f"\n")

    async def _request_with_retry(self, messages, request_id=None):
        """
        Execute streaming API request with retry mechanism.

        Args:
            messages: List of message objects to send
            request_id: Identifier for the request (used in logging)

        Returns:
            Dictionary with request result including accumulated content
        """
        sleep_time = self.initial_retry_delay
        errors = []

        # Use semaphore for concurrency control
        async with self.semaphore:
            for attempt in range(self.retry_limit):
                try:
                    response = await self.client.chat.completions.create(
                        messages=messages,
                        model=self.model_name,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        top_p=self.top_p,
                        stream=True  # Always stream in this class
                    )
                    full_content = await self._process_stream(response, request_id)
                    return {"success": True, "content": full_content, "id": request_id}
                except Exception as e:
                    errors.append(str(e))

                    # Adjust retry delay based on error type
                    if "rate limit" in str(e).lower():
                        sleep_time = min(30, sleep_time * 2)
                    elif "server error" in str(e).lower():
                        sleep_time = min(10, sleep_time * 1.5)
                    else:
                        sleep_time = min(20, sleep_time * 2)

                    if attempt < self.retry_limit - 1:
                        print(f"Request {request_id} failed (attempt {attempt + 1}/{self.retry_limit}): {e}")
                        await asyncio.sleep(sleep_time)
                    else:
                        print(f"Request {request_id} finally failed after {self.retry_limit} attempts")

            return {"success": False, "errors": errors, "id": request_id}

    async def _process_stream(self, response, request_id):
        """
        Process streaming response in real-time.

        Args:
            response: Streaming response from OpenAI API
            request_id: Identifier for the request

        Returns:
            Accumulated full content as string
        """
        content_parts = []
        try:
            async for chunk in response:
                try:
                    if hasattr(chunk, 'choices') and chunk.choices:
                        delta = getattr(chunk.choices[0], 'delta', None)
                        if delta and hasattr(delta, 'content') and delta.content:
                            # Process chunk in real-time
                            self.stream_callback(request_id, delta.content, finished=False)
                            # Accumulate for full response
                            content_parts.append(delta.content)
                except (AttributeError, IndexError):
                    continue

            # Signal completion of stream
            self.stream_callback(request_id, "", finished=True)
            full_content = ''.join(content_parts)
            return full_content
        except Exception as e:
            print(f"Stream processing error: {e}")
            return ''.join(content_parts) if content_parts else None

    async def dispatch_openai_requests(self, messages_list):
        """
        Dispatch multiple requests in parallel.

        Args:
            messages_list: List of message lists

        Returns:
            List of results with accumulated content
        """
        tasks = []
        for i, messages in enumerate(messages_list):
            task = self._request_with_retry(messages, request_id=i)
            tasks.append(task)

        results = await tqdm_asyncio.gather(*tasks, desc="Processing Streaming Requests")
        return results

    async def async_run(self, messages_list, custom_stream_handler=None):
        """
        Run streaming requests with optional custom handler.

        Args:
            messages_list: List of message lists
            custom_stream_handler: Optional replacement for default stream handler

        Returns:
            List of accumulated content from streams
        """
        # Optionally override stream handler for this run
        original_handler = self.stream_callback
        if custom_stream_handler:
            self.stream_callback = custom_stream_handler

        try:
            all_results = await self.dispatch_openai_requests(messages_list)

            preds = [None] * len(all_results)
            failed_requests = []

            for result in all_results:
                idx = result["id"]
                if result["success"]:
                    preds[idx] = result["content"]
                else:
                    failed_requests.append(idx)

            if failed_requests:
                print(f"Warning: {len(failed_requests)} streaming requests failed: {failed_requests}")

            return preds
        finally:
            # Restore original handler if it was temporarily replaced
            if custom_stream_handler:
                self.stream_callback = original_handler


class OpenAIChat:
    def __init__(
            self,
            client=None,
            base_url=None,
            api_key=None,
            model_name="gpt-3.5-turbo",
            max_tokens=128,
            temperature=1,
            top_p=1,
            max_concurrency=20,
            retry_limit=10,
            initial_retry_delay=0.5,
            timeout=30.0
    ):
        """
        Initialize the OpenAI Chat client for non-streaming completions.

        Args:
            client: Optional pre-configured OpenAI client
            base_url: API base URL
            api_key: OpenAI API key
            model_name: Model to use for completions
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_concurrency: Maximum concurrent requests
            retry_limit: Maximum number of retries per request
            initial_retry_delay: Initial delay between retries (exponential backoff)
            timeout: HTTP request timeout in seconds
        """
        self.client = client
        if self.client is None:
            if api_key is None:
                api_key = os.environ.get("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is required.")

            if base_url is None:
                base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

            self.client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

        # Request parameters
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p

        # Control parameters
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.retry_limit = retry_limit
        self.initial_retry_delay = initial_retry_delay

    async def _request_with_retry(self, messages, request_id=None):
        """
        Execute API request with retry mechanism.

        Args:
            messages: List of message objects to send
            request_id: Identifier for the request (used in logging)

        Returns:
            Dictionary with request result
        """
        sleep_time = self.initial_retry_delay
        errors = []

        # Use semaphore for concurrency control
        async with self.semaphore:
            for attempt in range(self.retry_limit):
                try:
                    response = await self.client.chat.completions.create(
                        messages=messages,
                        model=self.model_name,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        top_p=self.top_p,
                        stream=False
                    )
                    return {"success": True, "response": response, "id": request_id}
                except Exception as e:
                    errors.append(str(e))

                    # Adjust retry delay based on error type
                    if "rate limit" in str(e).lower():
                        sleep_time = min(30, sleep_time * 2)
                    elif "server error" in str(e).lower():
                        sleep_time = min(10, sleep_time * 1.5)
                    else:
                        sleep_time = min(20, sleep_time * 2)

                    if attempt < self.retry_limit - 1:
                        print(f"Request {request_id} failed (attempt {attempt + 1}/{self.retry_limit}): {e}")
                        await asyncio.sleep(sleep_time)
                    else:
                        print(f"Request {request_id} finally failed after {self.retry_limit} attempts")

            return {"success": False, "errors": errors, "id": request_id}

    async def dispatch_openai_requests(self, messages_list):
        """
        Dispatch multiple requests in parallel.

        Args:
            messages_list: List of message lists

        Returns:
            List of results
        """
        tasks = []
        for i, messages in enumerate(messages_list):
            task = self._request_with_retry(messages, request_id=i)
            tasks.append(task)

        results = await tqdm_asyncio.gather(*tasks, desc="Processing API Requests")
        return results

    async def async_run(self, messages_list):
        """
        Execute requests and process results.

        Args:
            messages_list: List of message lists

        Returns:
            List of completion results or None for failed requests
        """
        all_results = await self.dispatch_openai_requests(messages_list)

        preds = [None] * len(all_results)
        failed_requests = []

        for result in all_results:
            idx = result["id"]
            if result["success"]:
                preds[idx] = result["response"].choices[0].message.content
            else:
                failed_requests.append(idx)

        if failed_requests:
            print(f"Warning: {len(failed_requests)} requests failed: {failed_requests}")

        return preds


if __name__ == '__main__':
    inputs = [
        [
            {
                "role": "user",
                "content": "Hello, how are you?",
            },
            {
                "role": "user",
                "content": "I'm doing great, how about you?",
            },
        ]
        for _ in range(1)
    ]

    configs = {
        "openai_default": {},
    }

    agent = OpenAIChat(
        **configs["openai_default"]
    )
    # agent = StreamingOpenAIChat(
    #     **configs["openai_default"]
    # )

    messages_list = inputs
    print("input list", messages_list)

    results = asyncio.run(agent.async_run(messages_list=messages_list))
    print("output list", results)
