import os
import openai
import gradio as gr


#if you have OpenAI API key as a string, enable the below
openai.api_key = "api-key"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "you are a chatbot that know everything and very clever. You are also helpful, creative, clever, and very friendly."

def openai_create(prompt):

    response = openai.Completion.create(
    model="text-ada-001",
    prompt=prompt,
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
    )

    return response.choices[0].text


# Function that clones the GPT-3 model for conversation

def chatgpt_clone(input, history):
    history = history or []      # Initialize the chat history if it is None
    s = list(sum(history, ()))
    # Combine the current input with the chat history
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)       # Send the input and chat history to the GPT-3 model and get the response
    history.append((input, output))   # Add the current input and response to the chat history

    return history, history            # Return the updated chat history



# Define a Gradio Block to create the chatbot interface
block = gr.Blocks()

# Add a Markdown element to display the chatbot header
with block:
    gr.Markdown("""<h1><center>Our new ChatBot using GPT-3</center></h1>
    """)
    # Create a Gradio Chatbot element for the chat interface
    chatbot = gr.Chatbot()
    # Create a Gradio Textbox element for the user input
    message = gr.Textbox(placeholder=prompt)
    # Create a Gradio State element to store the chat history
    state = gr.State()
    # Create a Gradio Button element to submit the user input
    submit = gr.Button("SEND")
    # Define the function to be called when the submit button is clicked, passing in the chatgpt_clone function and the input and state elements
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# Launch the Gradio Block in debug mode
block.launch(debug=True)