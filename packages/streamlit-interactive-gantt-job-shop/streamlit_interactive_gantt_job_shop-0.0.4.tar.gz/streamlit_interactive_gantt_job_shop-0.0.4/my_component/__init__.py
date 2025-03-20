import os
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = False  # or True when you build for production

if not _RELEASE:
    _component_func = components.declare_component(
        "your_component_name",
        url="http://localhost:3001"  # dev mode
    )
else:
    build_dir = os.path.join(os.path.dirname(__file__), "frontend/build")
    _component_func = components.declare_component(
        "your_component_name",
        path=build_dir
    )

def gantt_component(tasks, key=None):
    """
    A Python function to display the Gantt chart with tasks.
    """
    return _component_func(tasks=tasks, key=key, default=None)
