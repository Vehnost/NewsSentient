"""
Test client for Sentient News Agent.
Demonstrates how to interact with the agent API.
"""
import requests
import json
import time
from typing import Optional


class SentientNewsClient:
    """Client for interacting with Sentient News Agent."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_capabilities(self):
        """Get agent capabilities."""
        response = self.session.get(f"{self.base_url}/capabilities")
        return response.json()
    
    def chat(self, message: str, stream: bool = False):
        """
        Chat with the agent.
        
        Args:
            message: User message
            stream: Enable streaming (default: False)
        """
        if stream:
            return self._chat_stream(message)
        else:
            return self._chat_non_stream(message)
    
    def _chat_non_stream(self, message: str):
        """Non-streaming chat."""
        response = self.session.post(
            f"{self.base_url}/v1/chat",
            json={"message": message, "stream": False}
        )
        return response.json()
    
    def _chat_stream(self, message: str):
        """Streaming chat with SSE."""
        print(f"\n🤖 Sending: {message}")
        print("📡 Streaming response...\n")
        
        response = self.session.post(
            f"{self.base_url}/v1/chat/stream",
            json={"message": message, "stream": True},
            stream=True
        )
        
        events = []
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line = line.decode('utf-8')
            if line.startswith('data: '):
                try:
                    event_data = json.loads(line[6:])
                    events.append(event_data)
                    
                    event_type = event_data.get('type')
                    
                    if event_type == 'thinking':
                        thinking = event_data.get('thinking', {})
                        print(f"💭 {thinking.get('type', '').upper()}: {thinking.get('content', '')}")
                    
                    elif event_type == 'content':
                        content = event_data.get('content', '')
                        print(content, end='', flush=True)
                    
                    elif event_type == 'data':
                        data = event_data.get('data', {})
                        print(f"\n📊 Data: {data.get('total_results', 0)} articles")
                    
                    elif event_type == 'complete':
                        print("\n\n✅ Complete!")
                    
                    elif event_type == 'error':
                        print(f"\n❌ Error: {event_data.get('content', 'Unknown error')}")
                
                except json.JSONDecodeError as e:
                    print(f"Error parsing event: {e}")
        
        return events
    
    def query_news(
        self,
        keywords: Optional[list] = None,
        categories: Optional[list] = None,
        max_results: int = 10
    ):
        """Direct news query."""
        response = self.session.post(
            f"{self.base_url}/v1/query/news",
            json={
                "keywords": keywords or [],
                "categories": categories or ["general"],
                "max_results": max_results
            }
        )
        return response.json()
    
    def get_categories(self):
        """Get available categories."""
        response = self.session.get(f"{self.base_url}/v1/categories")
        return response.json()


def demo_capabilities():
    """Demo: Get agent capabilities."""
    print("\n" + "="*60)
    print("📋 DEMO: Agent Capabilities")
    print("="*60)
    
    client = SentientNewsClient()
    capabilities = client.get_capabilities()
    
    print(f"\n🤖 Agent: {capabilities['name']}")
    print(f"📝 Description: {capabilities['description']}")
    print(f"🔢 Version: {capabilities['version']}")
    print(f"\n✨ Capabilities:")
    for cap in capabilities['capabilities']:
        print(f"  - {cap}")
    print(f"\n🌐 Languages: {', '.join(capabilities['supported_languages'])}")
    print(f"📊 Streaming: {'✅ Yes' if capabilities['streaming_supported'] else '❌ No'}")


def demo_streaming_chat():
    """Demo: Streaming chat."""
    print("\n" + "="*60)
    print("💬 DEMO: Streaming Chat")
    print("="*60)
    
    client = SentientNewsClient()
    
    # Test different queries
    queries = [
        "Show me latest AI news",
        "What's happening in crypto?",
        "Latest technology news",
    ]
    
    for query in queries:
        client.chat(query, stream=True)
        time.sleep(1)


def demo_non_streaming_chat():
    """Demo: Non-streaming chat."""
    print("\n" + "="*60)
    print("💬 DEMO: Non-Streaming Chat")
    print("="*60)
    
    client = SentientNewsClient()
    
    result = client.chat("Latest finance news", stream=False)
    print(f"\n🤖 Response:")
    print(result['message'])


def demo_direct_query():
    """Demo: Direct news query."""
    print("\n" + "="*60)
    print("🔍 DEMO: Direct News Query")
    print("="*60)
    
    client = SentientNewsClient()
    
    result = client.query_news(
        keywords=["bitcoin", "ethereum"],
        categories=["crypto"],
        max_results=5
    )
    
    print(f"\n📰 Found {result['total']} articles:")
    for i, article in enumerate(result['articles'], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   URL: {article['url']}")


def demo_categories():
    """Demo: Get categories."""
    print("\n" + "="*60)
    print("🏷️ DEMO: Available Categories")
    print("="*60)
    
    client = SentientNewsClient()
    
    result = client.get_categories()
    print(f"\n📂 Categories: {', '.join(result['categories'])}")


def main():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 Sentient News Agent - Test Client")
    print("="*60)
    
    try:
        # Check if server is running
        client = SentientNewsClient()
        health = client.session.get(f"{client.base_url}/health")
        print("\n✅ Server is running!")
        
        # Run demos
        demo_capabilities()
        demo_categories()
        demo_streaming_chat()
        # demo_non_streaming_chat()  # Uncomment to test
        # demo_direct_query()  # Uncomment to test
        
        print("\n" + "="*60)
        print("✅ All demos completed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server!")
        print("Make sure the server is running:")
        print("  python main.py")
        print("\nOr:")
        print("  uvicorn main:app --reload")


if __name__ == "__main__":
    main()
