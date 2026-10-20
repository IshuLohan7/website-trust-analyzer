# 🛡️ Smart Website Trust Analyzer

## About the Project

Smart Website Trust Analyzer is an AI/ML-powered web application that analyzes website URLs and predicts whether they may be phishing or potentially legitimate. It aims to help users make more informed decisions before trusting a website.

## Features

- AI/ML-based phishing URL prediction

- Decision Tree classification model

- URL analysis using URL length, HTTPS usage, presence of the @ symbol, and number of subdomains

- TinyFish API integration to retrieve additional information from eligible HTTPS websites

- Streamlit-based interactive user interface

- Separate modes for Website Users and Website Owners

## Technologies Used

- Python

- Streamlit

- Pandas

- Scikit-learn

- Requests

- TinyFish API

## How It Works

- The user enters a website URL.

- The application extracts selected URL features.

- The trained Decision Tree model predicts whether the URL may be phishing or potentially legitimate.

- For eligible HTTPS URLs classified as potentially legitimate, TinyFish retrieves additional website information.

- The application displays the prediction and any available retrieved information.

## How to Run Locally

- Clone or download this repository.

- Install the required dependencies:

  pip install -r requirements.txt

- Ensure phishing_model.pkl is in the same folder as app.py.

- To enable TinyFish, configure the TINYFISH_API_KEY environment variable with your API key.

- Run the application:

  streamlit run app.py

## Disclaimer

 This project is a prototype developed for educational and hackathon purposes. Model predictions are not a guarantee of website safety. TinyFish retrieves additional website information but does not independently certify that a website is safe.
