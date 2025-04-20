import os
from cerebras.cloud.sdk import Cerebras
import openai
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Initialize Cerebras client
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

def contact_provider_and_insurer(user_id, provider_name, estimated_price, actual_price):
    """
    Create an issue to resolve a price discrepancy with the insurer and provider.
    """
    issue_data = {
        "user_id": user_id,
        "provider_name": provider_name,
        "estimated_price": estimated_price,
        "actual_price": actual_price,
        "issue_type": "price_discrepancy",
        "status": "open",
        "details": "Price discrepancy between estimated and actual billed amount."
    }
    
    issue_response = client.create_issue(issue_data)

    if issue_response["status"] == "success":
        print(f"Issue created successfully for user {user_id} with provider {provider_name}")
        return issue_response["issue_id"]
    else:
        print("Failed to create issue.")
        return None

# Example function to update the issue status
def update_issue_status(issue_id, new_status):
    """
    Update the status of an issue (e.g., 'resolved', 'pending', etc.)
    """
    update_data = {
        "status": new_status,
        "issue_id": issue_id
    }

    update_response = client.update_issue(update_data)

    if update_response["status"] == "success":
        print(f"Issue {issue_id} updated to {new_status}")
    else:
        print("Failed to update issue.")
def estimate_cost(user_input, user_id):
    """
    Estimate the medical cost using OpenAI model (or Gemini) by interacting with llm.py
    """
    # Interacting with llm.py to process user input and estimate cost
    from llm import start_chat

    # Initialize chat session
    chat_session = start_chat(user_input)

    # Collect the chat response
    estimated_cost = ""
    while True:
        # Get the next message from the chat loop
        message = chat_session.get_response()
        estimated_cost = message

        # Check if the loop should end (e.g., user confirms the estimate)
        if "end" in message.lower():
            break
    
    # Return the estimated cost
    return estimated_cost
# Function to retrieve student data from the API
def get_student_data(uid):
    """
    Retrieve student data from the local FastAPI server
    """
    response = requests.get(f"http://localhost:8000/students/{uid}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example function to simulate the booking and form-filling process
def book_appointment(user_id, provider_id, service_type):
    """
    Simulate the appointment booking process
    """
    student_data = get_student_data(user_id)
    if student_data:
        print(f"Booking appointment for {student_data['first_name']} with provider {provider_id} for {service_type}")
        # Simulate booking with some dummy logic
        print("Appointment booked successfully!")
        return True
    else:
        print("Error: User data not found.")
        return False

# Main execution logic for demonstration
if __name__ == "__main__":
    # Example user and provider data
    user_id = "918859330"
    provider_id = 1
    service_type = "Dental Cleaning"
    
    # Get student data and proceed with booking
    book_appointment(user_id, provider_id, service_type)

    # Estimate cost based on user input
    user_input = "I need a dental cleaning and I am worried about the cost."
    estimated_cost = estimate_cost(user_input, user_id)
    print(f"Estimated cost: {estimated_cost}")
    
    # Simulate issue handling
    issue_id = contact_provider_and_insurer(user_id, "HealthyCare Clinic", 150.00, 200.00)
    if issue_id:
        update_issue_status(issue_id, "resolved")
