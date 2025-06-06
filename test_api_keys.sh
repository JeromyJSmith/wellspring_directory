#!/bin/zsh

# Store API keys securely as environment variables
export OPENROUTER_API_KEY='your_openrouter_api_key'
export SERPER_API_KEY='your_serper_api_key'
export DID_API_KEY='your_did_api_key'
export LLAMA_APP_KEY='your_llama_app_key'
export EXA_API_KEY='your_exa_api_key'
export PERPLEXITY_API_KEY='your_perplexity_api_key'

echo "🔐 API Key Testing Script"
echo "======================================"

# Test OpenRouter API Key
echo "Testing OpenRouter API key..."
OPENROUTER_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -d '{"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]}')

if [[ "$OPENROUTER_RESULT" == "200" || "$OPENROUTER_RESULT" == "201" ]]; then
  echo "✅ OpenRouter API key is valid (HTTP $OPENROUTER_RESULT)"
else
  echo "❌ OpenRouter API key may be invalid (HTTP $OPENROUTER_RESULT)"
fi
echo ""

# Test Serper API Key
echo "Testing Serper API key..."
SERPER_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "test"}')

if [[ "$SERPER_RESULT" == "200" ]]; then
  echo "✅ Serper API key is valid (HTTP $SERPER_RESULT)"
else
  echo "❌ Serper API key may be invalid (HTTP $SERPER_RESULT)"
fi
echo ""

# Test D-ID API Key
echo "Testing D-ID API key..."
DID_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X GET "https://api.d-id.com/talks" \
  -H "Authorization: Basic $DID_API_KEY")

if [[ "$DID_RESULT" == "200" ]]; then
  echo "✅ D-ID API key is valid (HTTP $DID_RESULT)"
else
  echo "❌ D-ID API key may be invalid (HTTP $DID_RESULT)"
fi
echo ""

# Test Llama App API Key (OpenAI format)
echo "Testing Llama App API key..."
LLAMA_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.openai.com/v1/chat/completions" \
  -H "Authorization: Bearer $LLAMA_APP_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hello"}]}')

if [[ "$LLAMA_RESULT" == "200" ]]; then
  echo "✅ Llama App API key is valid (HTTP $LLAMA_RESULT)"
else
  echo "❌ Llama App API key may be invalid (HTTP $LLAMA_RESULT)"
fi
echo ""

# Test EXA API Key
echo "Testing EXA API key..."
EXA_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.exa.ai/search" \
  -H "x-api-key: $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "numResults": 1}')

if [[ "$EXA_RESULT" == "200" ]]; then
  echo "✅ EXA API key is valid (HTTP $EXA_RESULT)"
else
  echo "❌ EXA API key may be invalid (HTTP $EXA_RESULT)"
fi
echo ""

# Test Perplexity API Key
echo "Testing Perplexity API key..."
PERPLEXITY_RESULT=$(curl -s -o /dev/null -w "%{http_code}" \
  -X POST "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sonar-small-online", "messages": [{"role": "user", "content": "Hello"}]}')

if [[ "$PERPLEXITY_RESULT" == "200" ]]; then
  echo "✅ Perplexity API key is valid (HTTP $PERPLEXITY_RESULT)"
else
  echo "❌ Perplexity API key may be invalid (HTTP $PERPLEXITY_RESULT)"
fi
echo ""

echo "🔒 Testing complete! Cleaning up..."

# Unset all environment variables to avoid leaking keys
unset OPENROUTER_API_KEY
unset SERPER_API_KEY
unset DID_API_KEY
unset LLAMA_APP_KEY
unset EXA_API_KEY
unset PERPLEXITY_API_KEY

echo "✨ All API keys have been removed from environment variables"
