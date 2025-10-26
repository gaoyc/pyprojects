import sys
import concurrent.futures

seasons = ['Spring', 'Summer', 'Fall', 'Winter']
list(enumerate(seasons))

# 结果为: [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]

list(enumerate(seasons, start=1))       # 小标从 1 开始

# 结果为: [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

#普通的 for 循环
i = 0
seq = ['one', 'two', 'three']
for element in seq:
    print(i, seq[i])
    i += 1


# for 循环使用 enumerate
seq = ['one', 'two', 'three','four', 'five']
for i, element in enumerate(seq):
    print(i, element)


def dealbatch(batchdata):
    reqdata = ''
    for data in batchdata:
        reqdata += (data+"\n")
    print("bulk req\n"+reqdata)

bulksike=3
nthreads=2
with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
    onebatch = []
    futures = []
    for i,data in enumerate(seq):
        print(data)
        onebatch.append(data)
        if len(onebatch) == bulksike:
            futures.append(executor.submit(dealbatch(onebatch)))
            onebatch.clear()
        # futures = executor.submit(print(), data):
    # 最后一批
    if len(onebatch) > 0:
        futures.append(executor.submit(dealbatch(onebatch)))
    for result in concurrent.futures.as_completed(futures):
                pass


docid = 1
vector = [1,3,4]
esbody = {
    'index': {
        "_id": docid,
        'id': docid,
        'vector': vector
    }
}


# esbody = '{"index": {"_id": "'+ docid +'", "id": '+docid+', "vector": '+vector+'}}\n'
# esbody += esbody
print(str(esbody))

print(str(esbody) +"\n"+ str(esbody))




"""
PUT my-index-000001/_doc/1
{
  "my_text" : "text1",
  "my_vector" : [0.5, 10, 6]
}
"""