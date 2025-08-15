import os

if "OPENAI_API_KEY" in os.environ:
    print("✅ API key is set.")
else:
    print("❌ API key is NOT set.")