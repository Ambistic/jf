import json

import streamlit as st
import streamlit.components.v1 as components
import psutil


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


def main():
    current = st.session_state.get("current")
    if current is None:
        return

    # read all starts
    starts = []
    stops = []
    # read all stops
    # for each start (in the correct reversed order) if stop stop, if pid run, else crashed

    with open(current, "r") as f:
        for line in f.readlines():
            el = json.loads(line)
            if el["status"] == "start":
                starts.append(el)
            elif el["status"] == "stop":
                stops.append(el)

    for start in starts:
        dual = start.copy()
        dual["status"] = "stop"
        if dual in stops:
            start["streamlit_status"] = "Stopped"
            start["css"] = "bg-success"
        elif psutil.pid_exists(start["pid"]):
            start["streamlit_status"] = "Running"
            start["css"] = "bg-primary"
        else:
            start["streamlit_status"] = "Crashed"
            start["css"] = "bg-danger"

    components.html("""
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
         integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    """)

    for start in starts[::-1]:
        components.html(f"""
        <div class="card text-white {start["css"]} mb-3">
            Name : {start["name"]}, pid : {start["pid"]}, status : {start["streamlit_status"]}
        </div>
        """)
