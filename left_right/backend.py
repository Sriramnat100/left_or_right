
import json
from dotenv import load_dotenv
import openai
import os
load_dotenv('key.env')  # This is the line that loads .env
openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key


class Opener:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        self.qs = data[:20]
        self.scoring = {}
        for score_dict in data[20:]:
            self.scoring.update(score_dict)

    def get_qs(self):
        questions = []
        for question in self.qs:
            questions.append(question['question'])
        return questions
    
    def get_vals(self):
        bools = []
        for bool in self.qs:
            bools.append(bool['left_leaning'])
        return bools
    
    def analyzer(self, result, booleans):

        total_prefs = []
        total_resps = []
        n = 1

        for response in result:
            key = result[response]
            if response == "user-pref-" + str(n):
                total_prefs.append(self.scoring[key])
                n = n + 1
            else:
                total_resps.append(self.scoring[key])

        #len(total_prefs) == len(total_resps) == len(booleans)
        for i in range(len(total_prefs)):
            if booleans[i]:
                total_prefs[i] = total_prefs[i] * total_resps[i]
            else:
                total_prefs[i] = -1 * total_prefs[i] * total_resps[i]

        f_total = sum(total_prefs)

        return f_total





class Chatbot:
  def __init__(self):
    #Saving the convorsations. The first "system" explains GPT's task. Second and third lines show sample questions. Last one is a 
    self.message_history = [
        {"role": "system", "content": "You are an assistant that determines who someone is likely to vote for based on the demographics that I feed you. I need a specific answer."},
        {"role": "user", "content": "Age 30, Female, Hispanic, Bachelor's degree, Income $50,000, Occupation: Teacher, Single, Lives in California, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},
        {"role": "user", "content": "Age 45, Male, White, High school diploma, Income $40,000, Occupation: Factory Worker, Married, Lives in Texas, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."},

        # Additional Democratic samples without party affiliation
        {"role": "user", "content": "Age 25, Female, African American, Master's degree, Income $60,000, Occupation: Social Worker, Single, Lives in New York, Non-religious, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},
        {"role": "user", "content": "Age 35, Male, Asian, PhD, Income $80,000, Occupation: Scientist, Married, Lives in Washington, Buddhist, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},
        {"role": "user", "content": "Age 50, Female, White, Bachelor's degree, Income $70,000, Occupation: Nurse, Divorced, Lives in Illinois, Jewish, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},
        {"role": "user", "content": "Age 28, Male, Hispanic, Bachelor's degree, Income $55,000, Occupation: Software Engineer, Single, Lives in Colorado, Non-religious, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},
        {"role": "user", "content": "Age 40, Female, Black, Associate degree, Income $45,000, Occupation: Teacher, Married, Lives in Florida, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Democratic candidate."},

        # Additional Republican samples without party affiliation
        {"role": "user", "content": "Age 55, Male, White, Some college, Income $100,000, Occupation: Business Owner, Married, Lives in Alabama, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."},
        {"role": "user", "content": "Age 60, Female, White, High school diploma, Income $30,000, Occupation: Retired, Widowed, Lives in Kansas, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."},
        {"role": "user", "content": "Age 50, Male, White, Bachelor's degree, Income $75,000, Occupation: Police Officer, Married, Lives in Ohio, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."},
        {"role": "user", "content": "Age 45, Female, White, Associate degree, Income $65,000, Occupation: Administrative Assistant, Married, Lives in South Carolina, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."},
        {"role": "user", "content": "Age 35, Male, White, High school diploma, Income $50,000, Occupation: Truck Driver, Single, Lives in Missouri, Christian, Never voted?"},
        {"role": "assistant", "content": "Based on the provided demographics, this person is likely to vote for a Republican candidate."}
        ]


  #defining gpt function
  def chat(self, user_input, role="user"):


    texts = ""
    for key in user_input:
        texts += f"{key}: {user_input[key]}, "

    texts = texts.rstrip(", ")


    self.message_history.append({"role": role, "content": texts})

      
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages= self.message_history
    )

    reply_content = response.choices[0].message.content

    return reply_content


    
