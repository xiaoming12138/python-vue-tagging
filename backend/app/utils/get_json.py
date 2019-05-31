from settings import *
import json

condition = {"is_labeled": True}
data = []
out = {}
results = table.find()
res_num = 0
qa_id = 0
for reslut in results:
    title = reslut['title']
    title_md5 = reslut['title_md5']
    index = reslut['index']
    context = reslut['context']
    question_answers = reslut['question_answer']
    qas = []
    res_num += len(question_answers)
    for question_answer in question_answers:
        qas.append({
            "answers": [{
                "answer_start": question_answer["start"],
                "text": question_answer['answer'],
            }],
            "question": question_answer["question"],
            "question_id": qa_id
        })
        qa_id += 1
    if not title_md5 in out:
        out.update({
            title_md5: {
                "title": title,
                'paragraphs': [{
                    "index": index,
                    "context": context,
                    "qas": qas
                }]
            }
        })
    else:
        out[title_md5]['paragraphs'].append({
            "index": index,
            "context": context,
            "qas": qas
        })

for item in out:
    data.append(out[item])

ans = {"data": data}
print(res_num)
f = open("labeled.json", "w+")
json.dump(ans, f, ensure_ascii=False, indent=2)
