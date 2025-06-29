import json

# Load rules
with open("data/prescriptions.json", "r") as f:
    rules = json.load(f)

def suggest_prescription(problem_text):
    problem_text = problem_text.lower()
    for condition in rules:
        for keyword in condition["keywords"]:
            if keyword in problem_text:
                return {
                    "tablets": condition.get("tablets", []),
                    "syrups": condition.get("syrups", [])
                }
    return {}

# ✅ Test block
if __name__ == "__main__":
    problem = input("Enter a sample problem: ")
    prescription = suggest_prescription(problem)
    print("\nSuggested Prescription:")
    print("Tablets:", prescription.get("tablets", []))
    print("Syrups:", prescription.get("syrups", []))
