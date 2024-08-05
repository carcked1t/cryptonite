import google.generativeai as genai
import streamlit as st
import pandas as pd

# Frontend: Streamlit
# LLM: Google Gemini(changed from open ai, which was used to showcase in meeting)
genai.configure(api_key="##removed the api key for github repo")

# Load riddles from a CSV file
def load_riddles(csv_file):
    riddles_df = pd.read_csv(csv_file)
    return riddles_df.to_dict('records')
riddles = load_riddles('riddles.csv')

def get_ai_response(prompt):
    response = genai.Completion.create(
        model="text-gpt-4-001",
        prompt=prompt,
        max_tokens=100
    )
    return response.result

def handle_prompt_injection(user_input):
    if "reveal riddle" in user_input.lower():
        return "\n".join([riddle["riddle"] for riddle in riddles])
    elif "reveal answer" in user_input.lower():
        return "\n".join([f"Riddle: {riddle['riddle']} - Answer: {riddle['answer']}" for riddle in riddles])
    else:
        return get_ai_response(user_input)

def main():
    st.title("AI Capture the Flag Challenge")
    
    st.write("Use prompt injection to get clues and solve the riddles.")

    if 'solved_riddles' not in st.session_state:
        st.session_state.solved_riddles = []
    if 'current_riddle' not in st.session_state:
        st.session_state.current_riddle = 0
    if 'final_key' not in st.session_state:
        st.session_state.final_key = "kinesthetic101"
    
    if st.session_state.current_riddle < len(riddles):
        riddle = riddles[st.session_state.current_riddle]
        st.write(f"Riddle {st.session_state.current_riddle + 1}: {riddle['riddle']}")
        
        user_input = st.text_input("Your answer or hint request:")
        
        if st.button("Submit"):
            if user_input.lower() == riddle['answer'].lower():
                st.session_state.solved_riddles.append(riddle['answer'])
                st.session_state.current_riddle += 1
                st.success("Correct! Moving to the next riddle.")
            else:
                response = handle_prompt_injection(user_input)
                st.write("AI Response:", response)
    else:
        user_key = st.text_input("All riddles solved! Enter the final key to complete the challenge:")
        
        if st.button("Submit Key"):
            if user_key == st.session_state.final_key:
                st.success("Congratulations! You've completed the challenge.")
            else:
                st.error("Incorrect key. Try again!")

if __name__ == "__main__":
    main()
