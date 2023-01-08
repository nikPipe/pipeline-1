import random

# List of responses
responses = [
    "Hello!",
    "Hi there!",
    "How are you doing?",
    "I'm doing well, how about you?",
    "I'm sorry, I don't understand.",
]

# Function to generate a response
def generate_response(prompt):
    # Check if the user is asking to execute a script
    if 'execute script' in prompt.lower():
        # Get the script name from the prompt
        script_name = prompt.split('execute script')[-1].strip()

        # Read the script file
        with open(script_name, 'r') as f:
            script = f.read()

        # Execute the script
        exec(script)
    else:
        # Generate a random response
        return random.choice(responses)

# Main loop
while True:
    # Get user input
    prompt = input("> ")

    # Generate a response
    response = generate_response(prompt)

    # Print the response
    print(response)
