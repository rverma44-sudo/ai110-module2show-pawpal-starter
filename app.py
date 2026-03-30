import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# Owner must persist so pets and available-time settings survive every rerun
if "owner" not in st.session_state:
    st.session_state["owner"] = Owner(
        name="Jordan",
        email="",
        available_minutes_per_day=60,
    )

# The active pet must persist so task additions target the correct Pet across reruns
if "current_pet" not in st.session_state:
    st.session_state["current_pet"] = None

# The scheduler must persist so the last generated plan is still visible after any widget interaction
if "scheduler" not in st.session_state:
    st.session_state["scheduler"] = None


def _make_scoped_scheduler(owner: Owner, pet: Pet) -> Scheduler:
    """Build a Scheduler scoped to one pet, sharing the owner's time budget."""
    scoped = Owner(owner.name, owner.email, owner.available_minutes_per_day)
    scoped.add_pet(pet)
    return Scheduler(scoped)


# ---------------------------------------------------------------------------
st.title("🐾 PawPal+")

owner: Owner = st.session_state["owner"]

# --- Owner settings --------------------------------------------------------
st.subheader("Owner Settings")
with st.form("owner_form"):
    col1, col2 = st.columns(2)
    with col1:
        owner_name_input = st.text_input("Your name", value=owner.name)
    with col2:
        available_input = st.number_input(
            "Available minutes per day",
            min_value=1,
            max_value=1440,
            value=owner.available_minutes_per_day,
        )
    if st.form_submit_button("Update owner"):
        if not owner_name_input.strip():
            st.error("Owner name cannot be empty.")
        else:
            owner.name = owner_name_input.strip()
            owner.set_available_time(int(available_input))
            st.success(f"Updated: {owner.name}, {owner.available_minutes_per_day} min/day.")

st.divider()

# --- Add a pet -------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name_input = st.text_input("Pet name")
        species_input = st.selectbox("Species", ["Dog", "Cat", "Bird", "Rabbit", "Other"])
    with col2:
        breed_input = st.text_input("Breed")
        age_input = st.number_input("Age (years)", min_value=0, max_value=30, value=1)
    health_input = st.text_input("Health notes (comma-separated, optional)")
    if st.form_submit_button("Add pet"):
        if not pet_name_input.strip():
            st.error("Pet name cannot be empty.")
        elif not breed_input.strip():
            st.error("Breed cannot be empty.")
        else:
            health_notes = [n.strip() for n in health_input.split(",") if n.strip()]
            new_pet = Pet(
                name=pet_name_input.strip(),
                species=species_input,
                breed=breed_input.strip(),
                age_years=int(age_input),
                health_notes=health_notes,
            )
            owner.add_pet(new_pet)
            st.success(f"{new_pet.name} ({new_pet.species}) added successfully.")

pets = owner.get_pets()
if pets:
    st.markdown("**Your pets:**")
    st.table([
        {"Name": p.name, "Species": p.species, "Breed": p.breed, "Age (yrs)": p.age_years}
        for p in pets
    ])

st.divider()

# --- Add a task ------------------------------------------------------------
st.subheader("Schedule a Task")

if not pets:
    st.info("Add at least one pet above before scheduling tasks.")
else:
    selected_name = st.selectbox("Select pet", [p.name for p in pets])
    selected_pet: Pet = next(p for p in pets if p.name == selected_name)
    st.session_state["current_pet"] = selected_pet

    with st.form("add_task_form"):
        col1, col2 = st.columns(2)
        with col1:
            task_name_input = st.text_input("Task name")
            duration_input = st.number_input(
                "Duration (minutes)", min_value=1, max_value=480, value=20
            )
        with col2:
            priority_input = st.slider("Priority (1 = low, 5 = high)", min_value=1, max_value=5, value=3)
            category_input = st.selectbox(
                "Category",
                ["exercise", "nutrition", "health", "hygiene", "enrichment", "grooming", "other"],
            )
        if st.form_submit_button("Add task & generate plan"):
            if not task_name_input.strip():
                st.error("Task name cannot be empty.")
            else:
                new_task = Task(
                    name=task_name_input.strip(),
                    duration_minutes=int(duration_input),
                    priority=int(priority_input),
                    category=category_input,
                )
                selected_pet.add_task(new_task)
                st.session_state["scheduler"] = _make_scoped_scheduler(owner, selected_pet)
                st.session_state["scheduler"].generate_plan()
                st.success(f"Task '{new_task.name}' added to {selected_pet.name}.")

    current_tasks = selected_pet.get_tasks()
    if current_tasks:
        st.markdown(f"**All tasks for {selected_pet.name}:**")
        st.table([
            {
                "Task": t.name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Category": t.category,
            }
            for t in current_tasks
        ])

st.divider()

# --- Today's schedule ------------------------------------------------------
st.subheader("Today's Schedule")

scheduler: Scheduler | None = st.session_state["scheduler"]
if scheduler is None or not scheduler.scheduled_tasks:
    st.info("No schedule yet. Add tasks above and a plan will be generated automatically.")
else:
    total = scheduler.get_total_scheduled_duration()
    budget = owner.available_minutes_per_day
    st.markdown(
        f"**{len(scheduler.scheduled_tasks)} task(s) scheduled — "
        f"{total} / {budget} min used**"
    )
    st.dataframe(
        [
            {
                "Task": t.name,
                "Duration (min)": t.duration_minutes,
                "Priority": t.priority,
                "Category": t.category,
            }
            for t in scheduler.scheduled_tasks
        ],
        use_container_width=True,
    )
    explanation = scheduler.explain_plan()
    if explanation:
        st.info(explanation)
