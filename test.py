import openai
import gradio as gr


#if you have OpenAI API key as a string, enable the below
openai.api_key = "xxxxx"

bot_name = "Chatbot"
user_name = "User"
background = "User is talking to Chatbot. Chatbot is helpful, creative, \
and very friendly and knows everything. Chatbot is created by Group3."


def ask(question, chat_log=None):
    prompt_text = f'{chat_log} {user_name}: {question} {bot_name}: '
    response = openai.Completion.create(
      engine='text-babbage-001',
      prompt=prompt_text,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n", "Chatbot:", "User:"],
    )
    story = response['choices'][0]['text']
    return str(story)


# Function that clones the GPT-3 model for conversation

def chatgpt_clone(input, history):
    log_list = history or []    # Initialize the chat history if it is None
    s = list(sum(log_list, ()))
    
    chat_log = background + (' '.join(s))   # Combine the backgorund info with the chat history
    answer = ask(input, chat_log)   # Send the input and chat history to the GPT-3 model and get the response  

    # Add the current input and response to the chat history
    user_log = f"{user_name}: {input}"
    bot_log = f"{bot_name}: {answer}"
    log_list.append((user_log, bot_log))

    return log_list, log_list   # Return the updated chat history 




# Define a Gradio Block to create the chatbot interface
block = gr.Blocks()

# Add a Markdown element to display the chatbot header
with block:
    gr.Markdown("""<h1><center>Our new ChatBot using GPT-3</center></h1>
    """)
    # Create a Gradio Chatbot element for the chat interface
    chatbot = gr.Chatbot()
    # Create a Gradio Textbox element for the user input
    message = gr.Textbox(placeholder='Type your messages!!!')
    # Create a Gradio State element to store the chat history
    state = gr.State()
    # Create a Gradio Button element to submit the user input
    submit = gr.Button("SEND")
    # Define the function to be called when the submit button is clicked, passing in the chatgpt_clone function and the input and state elements
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])


# Launch the Gradio Block in debug mode
block.launch(debug=True)
