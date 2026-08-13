from risk_analyzer import analyze_message


message = """
URGENT! Congratulations! You have won $1000.
Click https://example.com immediately to claim your prize.
Send your OTP to verify your bank account.
"""


result = analyze_message(message)


print("\n==============================")
print("       SCAMSHIELD AI")
print("==============================")

print(
    "\nRisk Score:",
    result["risk_score"],
    "%"
)

print(
    "Risk Level:",
    result["risk_level"]
)

print(
    "\nML Model Score:",
    result["ml_score"],
    "%"
)

print(
    "Neural Network Score:",
    result["nn_score"],
    "%"
)


print("\nRisk Indicators:")

for indicator in result["indicators"]:

    print(
        "-",
        indicator
    )


print(
    "\nRecommendation:"
)

print(
    result["recommendation"]
)