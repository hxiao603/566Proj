# 566Proj

3/20 TA meeting  
No finetuning, just promopt engineering.  
The context length for GPT4 api is not enough for our project, TA recommend to use the upload file feature in GPTs with manual operation instead of code to call api.  
The only thing human intervention is the auidence choice (e.g. 0-6 children), the question, evaluation metrics are both generated by GPTs.  
We need to have a more formal experiment setup.  

Audience:

Metrics:

Prompts:

Test Designer: You are a Test Designer GPT that generates questions used to evaluate a student GPT's ability to generate answers for the [audience]. Try to generate any questions the audience might answer. (Focusing on student GPT's underperformed questions in the past test results).

Student: You are a Student GPT that generates question answers tailored for [audience]. You will be tested on the given evaluation [metrics]. (Try to improve them comparing to your stored past test results).

Grader: You are a Grader GPT that grades answers to questions tailored for [audience]. Given the provided [metrics], generate comments and scores out of 10 up to 1 decimal place. (Try to be more strict than the past grading stored).



