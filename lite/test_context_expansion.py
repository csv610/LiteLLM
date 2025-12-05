#!/usr/bin/env python
import json
import os
from lite_chat import ChatSession

# Clean up any existing test session file
test_session_file = "test_chat_session.json"
if os.path.exists(test_session_file):
    os.remove(test_session_file)

# Create a new session
session = ChatSession(
    model="gemini/gemini-2.5-flash",
    max_tokens=10000,
    session_file=test_session_file,
)

print("=" * 80)
print("Testing Context Expansion Feature")
print("=" * 80)

# Test 1: First question (should not be expanded)
print("\n[Test 1] First Question: 'How far is the moon from earth?'")
print("-" * 80)
response1 = session.ask("How far is the moon from earth?")
print(f"Response: {response1}\n")

# Check what was stored
print("Stored message:")
print(json.dumps(session.messages[-1], indent=2))

# Test 2: Follow-up question (should be expanded with context)
print("\n[Test 2] Follow-up Question: 'Why are there dark spots on it?'")
print("-" * 80)
print("User input: 'Why are there dark spots on it?'")
print("Expected expansion: Should include 'moon' to make it complete")
response2 = session.ask("Why are there dark spots on it?")
print(f"Response: {response2}\n")

# Check what was stored
print("Stored message (should be expanded):")
print(json.dumps(session.messages[-2], indent=2))  # The user message

# Test 3: Another follow-up
print("\n[Test 3] Another Follow-up: 'How many are there?'")
print("-" * 80)
print("User input: 'How many are there?'")
print("Expected expansion: Should include context about dark spots on the moon")
response3 = session.ask("How many are there?")
print(f"Response: {response3}\n")

# Check what was stored
print("Stored message (should be expanded):")
print(json.dumps(session.messages[-2], indent=2))

# Save session
session.save()

print("\n" + "=" * 80)
print("Full Conversation History:")
print("=" * 80)
for i, msg in enumerate(session.messages):
    print(f"\n[{i}] {msg['role'].upper()}")
    print(f"    {msg['content'][:100]}..." if len(msg['content']) > 100 else f"    {msg['content']}")

print("\n" + "=" * 80)
print("Session saved to:", test_session_file)
with open(test_session_file, 'r') as f:
    data = json.load(f)
    print(f"Total messages in file: {len(data)}")
print("=" * 80)
