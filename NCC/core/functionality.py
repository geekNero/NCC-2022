import subprocess 
import time
import shutil
from .models import *
signals = {
    1: "CTE",
    2: "CTE",
    127: "CTE",
    132: "RE",
    133: "RE",
    134: "RE",
    136: "RE",
    137: "TLE",
    138: "MLE",
    139: "RE",
    158: "TLE",
    152: "TLE",
    159: "MLE",
    153: "MLE",
}
def find_container():
    container=0
    while(len(list(Container.objects.filter(status=False)))==0):
        time.sleep(5)
    container=list(Container.objects.filter(status=False))[0]
    container.status=True
    container.save()
    return container

def swap_code(container,code,language,time_limit,memory_limit):
    dest=f"containers/{container.name}/sub.py"
    path=""
    with open(dest,'a') as sub:
        if(language=="python"):
            path="code.py"
            sub.write(f'py({time_limit},{memory_limit})')
        elif(language=="c++"):
            path="code.cpp"
            sub.write(f'cpp({time_limit},{memory_limit})')
        else:
            path="code.c"
            sub.write(f'c({time_limit},{memory_limit})')
    dest=f"containers/{container.name}/{path}"
    with open(dest,'w+') as op:
        op.write(code)

def get_sub(container):
    origin="sub.py"
    dest=f"containers/{container.name}/sub.py"
    shutil.copyfile(origin,dest)

def swap_input(container,path,input):
    inp=f'containers/{container.name}/input.txt'
    if(path):
        shutil.copyfile(input,inp)
    else:
        with open(inp,"w+") as i:
            i.write(input)

def swap_output(container,path,output):
    samp_op=f'containers/{container.name}/sam_output.txt'
    if(path):
        shutil.copyfile(output,samp_op)
    else:
        with open(samp_op,"w+") as o:
            o.write(output)

def returnContainer(container):
    container.status=False
    container.save()

def get_returnCode(container):
    returnCode=0
    with open(f'containers/{container.name}/return_code.txt','r') as ret:
        returnCode=ret.read()
    returnCode=returnCode.strip()
    returnCode=int(returnCode)
    return returnCode

def get_Error(container):
    error=""
    with open(f'containers/{container.name}/error.txt','r') as err:
        error=err.read()
    return error

def get_Output(container):
    op=""
    with open(f"containers/{container.name}/output.txt") as file_1:
        op=file_1.read()    
    return op

def run_code(code,language,qid):
    container=find_container()
    qid=Question.objects.get(pk=qid)
    get_sub(container)
    swap_code(container,code,language,qid.time_limt,qid.memory_limit)
    test_ops=[]
    error=0
    for test in testcase.objects.filter(q_id=qid):
        swap_input(container,True,test.tc_input.path)
        swap_output(container,True,test.tc_output.path)
        execute(container)
        returnCode=get_returnCode(container)
        error=get_Error(container)
        test_ops=[]
        print("Return COde : ",returnCode)
        if(returnCode!=0):
            try:
                if(returnCode<0):
                    returnCode=128-returnCode
                test_ops.append(signals[returnCode])
            except:
                test_ops.append("Unknown Error")
            break
        else:
            test_ops=[]
            result=comapare(container)
            if(result):
                test_ops.append('Passed')
            else:
                test_ops.append('WA')
    returnContainer(container)
    return test_ops,error


def execute(container):
    command=f"sudo docker exec {container.name} python3 src/sub.py"
    a=subprocess.run(command,shell=True,text=True)

def run_container():
    subprocess.run('bash docker_scripts/run.sh',shell=True)

def create_container():
    subprocess.run('bash docker_scripts/create.sh',shell=True,text=True)
    for i in range(1,11):
        Container.objects.get_or_create(name=f"NCC-Container-{i}",status=False)
def comapare(container):
    with open(f"containers/{container.name}/output.txt") as file_1:
        file_1_text = file_1.readlines()
    with open(f"containers/{container.name}/sam_output.txt") as file_2:
        file_2_text = file_2.readlines()
    index = 0
    result = True
    if len(file_2_text) > len(file_1_text):
        result = False
    else:
        for line in file_2_text:
            line1 = file_1_text.pop(0)
            line = line.rstrip()
            line1 = line1.rstrip()
            if len(line) != len(line1):
                result = False
            else:
                for index in range(len(line)):
                    if line[index] != line1[index]:
                        result = False
        for line in file_1_text:
            line = line.split()
            if len(line) > 0:
                result = False
    return result

def run_updates(pk,test_ops,error,user,code,language):
    status="NA"
    qscore=Question.objects.get(pk=pk)
    total=len(testcase.objects.filter(q_id=qscore))
    if(test_ops[-1]=="Passed" and len(test_ops)==total):
        data,created=Question_Status.objects.get_or_create(q_id=qscore,p_id=user)
        status="AC"
        if(created or data.score==0):
            data.score=qscore.score-data.penalty
            user.total_score+=data.score
            data.penalty=0
            data.status="AC"
            qscore.score-=1
            data.save()
            qscore.save()
    else:
        status=test_ops[-1]
        data,created=Question_Status.objects.get_or_create(q_id=qscore,p_id=user)
        data.penalty+=10
        if(created or data.score==0):
            data.status=test_ops[-1]
        for i in range(len(test_ops),total):
            test_ops.append('Locked')
        data.save()
    print(status)
    sub=Submission(q_id=qscore,p_id=user,code=code,language=language,status=status)
    sub.save()
    user.save()
    return test_ops,error

def custom(code,language,input):
    container=find_container()
    get_sub(container)
    swap_code(container,code,language,1,256)
    swap_input(container,False,input)
    execute(container)
    output=get_Output(container)
    error=get_Error(container)
    if(len(error)):
        output=""
    returnContainer(container)
    return output,error