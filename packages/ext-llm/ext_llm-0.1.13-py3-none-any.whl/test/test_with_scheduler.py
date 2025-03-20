import ext_llm
from ext_llm.scheduler import RequestScheduler

#read config yaml file
config : str = open("config.yaml").read()
#initialize extllm library
extllm = ext_llm.init(config)

llm_client = extllm.get_client("groq-llama")
scheduler = extllm.get_scheduler(llm_client, max_workers=10)

scheduler.start()
requests=[]
requests_amount=50
for i in range(requests_amount):
    requests.append(scheduler.submit_request("you are a helpful assistant",
                                       "What is the capital of France?",))
    #print("Request", i, ":", scheduler.get_result(request))

for i in range(requests_amount):
    print("Request", i, ":", scheduler.get_result(requests[i]))

scheduler.stop()