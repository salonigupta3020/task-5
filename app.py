from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import openai

# Set your OpenAI API key (Ensure to keep this key private!)
openai.api_key = "sk-XlSa-ztuhco0JuKs4k2DExotBbbCcKTgYfPthX7tp7T3BlbkFJUvatZ9jQmhqyY-OCrId5urrpvWlXOCyvrDHovwSlgA"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')
    image_file = request.files.get('image')

    if image_file and image_file.filename != '':
        image_response = handle_image_input(image_file)
        return render_template('index.html', response=image_response)

    if user_input:
        text_response = handle_text_input(user_input)
        return render_template('index.html', response=text_response)

    return redirect(url_for('home'))

def handle_image_input(image_file):
    try:
        img = Image.open(image_file)
        img.show()  # Display the image for debugging
        return "Image processed successfully."
    except Exception as e:
        print(f"Error processing image: {e}")
        return "Error processing the uploaded image."

def handle_text_input(user_input):
    try:
        print(f"Sending request with input: {user_input}")  # Log input
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        print(f"Received response: {response}")  # Log response
        return response.choices[0].message['content']
    except openai.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "Sorry, there was an issue connecting to the OpenAI API."
    except Exception as e:
        print(f"General Error: {e}")
        return f"Sorry, an unexpected error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
