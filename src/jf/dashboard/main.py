import streamlit as st


def init():
    # config file
    pass


def sidebar():
    with st.sidebar():
        st.header("Select a project")
        st.radio("Projects", list_project)


def main():
    pass


if __name__ == "__main__":
    init()
    sidebar()
    main()