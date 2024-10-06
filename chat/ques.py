import re

def extract_questions(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Use regular expression to find sentences ending with a question mark
    questions = [question.strip() for question in re.findall(r'[^.!?]*\?', content)]

    return questions

# Replace 'space_data.txt' with the actual path to your file
file_path = 'chat/space_data.txt'
questions_array = extract_questions(file_path)

# Print the array of questions
for i, question in enumerate(questions_array, 1):
    print(questions_array)
