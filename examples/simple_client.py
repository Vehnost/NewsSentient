"""
Simple example of using Sentient News Agent.
"""
import requests
import json


def simple_query():
    """Simple non-streaming query."""
    print("📰 Simple News Query\n")
    
    response = requests.post(
        "http://localhost:8000/v1/chat",
        json={
            "message": "Show me latest technology news",
            "stream": False
        }
    )
    
    result = response.json()
    print(result['message'])


def streaming_query():
    """Streaming query with real-time updates."""
    print("\n📡 Streaming News Query\n")
    
    with requests.post(
        "http://localhost:8000/v1/chat/stream",
        json={
            "message": "Latest AI and crypto news",
            "stream": True
        },
        stream=True
    ) as response:
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line = line.decode('utf-8')
            if line.startswith('data: '):
                event = json.loads(line[6:])
                
                if event['type'] == 'thinking':
                    thinking = event.get('thinking', {})
                    print(f"💭 {thinking.get('content', '')}")
                
                elif event['type'] == 'content':
                    print(event.get('content', ''), end='', flush=True)
                
                elif event['type'] == 'complete':
                    print("\n✅ Done!")


def direct_query():
    """Direct news query without chat."""
    print("\n🔍 Direct News Query\n")
    
    response = requests.post(
        "http://localhost:8000/v1/query/news",
        json={
            "keywords": ["bitcoin", "ethereum"],
            "categories": ["crypto"],
            "max_results": 3
        }
    )
    
    result = response.json()
    
    print(f"Found {result['total']} articles:\n")
    for article in result['articles']:
        print(f"• {article['title']}")
        print(f"  {article['source']} - {article['url']}\n")


if __name__ == "__main__":
    print("="*60)
    print("Sentient News Agent - Simple Examples")
    print("="*60)
    
    try:
        # Test connection
        response = requests.get("http://localhost:8000/health")
        print("✅ Server is running!\n")
        
        # Run examples
        simple_query()
        streaming_query()
        direct_query()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Server is not running!")
        print("\nStart the server with:")
        print("  python main.py")
