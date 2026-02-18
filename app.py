import streamlit as st
from datetime import date
from pawpal_system import Pet, CareTask, Owner, DailyPlan, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("PawPal+")

# --- Session state initialisation ---
if "owner" not in st.session_state:
    st.session_state.owner = None

if "pet" not in st.session_state:
    st.session_state.pet = None

if "tasks" not in st.session_state:
    st.session_state.tasks = []   # list of CareTask objects

if "plan" not in st.session_state:
    st.session_state.plan = None

# --- Owner & Pet setup ---
st.subheader("Owner & Pet")

col1, col2, col3 = st.columns(3)
with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    pet_name = st.text_input("Pet name", value="Mochi")
with col3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    pet = Pet(name=pet_name, species=species, breed="", age=0, weight=0.0)
    owner = Owner(name=owner_name)
    owner.add_pet(pet)
    st.session_state.pet = pet
    st.session_state.owner = owner
    st.session_state.tasks = []   # reset tasks for new pet
    st.session_state.plan = None
    st.success(f"Saved {owner_name} with pet {pet_name}.")

# --- Task entry ---
st.divider()
st.subheader("Tasks")

if st.session_state.pet is None:
    st.info("Save an owner and pet above before adding tasks.")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", [1, 2, 3, 4, 5], index=2)

    if st.button("Add task"):
        task = CareTask(
            task_type="general",
            name=task_title,
            duration_minutes=int(duration),
            priority=priority,
            frequency="daily"
        )
        st.session_state.pet.add_care_task(task)
        st.session_state.tasks.append(task)
        st.success(f"Added task: {task_title}")

    if st.session_state.tasks:
        st.write("Current tasks:")
        st.table([
            {
                "Task": t.name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Completed": t.is_completed
            }
            for t in st.session_state.tasks
        ])
    else:
        st.info("No tasks yet. Add one above.")

# --- Schedule generation ---
st.divider()
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Please save an owner and pet first.")
    elif not st.session_state.tasks:
        st.warning("Please add at least one task first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        st.session_state.plan = scheduler.generate_daily_plan(date.today())
        st.success("Schedule generated!")

if st.session_state.plan is not None:
    plan = st.session_state.plan
    st.markdown(f"**Date:** {plan.date.strftime('%A, %B %d, %Y')}")
    st.markdown(f"**Reasoning:** {plan.reasoning}")

    if plan.unscheduled_tasks:
        st.markdown("**Tasks to complete:**")
        st.table([
            {
                "Task": t.name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority
            }
            for t in plan.unscheduled_tasks
        ])
