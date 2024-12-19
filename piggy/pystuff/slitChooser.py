import streamlit as st

def main():
    st.title("Streamlit: Choose from List or Freeform Input")

    options = ["Option 1", "Option 2", "Option 3", "Other (Freeform)"]

    selected_option = st.selectbox("Select an option:", options)

    if selected_option == "Other (Freeform)":
        freeform_input = st.text_input("Enter your freeform data:")
        if st.button("Submit Freeform"):
            if freeform_input:
                st.write(f"You entered: {freeform_input}")
            else:
                st.warning("Please enter some text.")
    else:
        st.write(f"You selected: {selected_option}")


    st.markdown("---")
    st.subheader("Alternative using `st.multiselect` with Freeform")

    all_options = ["Apple", "Banana", "Orange"]
    selected_options = st.multiselect("Select items (or type to add):", all_options)

    new_options = []
    for option in selected_options:
        if option not in all_options:  # Check if it's a new entry
            new_options.append(option)
    
    if new_options:
        st.write("You added the following new items:")
        for new_option in new_options:
            st.write(f"- {new_option}")

    st.write("You selected the following existing items:")
    for option in selected_options:
        if option in all_options:
            st.write(f"- {option}")
    

if __name__ == "__main__":
    main()
