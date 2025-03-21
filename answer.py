import json

def load_questionnaires(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return json.load(file)

def update_questionnaires(questionnaires):
    fill_type = input("Do you want to fill the 'checkbox' or the 'text' answers (c/t) ").strip().lower()
    if fill_type in ['c', 't']:
        if fill_type == 'c':    
            for question in questionnaires.get('questions', []):
                if question.get('answerType') == 3:
                    answer = input(f"Set 'expectedValue' for question '{question['description']}' to true or false? ").strip().lower()
                    if answer in ['t', 'f']:
                        question['expectedValue'] = (answer == 't')
                    else:
                        print(f"Invalid input for question '{question['question']}'. Skipping...")
        else:
            for question in questionnaires.get('questions', []):
                pass
                   
                    
                    
    return questionnaires

def save_questionnaires(file_path, questionnaires):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(questionnaires, file, ensure_ascii=False ,indent=4)

if __name__ == "__main__":
    file_path = 'questionnaires.json'
    questionnaires = load_questionnaires(file_path)
    updated_questionnaires = update_questionnaires(questionnaires)
    save_questionnaires(file_path, updated_questionnaires)