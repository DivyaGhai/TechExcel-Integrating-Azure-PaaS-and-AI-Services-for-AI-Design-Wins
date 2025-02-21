import requests
import streamlit as st

st.set_page_config(layout="wide")

@st.cache_data
def get_hotels():
    """Return a list of hotels from the API."""
    api_endpoint = st.secrets["api"]["endpoint"]

    if not api_endpoint.startswith("http"):
        api_endpoint = f"https://{api_endpoint}"

    response = requests.get(f"{api_endpoint}/Hotels", timeout=10)

    # Check if the response is successful and contains JSON
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Response content is not valid JSON.")
            return []
    else:
        st.error(f"Failed to fetch hotels. Status code: {response.status_code}")
        return []


@st.cache_data
def get_hotel_bookings(hotel_id):
    """Return a list of bookings for the specified hotel."""
    api_endpoint = st.secrets["api"]["endpoint"]
    response = requests.get(f"{api_endpoint}/Hotels/{hotel_id}/Bookings", timeout=10)

    # Check if the response is successful and contains JSON
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            st.error("Response content is not valid JSON.")
            return []
    else:
        st.error(f"Failed to fetch bookings. Status code: {response.status_code}")
        return []


@st.cache_data
def invoke_chat_endpoint(question):
    """Invoke the chat endpoint with the specified question."""
    api_endpoint = st.secrets["api"]["endpoint"]
    response = requests.post(f"{api_endpoint}/Chat", data={"message": question}, timeout=10)

    # Check if the response is successful and contains JSON
    if response.status_code == 200:
        try:
            return response.json()  # Assuming the response is in JSON
        except ValueError:
            st.error("Response content is not valid JSON.")
            return {}
    else:
        st.error(f"Failed to get response from Chat endpoint. Status code: {response.status_code}")
        return {}


def main():
    """Main function for the Chat with Data Streamlit app."""

    st.write(
    """
    # API Integration via Semantic Kernel

    This Streamlit dashboard is intended to demonstrate how we can use
    the Semantic Kernel library to generate SQL statements from natural language
    queries and display them in a Streamlit app.

    ## Select a Hotel
    """
    )

    # Display the list of hotels as a drop-down list
    hotels_json = get_hotels()
    if not hotels_json:  # If no hotels are fetched
        return

    # Reshape hotels to an object with hotelID and hotelName
    hotels = [{"id": hotel["hotelID"], "name": hotel["hotelName"]} for hotel in hotels_json]
    
    selected_hotel = st.selectbox("Hotel:", hotels, format_func=lambda x: x["name"])

    # Display the list of bookings for the selected hotel as a table
    if selected_hotel:
        hotel_id = selected_hotel["id"]
        bookings = get_hotel_bookings(hotel_id)
        if bookings:  # If bookings are available
            st.write("### Bookings")
            st.table(bookings)

    st.write(
        """
        ## Ask a Bookings Question

        Enter a question about hotel bookings in the text box below.
        Then select the "Submit" button to call the Chat endpoint.
        """
    )

    question = st.text_input("Question:", key="question")
    if st.button("Submit"):
        with st.spinner("Calling Chat endpoint..."):
            if question:
                response = invoke_chat_endpoint(question)
                if response:
                    st.write(response)
                    st.success("Chat endpoint called successfully.")
                else:
                    st.warning("No response from Chat endpoint.")
            else:
                st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
