from flask import Flask, render_template, request
import pandas as pd
from transformers import pipeline

app = Flask(__name__)

class TabularQA:
    def __init__(self, data_source:str, device='cpu') -> None:
        self.df = pd.read_csv(data_source)
        self.df = self.df.astype(str)
        self.tqa = pipeline(
                        task="table-question-answering",
                        model="google/tapas-large-finetuned-wtq",
                        device=device)
    
    def get_answer(self, query:str):
        response = self.tqa(table=self.df, query=query)
        return response["answer"]

tqa = None

@app.route('/', methods=['GET', 'POST'])
def home():
    global tqa
    if request.method == 'POST':
        question = request.form['question']
        answer = tqa.get_answer(question)
        return render_template('index.html', answer=answer)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    tqa = TabularQA(data_source='database.csv')
    app.run(debug=True)