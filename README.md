# ChatBot

## Name

Streamlit Bedrock Chat application

## Description

The application will first ask the user to enter a youtube video url.
The bot will summarize the transcript in the youtube video.
Then the user can ask further questions about the transcript in the video.
The bot will answer the questions.

## Installation

Steps to install the application

1. Clone the repo
   ```sh
   git clone git@gitlab.com:subinvs/bedrock-calude3-chatbot.git
   ```
2. Move to root directory
   ```sh
   cd chatbot
   ```
3. Install packages
   ```sh
   pip install -r reuirements.txt
   ```
4. Create .streamlit folder in the root
5. Move to .streamlit directory
   ```sh
   cd .streamlit
   ```
6. Create secrets.toml file and add AWS credentials in the file
   ```sh
   ACCESS_KEY=<Access key>
   SECRET_KEY=<Secret access key>
   ```
7. From root folder run the following command to run the application in browser
   ```sh
   streamlit run app.py
   ```
