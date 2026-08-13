import pandas as pd


input_file = "dataset/SMSSpamCollection"
output_file = "dataset/scam_messages.csv"


# Load original dataset
df = pd.read_csv(
    input_file,
    sep="\t",
    header=None,
    names=["original_label", "message"],
    encoding="utf-8"
)


# Convert labels
df["label"] = df["original_label"].map({
    "ham": "safe",
    "spam": "scam"
})


# Keep only required columns
df = df[["label", "message"]]


# Remove missing values
df = df.dropna()


# Remove duplicate messages
df = df.drop_duplicates()


# Save converted dataset
df.to_csv(output_file, index=False)


print("Dataset prepared successfully!")
print()
print("Total messages:", len(df))
print()
print("Label distribution:")
print(df["label"].value_counts())