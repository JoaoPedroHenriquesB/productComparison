import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, render_template, request

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")


@app.route("/", methods=["GET", "POST"])
def main():
    product_a = None
    product_b = None
    gemini = None

    if request.method == "POST":
        product_a = request.form.get("product_a")
        product_b = request.form.get("product_b")

        prompt = f"Compare {product_a} vs {product_b} in an EXTREMELY CONCISE format: KEY DIFFERENCES: • [3-5 words] • [3-5 words] • [3-5 words] STRENGTHS: PRODUCT_A: [2-3 short points] PRODUCT_B: [2-3 short points] RECOMMENDATION: PRODUCT_A for [specific user], PRODUCT_B for [specific user]. Keep each line very short, max 30 lines total."

        response = model.generate_content(prompt)
        gemini = response.text

    return render_template(
        "index.html", product_a=product_a, product_b=product_b, gemini=gemini
    )


if __name__ == "__main__":
    app.run(debug=True)
