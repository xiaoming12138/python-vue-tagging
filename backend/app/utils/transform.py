from settings import *
from langconv import *


results = table.find()
for res in results:
    context = res['context']
    new_context = Converter('zh-hans').convert(context)
    id = res['_id']
    item = table.find_one({"_id": id})
    table.update_one({"_id":id},{"$set":{'context':new_context}})
    print(new_context)
