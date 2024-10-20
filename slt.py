import streamlit as st
import csv
import re
import pandas as pd

# Function to validate email
def validate_email(email):
    """Validate the email address"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# Function to submit form data
def submit_form(description, email):
    """Submit the form data to the CSV file"""
    data = {'Description': [description], 'Email': [email]}
    df = pd.DataFrame(data)

    # Try to append to the CSV if it exists, otherwise create a new one
    try:
        existing_df = pd.read_csv('user_requests.csv')
        combined_df = pd.concat([existing_df, df])
        combined_df.to_csv('user_requests.csv', index=False)
    except FileNotFoundError:
        df.to_csv('user_requests.csv', index=False)

# Form to ask a question
def ask_me_a_question_form():
    """The 'Ask me a question' form"""
    st.subheader("Ask me a question:")
    description = st.text_area(label="A description of why you're reaching out, including any questions you have")
    email = st.text_input(label="What email can I reach you at?")

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not validate_email(email):
            st.error("Invalid email address")
        else:
            submit_form(description, email)
            st.success("Thank you for your submission!")

# Function to display user requests from the CSV file
def view_submissions():
    """Display submitted questions"""
    st.subheader("Submitted Questions")
    
    try:
        df = pd.read_csv('user_requests.csv')
        st.dataframe(df)  # Display the data in a table format
    except FileNotFoundError:
        st.write("No submissions found yet.")

# Main function for multi-page navigation
def main():
    st.title("My Small Business")
    
    # Create a sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["Ask a Question", "View Submissions"])

    if page == "Ask a Question":
        st.subheader("Description of my small business", divider="violet")
        with st.form("Ask me a question:", clear_on_submit=True):
            ask_me_a_question_form()
    
    elif page == "View Submissions":
        view_submissions()

if __name__ == "__main__":
    main()
