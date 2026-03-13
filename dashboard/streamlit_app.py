import streamlit as st
import requests
import pandas as pd
from datetime import timezone, timedelta, date

API = "https://supreme-space-fiesta-6q77r6rgxjv35674-8000.app.github.dev"

st.title("Free Will Erosion Engine")

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token is None:

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            res = requests.post(
                f"{API}/auth/login",
                data={
                    "username": username,
                    "password": password
                }
            )

            if res.status_code == 200:
                st.session_state.token = res.json()["access_token"]
                st.success("Logged in successfully")
                st.rerun()
            else:
                st.error("Login failed")

    with tab2:

        new_user = st.text_input("New Username")
        new_email = st.text_input("Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):

            res = requests.post(
                f"{API}/auth/register",
                json={
                    "username": new_user,
                    "email": new_email,
                    "password": new_pass
                }
            )

            if res.status_code == 201:
                st.success("Account created. Please login.")
            else:
                st.error("Registration failed")

else:

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }
    st.header("Log a Decision")

    with st.form("decision_form"):

        action = st.selectbox(
            "Action",
            [
                "wake_up",
                "sleep",
                "breakfast",
                "lunch",
                "dinner",
                "snacks",
                "scroll_instagram",
                "youtube/netflix/anime",
                "study",
                "work",
                "school",
                "game",
                "exercise",
                "walk"
            ]
        )
        domain = st.selectbox(
            "Domain",
            [
                "sleep",
                "work",
                "movement",
                "leisure",
                "health",
                "entertainment",
                "social",
                "food"
            ]
        )

        occurred_at = st.datetime_input("Time")

        submitted = st.form_submit_button("Log Decision")

        if submitted:

            ist = timezone(timedelta(hours=5, minutes=30))

            payload = {
                "action": action,
                "domain": domain,
                "occurred_at": occurred_at.replace(tzinfo=ist).isoformat()
            }

            res = requests.post(
                f"{API}/decision/log",
                json=payload,
                headers=headers
            )

            if res.status_code == 201:
                st.success("Decision logged successfully")
                st.rerun()
            else:
                st.error("Failed to log decision")
                st.write(res.text)
                
    st.header("Recent Decisions")

    st.subheader("History")

    recent_start = (date.today() - timedelta(days=15)).isoformat()
    recent_end = date.today().isoformat()

    res = requests.get(
        f"{API}/analysis/history",
        headers=headers,
        params={
            "start_date": recent_start,
            "end_date": recent_end
        }
    )

    if res.status_code != 200:
        st.error("Failed to fetch history")
        st.write(res.text)
        st.stop()

    history = res.json()

    if history:

        df_recent = pd.DataFrame(history)

        df_recent["timestamp"] = pd.to_datetime(df_recent["timestamp"])

        df_recent = df_recent.sort_values("timestamp", ascending=False).head(10)

        for _, row in df_recent.iterrows():

            col1, col2, col3 = st.columns([6,1,1])

            col1.write(f"{row['timestamp']} — {row['action']} ({row['domain']})")

            if col2.button("Edit", key=f"edit_{row['id']}"):
                st.session_state.edit_id = row["id"]
                st.session_state.edit_action = row["action"]
                st.session_state.edit_domain = row["domain"]

            if col3.button("Delete", key=f"delete_{row['id']}"):

                requests.delete(
                    f"{API}/decision/{row['id']}",
                    headers=headers
                )

                st.rerun()

    else:
        st.info("No decisions logged yet.")

    if "edit_id" in st.session_state:

        st.subheader("Edit Decision")

        new_action = st.text_input(
            "Action",
            value=st.session_state.get("edit_action", "")
        )

        new_domain = st.text_input(
            "Domain",
            value=st.session_state.get("edit_domain", "")
        )

        if st.button("Save Changes"):

            payload = {
                "action": new_action,
                "domain": new_domain,
                "occurred_at": datetime.now().isoformat()
            }

            res = requests.put(
                f"{API}/decision/{st.session_state.edit_id}",
                json=payload,
                headers=headers
            )

            if res.status_code == 200:

                del st.session_state["edit_id"]
                del st.session_state["edit_action"]
                del st.session_state["edit_domain"]

                st.success("Decision updated")
                st.rerun()

            else:
                st.error("Update failed")
                st.write(res.text)
                
    st.subheader("Filter Decisions")

    col1, col2 = st.columns(2)

    start_date = col1.date_input(
        "Start Date",
        date.today() - timedelta(days=7)
    )

    end_date = col2.date_input(
        "End Date",
        date.today()
    )

    if st.button("Load History"):

        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        res = requests.get(
            f"{API}/analysis/history",
            headers=headers,
            params=params
        )

        if res.status_code != 200:
            st.error("Failed to fetch filtered history")
            st.write(res.text)
            st.stop()

        history = res.json()

        if history:

            df = pd.DataFrame(history)

            df["timestamp"] = pd.to_datetime(df["timestamp"])

            df = (
                df
                .sort_values("timestamp", ascending=True)
                .drop(columns=["id"])
            )

            st.dataframe(df, height=350)

        else:
            st.info("No decisions in selected range.")            
    
    st.header("Behavior Analytics Dashboard")

    res = requests.get(
        f"{API}/analysis/today",
        headers=headers
    )

    if res.status_code != 200:
        st.error(f"API Error {res.status_code}")
        st.write(res.text)
        st.stop()

    today = res.json()

    col1, col2, col3 = st.columns(3)

    col1.metric("Free Will Index", today["free_will_index"])
    col2.metric("Entropy", today["entropy_score"])
    col3.metric("Predictability", today["predictability_score"])

    res = requests.get(
        f"{API}/analysis/summary",
        headers=headers
    )

    if res.status_code != 200:
        st.error(f"API error {res.status_code}")
        st.write(res.text)
        st.stop()

    summary = res.json()
    df = pd.DataFrame(summary)

    if not df.empty:
        st.subheader("Entropy Trend")
        st.line_chart(df.set_index("date")["entropy_score"])

    st.subheader("Action Frequency")

    res = requests.get(
        f"{API}/analysis/history",
        headers=headers,
        params={
            "start_date": "2000-01-01",
            "end_date": "2100-01-01"
        }
    )

    if res.status_code != 200:
        st.error("Failed to fetch history for frequency chart")
        st.write(res.text)
    else:

        history = res.json()

        if history:

            df_actions = pd.DataFrame(history)

            action_counts = (
                df_actions["action"]
                .value_counts()
                .head(10)
                .sort_values(ascending=True)
            )

            st.bar_chart(action_counts)

        else:
            st.info("Not enough data to generate action frequency chart.")
            
    st.subheader("Next Action Prediction")

    res = requests.get(
        f"{API}/analysis/predict-next",
        headers=headers
    )

    if res.status_code == 200:

        prediction = res.json()

        if prediction["next_action"]:
            st.success(
                f"Next likely action: {prediction['next_action']} "
                f"(confidence {prediction['confidence']:.2f})"
            )
        else:
            st.info(prediction.get("reason", "Not enough data"))

    st.subheader("Behavior Simulation")

    res = requests.get(
        f"{API}/analysis/simulate",
        headers=headers
    )

    if res.status_code == 200:

        sim = res.json()

        st.write("Predicted 24h Predictability:", sim["predictability_24h"])

        st.write("Dominant Habit Loop:")
        st.write(" → ".join(sim["dominant_loop"]))

        st.write("Simulated Future Sequence:")
        st.write(" → ".join(sim["simulated_sequence"][:20]))

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()