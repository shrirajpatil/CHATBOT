from transformers import pipeline

# Load the question-answering pipeline with a BERT-based model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Example passage
# Read content from the text file
file_path = "chat/space_data.txt"  # Replace with the actual path to your text file
with open(file_path, "r", encoding="utf-8") as file:
    passage = file.read()
# Ask questions
question1 = "What is moon"
question2 = "Who is founder of ISRO?"

# Process passage and answer questions
answer1 = qa_pipeline({"context": passage, "question": question1})
answer2 = qa_pipeline({"context": passage, "question": question2})

# Print answers
print("Answer 1:", answer1['answer'])
print("Answer 2:", answer2['answer'])
