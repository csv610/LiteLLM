#!/usr/bin/env python3
"""Add new myths to appropriate sections in myths.json."""

import json

# New myths categorized by topic
NEW_MYTHS = {
    "Food & Nutrition": [
        "Microwaving your food is bad for you because it kills nutrients.",
        "It is safe to eat dropped food if it is picked up within 5 seconds.",
        "Eating late at night causes weight gain.",
        "Eating fish makes you smarter.",
        "Eggs are bad for your cholesterol.",
        "Carbs are bad for weight loss.",
        "Eating nuts causes weight gain.",
        "Eating before exercising causes stomach cramps.",
        "Eating breakfast is essential for metabolism.",
        "Skipping meals slows your metabolism.",
        "Monosodium glutamate (MSG) is toxic to humans.",
        "Eating fat makes you fat.",
    ],
    "General Health & Wellness": [
        "Public toilet seats carry infections and diseases.",
        "Getting an X-ray will give you cancer.",
        "You need to drink 8 glasses of water per day.",
        "Cold weather causes colds.",
        "Vitamin C prevents common colds.",
        "Fever is always dangerous and should be brought down immediately.",
        "Drinking coffee stunts your growth.",
        "Starve a fever, feed a cold.",
        "Energy drinks are safer than coffee.",
        "Antibiotics can treat viral infections.",
        "You lose consciousness immediately after being knocked out hard.",
        "Drinking alcohol kills brain cells permanently.",
        "Detox diets are necessary for good health.",
        "Natural supplements are always safe.",
        "Red wine is good for your heart.",
        "You must wait 30 minutes after eating before swimming.",
        "Fluoride in water causes cancer.",
        "You lose most body heat through your head.",
        "Drinking milk helps broken bones heal faster.",
        "Gum stays in your stomach for seven years if swallowed.",
        "Using deodorant causes breast cancer.",
        "Alcohol kills brain cells that cannot be replaced.",
        "A person bitten by a snake in water cannot be saved.",
        "You need 10,000 steps a day to be healthy.",
        "Sleeping with wet hair causes pneumonia.",
        "Artificial sweeteners are worse than sugar.",
        "You need to stretch before every workout.",
        "Cold hands indicate poor circulation.",
        "You can catch a cold from being cold.",
        "Hot drinks warm you up when you're cold.",
        "Sleeping with socks on reduces body temperature too much.",
        "Antibiotics should be taken until symptoms disappear.",
        "Fever indicates a serious infection.",
        "X-rays are extremely dangerous.",
    ],
    "Skin Health": [
        "You should always peel fruits and veggies.",
        "Shaving makes hair grow back thicker.",
        "You need sunscreen indoors to prevent skin cancer.",
        "Cutting hair makes it grow back fuller and thicker.",
        "Chocolate causes acne.",
    ],
    "Eye Health": [
        "Carrots significantly improve your eyesight.",
        "Sitting too close to the TV damages your eyes.",
        "Reading in dim light damages eyesight permanently.",
        "Eating carrots improves night vision significantly.",
    ],
    "First Aid & Treatment": [
        "Apply ice if you burn yourself.",
        "You should pee on a jellyfish sting.",
        "Applying butter to burns helps them heal.",
        "Tilting your head back stops nosebleeds.",
        "Hydrogen peroxide is the best wound cleaner.",
        "You should chew aspirin during a heart attack.",
    ],
    "Brain & Cognition": [
        "We only use 10% of our brains.",
        "You cannot teach an old dog new tricks due to brain plasticity.",
    ],
    "All about arthritis": [  # Existing section
        "Cracking joints leads to arthritis.",
        "Cracking your knuckles leads to arthritis.",
    ],
    "Exercise & Fitness": [
        "You shouldn't swim immediately after eating.",
        "Lifting weights makes women bulky.",
    ],
    "Technology & Radiation": [
        "Microwave radiation is dangerous and causes cancer.",
        "Using your phone before bed prevents sleep.",
    ],
    "Sexual health": [  # Existing section
        "Hormonal birth control causes infertility.",
        "You must wash the vagina after intercourse.",
        "Daily masturbation is unhealthy.",
        "It is unnatural for females to masturbate.",
        "Anal sex makes the penis healthier.",
        "Masturbation causes hair loss or blindness.",
        "Sexual contact with animals indicates a mental disorder.",
    ],
    "Digestive Health": [  # Existing section
        "Eating spicy food causes ulcers.",
        "Ginger can cure nausea and vomiting.",
    ],
    "All about aging": [  # Existing section
        "Eating garlic keeps mosquitoes away.",
    ],
}


def main():
    """Main function to add new myths to myths.json."""
    # Load existing myths
    with open('myths.json', 'r') as f:
        data = json.load(f)

    existing_myths = data['myths']

    # Create a dictionary of existing topics for easy lookup
    topic_dict = {item['topic']: item['myths'] for item in existing_myths}

    # Add new myths to appropriate topics
    for topic, new_myths in NEW_MYTHS.items():
        if topic in topic_dict:
            # Topic exists, add to it
            topic_dict[topic].extend(new_myths)
        else:
            # Create new topic
            topic_dict[topic] = new_myths

    # Rebuild the myths list
    updated_myths = [
        {"topic": topic, "myths": myths}
        for topic, myths in topic_dict.items()
    ]

    # Save updated data
    output = {"myths": updated_myths}
    with open('myths.json', 'w') as f:
        json.dump(output, f, indent=2)

    total_new = sum(len(myths) for myths in NEW_MYTHS.values())
    total_all = sum(len(item['myths']) for item in updated_myths)

    print(f"✓ Added {total_new} new myths")
    print(f"✓ Total myths in file: {total_all}")
    print(f"✓ Total topics: {len(updated_myths)}")


if __name__ == "__main__":
    main()
