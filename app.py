import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        inputPhrase = request.form["input"]
        response = openai.Completion.create(
                                            model="text-davinci-002",
                                            prompt=generate_prompt(inputPhrase),
                                            max_tokens=50,
                                            temperature=0.35,
                                            stop="Input"
                                            )
        print(response)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(input):
    return """Convert the input into language which is much more kind and professional.

        Input: can't make it tonight
        Output: Hey! Sorry about this but I have to cancel for tonight. I hope you understand.
        
        Input: i'm quittin
        Output: Hello, I am sad to announce but I must put in my two weeks. It's been a real joy to work with all of you! Thank you so much for the opportunity
        
        Input: i want this job
        Output: I would love the opportunity to work for you! I am sure I have the skillset and attitude necessary to excel at this position.
        
        Input: i'm out sick today:
        Output: Hey, I'm sorry for the short notice but I am feeling really sick today and won't be able to come into work.
        
        Input:{}
        Output:""".format(input)
