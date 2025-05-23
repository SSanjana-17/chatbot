from flask import Flask, render_template, request, jsonify
import pandas as pd
from rapidfuzz import process  # ✅ Add this line

app = Flask(__name__)

# ✅ Load your dataset (with safe encoding)
faq_df = pd.read_csv('full_faq_dataset_with_categories.csv', encoding='ISO-8859-1')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '').strip().lower()

    # ✅ Use fuzzy matching to find the best matching question
    best_match = process.extractOne(user_message, faq_df['question'], score_cutoff=70)

    if best_match:
        matched_question = best_match[0]
        answer_row = faq_df[faq_df['question'] == matched_question]
        answer = answer_row.iloc[0]['answer']
    else:
        answer = "Sorry, I couldn't find an answer for that. Try rephrasing your question."

    return jsonify({'reply': answer})

if __name__ == '__main__':
    app.run(debug=True)
