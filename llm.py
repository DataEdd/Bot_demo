import os
from openai import OpenAI
import requests
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

cerebras_client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

# Initialize OpenAI API client

# Load system prompt
with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

# Function to get student data from the local API (error handling added)
def get_student_data(uid):
    try:
        response = requests.get(f"http://localhost:8000/students/{uid}")
        response.raise_for_status()  # Raise an error if the response code is not 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching student data: {e}")
        return None


# Function to create an issue in Cerebras when there's a price discrepancy
def create_price_discrepancy_issue(user_id, provider_name, estimated_price, actual_price):
    issue_data = {
        "user_id": user_id,
        "provider_name": provider_name,
        "estimated_price": estimated_price,
        "actual_price": actual_price,
        "issue_type": "price_discrepancy",
        "status": "open",
        "details": "Price discrepancy between estimated and actual billed amount."
    }
    issue_response = cerebras_client.create_issue(issue_data)
    
    if issue_response["status"] == "success":
        print(f"Issue created successfully for user {user_id} with provider {provider_name}")
        return issue_response["issue_id"]
    else:
        print("Failed to create issue.")
        return None


# Get user context (replace with actual UID you're testing)
uid = "918859330"  # Change before production; import from login
student = get_student_data(uid)

if not student:
    print("Could not fetch student data. Exiting...")
    exit()

# Initial conversation history
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": f"Student info: {student}"}
]

print("👩‍⚕️ SHIPSmart is ready. Ask your insurance cost question below.")
print("Type 'exit' to quit.\n")

def chat_with_ai():
    while True:
        user_input = input("🧑 You: ")

        if user_input.lower() in {"exit", "quit"}:
            print("👋 Bye! Stay healthy.")
            break

        # Add user message to history
        messages.append({"role": "user", "content": user_input})

        # Send to OpenAI (corrected method: ChatCompletion.create)
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can also use "gpt-4" if available
        messages=messages,
        temperature=0.3)

        ai_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_message})

        print("\n🤖 SHIPSmart:\n")
        print(ai_message)
        print("\n---")
                # Simulate price discrepancy (if the issue is mentioned)
        if "charged" in user_input.lower() and "discrepancy" in user_input.lower():
            # You would typically extract this from the user input (this is just for demo purposes)
            estimated_price = 150  # Example estimated price
            actual_price = 200     # Example actual charged price
            issue_id = create_price_discrepancy_issue(uid, "HealthyCare Clinic", estimated_price, actual_price)
            
            if issue_id:
                print(f"Price discrepancy issue created with ID: {issue_id}")


# Start the chat
chat_with_ai()
