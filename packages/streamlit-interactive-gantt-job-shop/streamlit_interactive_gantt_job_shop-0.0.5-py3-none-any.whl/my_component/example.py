import streamlit as st
from my_component import gantt_component

st.set_page_config(layout="wide")
st.title("My Gantt Chart")

tasks_data = {
    "data": [
        {"id": "machine1", "text": "Machine #1", "type": "project", "open": True},
        {"id": "job1", "text": "Job #1", "start_date": "2025-03-14", "duration": 3, "parent": "machine1", "priority": "1"},
        {"id": "job2", "text": "Job #2", "start_date": "2025-03-17", "duration": 2, "parent": "machine1"},
        {"id": "machine2", "text": "Machine #2", "type": "project", "open": True},
        {"id": "job3", "text": "Job #3", "start_date": "2025-03-15", "duration": 5, "parent": "machine2", "machine": "machine2"},
        {"id": "job4", "text": "Job #4", "start_date": "2025-03-20", "duration": 4, "parent": "machine2"}
    ]
}


result = gantt_component(tasks=tasks_data, key="mygantt")

st.write("Component returned:", result)
if result and result.get("action") == "task_updated":
    st.write(f"Task {result['task_id']} was updated to:", result["task_data"])
