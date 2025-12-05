import pytest
from lite.config import ChatConfig
from lite.lite_chat import LiteChat

def test_history_trimming_pairs():
    """Verify that conversation history is trimmed in pairs, removing the oldest."""
    # max_history is 4, so it should hold 2 pairs.
    chat_config = ChatConfig(max_history=4)
    client = LiteChat(chat_config=chat_config)

    # Add 3 pairs (6 messages)
    for i in range(3):
        client.add_message_to_history("user", f"User message {i+1}")
        client.add_message_to_history("assistant", f"Assistant message {i+1}")

    history = client.get_conversation_history()

    # 1. Check if history length is now equal to max_history
    assert len(history) == 4, f"History length should be 4, but is {len(history)}"

    # 2. Check if the OLDEST pair has been removed.
    # The first message should now be "User message 2"
    oldest_remaining_message = history[0]
    assert oldest_remaining_message["role"] == "user"
    assert oldest_remaining_message["content"] == "User message 2"

    # 3. Check if the newest messages are still there.
    newest_message = history[-1]
    assert newest_message["role"] == "assistant"
    assert newest_message["content"] == "Assistant message 3"
    
    print("\nTest 'test_history_trimming_pairs' passed.")

def test_odd_max_history_is_decremented():
    """Verify that an odd max_history value is decremented by 1."""
    chat_config = ChatConfig(max_history=5)
    client = LiteChat(chat_config=chat_config)

    # The constructor should have decremented max_history to 4.
    assert client.max_history == 4, f"max_history should be 4, but is {client.max_history}"
    
    print("\nTest 'test_odd_max_history_is_decremented' passed.")

def test_history_trimming_with_zero_max_history():
    """Verify that history remains empty if max_history is 0."""
    chat_config = ChatConfig(max_history=0)
    client = LiteChat(chat_config=chat_config)

    client.add_message_to_history("user", "User message 1")
    client.add_message_to_history("assistant", "Assistant message 1")

    history = client.get_conversation_history()

    assert len(history) == 0, f"History should be empty, but is {len(history)}"

    print("\nTest 'test_history_trimming_with_zero_max_history' passed.")

def test_history_even_after_complete_pairs():
    """Verify that conversation history length is even after adding complete user-assistant pairs."""
    chat_config = ChatConfig(max_history=6)
    client = LiteChat(chat_config=chat_config)

    # Scenario 1: Add one pair
    client.add_message_to_history("user", "Q1")
    client.add_message_to_history("assistant", "A1")
    assert len(client.get_conversation_history()) % 2 == 0, "History should be even after 1 pair"
    assert len(client.get_conversation_history()) == 2

    # Scenario 2: Add second pair
    client.add_message_to_history("user", "Q2")
    client.add_message_to_history("assistant", "A2")
    assert len(client.get_conversation_history()) % 2 == 0, "History should be even after 2 pairs"
    assert len(client.get_conversation_history()) == 4

    # Scenario 3: Add third pair
    client.add_message_to_history("user", "Q3")
    client.add_message_to_history("assistant", "A3")
    assert len(client.get_conversation_history()) % 2 == 0, "History should be even after 3 pairs"
    assert len(client.get_conversation_history()) == 6

    # Scenario 4: Add fourth pair (should trigger trimming to maintain max_history=6)
    client.add_message_to_history("user", "Q4")
    client.add_message_to_history("assistant", "A4")
    assert len(client.get_conversation_history()) % 2 == 0, "History should be even after 4th pair with trimming"
    assert len(client.get_conversation_history()) == 6, "History should be trimmed to max_history=6"

    print("\nTest 'test_history_even_after_complete_pairs' passed.")

def test_history_never_exceeds_max_and_even_after_complete_pairs():
    """Verify history never exceeds max_history and is even after complete pairs."""
    chat_config = ChatConfig(max_history=8)
    client = LiteChat(chat_config=chat_config)

    # Add 10 pairs (20 messages) when max_history is 8
    for i in range(10):
        client.add_message_to_history("user", f"User message {i+1}")
        client.add_message_to_history("assistant", f"Assistant message {i+1}")

        history = client.get_conversation_history()
        assert len(history) % 2 == 0, f"History should be even after pair {i+1}"
        assert len(history) <= 8, f"History exceeds max_history: {len(history)} > 8"

    # Final check
    history = client.get_conversation_history()
    assert len(history) == 8, f"Final history should be 8, but is {len(history)}"
    assert len(history) % 2 == 0, "Final history should be even"

    # Verify the oldest messages were removed (should start with User message 7 after adding 10 pairs)
    # With max_history=8 and 8 messages kept, we retain messages 7-10 (4 pairs)
    assert history[0]["content"] == "User message 7", "Oldest messages should be removed"

    print("\nTest 'test_history_never_exceeds_max_and_even_after_complete_pairs' passed.")

def test_alternating_message_roles_pairs():
    """Verify history is even after adding complete alternating pairs."""
    chat_config = ChatConfig(max_history=10)
    client = LiteChat(chat_config=chat_config)

    # Add alternating pairs: (user, assistant) repeated
    for i in range(8):
        client.add_message_to_history("user", f"User {i+1}")
        client.add_message_to_history("assistant", f"Assistant {i+1}")
        history = client.get_conversation_history()
        assert len(history) % 2 == 0, f"History should be even after pair {i+1}"
        assert len(history) <= 10, f"History exceeds max_history after pair {i+1}"

    print("\nTest 'test_alternating_message_roles_pairs' passed.")

def test_history_structure_integrity():
    """Verify that after trimming, history maintains valid user-assistant pairs."""
    chat_config = ChatConfig(max_history=4)
    client = LiteChat(chat_config=chat_config)

    # Add 3 pairs
    pairs = [("Q1", "A1"), ("Q2", "A2"), ("Q3", "A3")]
    for user_msg, assistant_msg in pairs:
        client.add_message_to_history("user", user_msg)
        client.add_message_to_history("assistant", assistant_msg)

    # At this point we have 6 messages, should trim to 4
    history = client.get_conversation_history()
    assert len(history) == 4, f"History should be 4 after trimming, got {len(history)}"

    # Verify structure: should be [user, assistant, user, assistant]
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"
    assert history[2]["role"] == "user"
    assert history[3]["role"] == "assistant"

    # Verify content: should have Q2, A2, Q3, A3
    assert history[0]["content"] == "Q2"
    assert history[1]["content"] == "A2"
    assert history[2]["content"] == "Q3"
    assert history[3]["content"] == "A3"

    print("\nTest 'test_history_structure_integrity' passed.")
