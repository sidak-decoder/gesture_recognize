import streamlit as st
from app import Login

def main():
    st.title("Login App")
    login = Login()
    login.login_window.mainloop()

if __name__ == "__main__":
    main()