import streamlit as st
import pandas as pd
import os

# File to store library data
DATA_FILE = "library_data.csv"

# Initialize file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Book ID", "Title", "Author", "Status", "Issued To"])
    df.to_csv(DATA_FILE, index=False)

# Load data
def load_data():
    return pd.read_csv(DATA_FILE)

# Save data
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Add book
def add_book(book_id, title, author):
    df = load_data()
    if book_id in df['Book ID'].values:
        st.warning("Book ID already exists!")
    else:
        df.loc[len(df)] = [book_id, title, author, "Available", ""]
        save_data(df)
        st.success("Book added successfully!")

# Issue book
def issue_book(book_id, student_name):
    df = load_data()
    if book_id not in df['Book ID'].values:
        st.error("Book ID not found.")
        return
    index = df[df['Book ID'] == book_id].index[0]
    if df.loc[index, "Status"] == "Issued":
        st.warning("Book is already issued.")
    else:
        df.loc[index, "Status"] = "Issued"
        df.loc[index, "Issued To"] = student_name
        save_data(df)
        st.success("Book issued to " + student_name)

# Return book
def return_book(book_id):
    df = load_data()
    if book_id not in df['Book ID'].values:
        st.error("Book ID not found.")
        return
    index = df[df['Book ID'] == book_id].index[0]
    df.loc[index, "Status"] = "Available"
    df.loc[index, "Issued To"] = ""
    save_data(df)
    st.success("Book returned successfully!")

# Streamlit UI
st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Menu", ["Add Book", "View Books", "Issue Book", "Return Book"])

if menu == "Add Book":
    st.header("Add New Book")
    book_id = st.text_input("Book ID")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    if st.button("Add Book"):
        add_book(book_id, title, author)

elif menu == "View Books":
    st.header("All Books")
    df = load_data()
    st.dataframe(df)

elif menu == "Issue Book":
    st.header("Issue a Book")
    book_id = st.text_input("Book ID to Issue")
    student = st.text_input("Issued To (Student Name)")
    if st.button("Issue"):
        issue_book(book_id, student)

elif menu == "Return Book":
    st.header("Return a Book")
    book_id = st.text_input("Book ID to Return")
    if st.button("Return"):
        return_book(book_id)
