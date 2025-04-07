## Outdated version (Old project)

This app is designed to facilitate interaction with multiple AI assistants using the OpenAI API. Users can add, manage, and remove AI assistants, and send prompts to receive generated responses from each assistant. It's main goal is to test multiple system prompts at once.

## Prerequisites

- **Python 3.8+**
- An **OpenAI API key** with the `OPENAI_API_KEY` environment variable set.
- Dependencies listed in the **`requirements.txt`** file.

## Installation
**Clone the repository**:

    
    git clone https://github.com/Nikodem5/prompt_testing
    cd prompt_testing
    

**Install the required Python packages:**

    
    pip install -r requirements.txt
    

**Set the `OPENAI_API_KEY` environment variable:**

    
    export OPENAI_API_KEY='your_openai_api_key'
    

**Run the app**

    
    flet run prompt_testing_v1.py
    

## App Functionality
Main Page:
  Add Assistant: Enter an assistant ID and click the "Add Assistant" button to add a new assistant. The assistant ID is appended to the assistants.txt file.
  Remove Assistant: Click the "Remove" button to remove the last assistant from the app and the assistants.txt file.
  Send Prompt: Enter a message in the text field and click the "Send" button to send the prompt to all added assistants. The responses are displayed below the prompt.
  Show Layout: Click the "Show" button to display the current layout of the page in the console for debugging purposes. (used for development)

## Response Generation
When a prompt is sent:
  The prompt is sent to each assistant.
  The app waits for each assistant to generate a response.
  Responses are displayed in a row beneath the prompt, with each assistant's name and response clearly labeled.
