
import streamlit as st
import json

st.set_page_config(page_title="ATOgen Control Lookup", layout="wide")

st.title("ATOgen Control Narrative Viewer")
st.markdown("Search and view FedRAMP Moderate control narratives.")

@st.cache_data
def load_controls():
    with open("ATOgen_Control_Enhancements_Automation_Block.json", "r") as f:
        return json.load(f)

controls = load_controls()
control_ids = sorted([c["control_id"] for c in controls])

selected_control = st.selectbox("Select a control ID:", control_ids)
control = next((c for c in controls if c["control_id"] == selected_control), None)

if control:
    st.subheader(f"📘 {control['control_id']}")
    st.markdown(f"**Control Family:** `{control['control_family']}`")
    st.markdown(f"**Status:** `{control['status']}`")
    st.markdown("### Implementation Statement")
    st.write(control["implementation"]["statement"])
    st.markdown("### Responsible Roles")
    st.write(control["implementation"]["responsible_roles"])
    export = st.button("Export as JSON")
    if export:
        export_data = json.dumps(control, indent=2)
        st.download_button("Download JSON", export_data, file_name=f"{control['control_id']}.json")
else:
    st.warning("Control not found.")
