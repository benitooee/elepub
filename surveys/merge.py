import os
import pandas as pd

# Folder where your CSVs live
DATA_DIR = "."

# List of model CSV filenames you showed in the screenshot.
# If you add more later, just add them to this list.
MODEL_FILES = [
    "gemma-3-1b-it.csv",
    "gemma-3-4b-it.csv",
    "gemma-3-270m-it.csv",
    "Qwen2.5-0.5B.csv",
    "Qwen2.5-1.5B.csv",
    "Qwen2.5-3B.csv",
    "Qwen2.5-7B.csv",
    "Qwen2.5-14B.csv",
    "Yi-1.5-6B.csv",
    "Yi-1.5-9B.csv",
]

def main():
    # Build full paths and keep only existing files
    files = []
    for name in MODEL_FILES:
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            files.append(path)
        else:
            print(f"WARNING: {name} not found, skipping.")

    if not files:
        print("No model CSVs found. Check DATA_DIR and MODEL_FILES.")
        return

    print("Files to merge:")
    for f in files:
        print(" -", os.path.basename(f))

    # === 1) Use the first file as the base ===
    first_file = files[0]
    first_name = os.path.splitext(os.path.basename(first_file))[0]

    print(f"\nUsing {os.path.basename(first_file)} as the base table.")

    base_df = pd.read_csv(first_file)

    if "question" not in base_df.columns or "response" not in base_df.columns:
        raise ValueError(f"{first_file} must have 'question' and 'response' columns.")

    # Start with question + first model
    merged = pd.DataFrame()
    merged["question"] = base_df["question"]
    merged[first_name] = base_df["response"]

    # === 2) Add each remaining model by row index ===
    for f in files[1:]:
        model_name = os.path.splitext(os.path.basename(f))[0]
        print(f"\nAdding model: {model_name}")

        df = pd.read_csv(f)

        if "question" not in df.columns or "response" not in df.columns:
            raise ValueError(f"{f} must have 'question' and 'response' columns.")

        # Optional: sanity check that questions line up
        if not df["question"].equals(merged["question"]):
            print(f"WARNING: questions differ in {model_name}; falling back to merge on text.")
            df_model = df[["question", "response"]].rename(columns={"response": model_name})
            merged = merged.merge(df_model, on="question", how="outer")
        else:
            # Same questions, same order → just attach by index (very fast)
            merged[model_name] = df["response"].values

    # === 3) Save result ===
    out_path = os.path.join(DATA_DIR, "merged_models.csv")
    merged.to_csv(out_path, index=False)
    print("\n✅ Merged CSV saved as:", out_path)

if __name__ == "__main__":
    main()
