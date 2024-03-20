from openai import OpenAI as Real_OpenAI
import openai
import os

os.environ["OPENAI_API_KEY"] = "你的api"
# openai_agent = Real_OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Used to generate questions
def question_generation(agent, role="a 12 year old child"):
    template = "Play the role of a {role} and generate 100 question that the {role} would ask. Don't generate the same question you have generated before."
    prompt = [{"role": "user", "content": template.format(role=role)}]
    return agent.chat.completions.create(messages = prompt, model="gpt-3.5-turbo")['choices']['message']['content']


def gpt4_generate(system, content, model_type="gpt-4-1106-preview"):
    msg = [{"role": "system", "content": system}, {"role": "user", "content": content}]
    #openai.api_key = '你的api'
    try:
        response = openai.chat.completions.create(
            model=model_type,
            messages=msg,
            extra_headers={"apikey": "你的api"},
            temperature=0.85,
            top_p=0.95
        )
        if response == None:
            return None
        else:
            reply_content = response.choices[0].message.content
            return reply_content
    except Exception as e:
        print(e)
        return None
    
MAX_ITERATION_EACH = 5

def score_reason_split(score_reason):
   if score_reason[1] == '0':
      return int(score_reason[:2]), score_reason[3:]
   else:
      return int(score_reason[:2]), score_reason[2:]


def fine_tune(Questions, stu_sys, stu_user, grader_sys, grader_user):
    answer_store = [[] for i in range(len(Questions))]
    for question_loc in range(len(Questions)):
        question = Questions[question_loc]
        his_answer = ""
        advice = ""
        for ite in range(MAX_ITERATION_EACH):
            cur_answer = gpt4_generate(system=stu_sys , content=stu_user.format(question=question, advice=advice, his_answer=his_answer))
            print("目前的答案是：", cur_answer)
            score_reason = gpt4_generate(system=grader_sys , content=grader_user.format(question=question, answer=cur_answer))
            #score, reason = score_reason_split(score_reason)
            answer_store[question_loc].append(cur_answer)
            his_answer = cur_answer
            advice = score_reason
            print("评分和评价是：", score_reason)
            input()
        print("针对第", question_loc, "个问题，回答变化是", answer_store[question_loc])


questions = ["Can I stay up past my bedtime tonight?",
             "Why do I have to go to school every day?",
             "Can I have a pet?",
             "How come adults get to drive cars but I can't?",
             "What's the point of homework?",
             "Can I have a sleepover with my friends this weekend?",
             "Why do I have to eat vegetables?",
             "Can I have a phone like my friends?",
             "How do airplanes stay in the sky?",
             "Why do I have to take a bath every day?"]

student_system_prompt = "You should act as a child age under 12. Answer the question below using language that fits who you are. Modify your answer according to advice to your history answer. Here is an example\n\
        Question: Do you like sweet\n\
        History Answer: I love it since it can provide us with energy.\n\
        Advice: children pay more attention to the taste of a video than how much energy it provides. The above answer is more like that of an adult exercising than a child.\n\
        Output: I love it since it tastes good!"
student_user_prompt = "Just output your answer, don't contain anythingelse.\nQuestion: {question}\n\
        Advice: {advice}\n\
        History Answer: {his_answer}"

grader_system_prompt = "Grade the answer with score between 0 and 10. Then give advice and analysis to generate a better answer. The closer the language of the answer is to the answering style of a 12-year-old child, the higher the score. Write your score and reason in the output. Here is an example: \
    Question: Do you like sweet?\n \
    Answer: I love it since it can provide us with energy.\n \
    output: 3. children pay more attention to the taste of a video than how much energy it provides. The above answer is more like that of an adult exercising than a child."
grader_user_prompt = "Question: {question} \n Answer: {answer}"


fine_tune(questions, student_system_prompt, student_user_prompt, grader_system_prompt, grader_user_prompt)
