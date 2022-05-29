import json

import streamlit as st
import streamlit.components.v1 as components
import psutil
import pandas as pd


BASE_HTML_CODE = """
                    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
                     integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                """


def init(conf_path):
    with open(conf_path, "r") as f:
        lines = [x.strip() for x in f.readlines()]
    st.session_state["projects"] = lines


def sidebar():
    with st.sidebar:
        st.header("Select a project")
        r = st.radio("Projects", st.session_state["projects"])

        for proj in st.session_state["projects"]:
            if r == proj:
                st.session_state["current"] = proj


def is_empty(line):
    return len(line) == 0


def is_stopped(row, df):
    return not df[
        (df.pid == row.pid)
        & (df["name"] == row["name"])
        & (df.status == "end")
    ].empty


def is_crashed(row, df):
    return not df[
        (df.pid == row.pid)
        & (df["name"] == row["name"])
        & (df.status == "crash")
    ].empty


def is_running(row):
    return psutil.pid_exists(row.pid)


def get_status(row, df):
    if is_stopped(row, df):
        return "stopped"
    elif is_crashed(row, df):
        return "crashed"
    elif is_running(row):
        return "running"
    else:
        return "killed"


def get_css(streamlit_status):
    dict_corr = dict(
        stopped="bg-success",
        running="bg-primary",
        crashed="bg-danger",
        killed="bg-dark"
    )
    return dict_corr.get(streamlit_status, "bg-warning")


def main():
    current = st.session_state.get("current")
    if current is None:
        return

    elements = []

    with open(current, "r") as f:
        for line in f.read().split("\n"):
            if is_empty(line):
                continue
            el = json.loads(line)
            elements.append(el)

    df = pd.DataFrame(elements)

    html_code = BASE_HTML_CODE

    for i, row in df.iterrows():
        if row["status"] != "start":
            continue
        streamlit_status = get_status(row, df)
        css = get_css(streamlit_status)

        html_code += f"""
                <div class="card text-white {css} mb-3">
                    Name : {row["name"]}, pid : {row["pid"]}, status : {streamlit_status}
                </div>
                """

    components.html(html_code)
