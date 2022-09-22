import subprocess 
import time
import shutil
from unittest import TestCase, result
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
def run_code(code,language,qid):
    container=0
    while(len(list(Container.objects.filter(status=False)))==0):
        time.sleep(5)
    container=list(Container.objects.filter(status=False))[0]
    container.status=True
    container.save()
    origin="sub.py"
    dest=f"containers/{container.name}/sub.py"
    shutil.copyfile(origin,dest)
    path=""
    with open(dest,'a') as sub:
        if(language=="python"):
            path="code.py"
            sub.write('py()')
        elif(language=="c++"):
            path="code.cpp"
            sub.write('cpp()')
        else:
            path="code.c"
            sub.write('c()')
    dest=f"containers/{container.name}/{path}"
    with open(dest,'w+') as op:
        op.write(code)
    test_ops=[]
    for test in testcase.objects.filter(q_id=qid):
        inp=f'containers/{container.name}/input.txt'
        samp_op=f'containers/{container.name}/sam_output.txt'
        shutil.copyfile(test.tc_input.path,inp)
        shutil.copyfile(test.tc_output.path,samp_op)
        execute(container)
        returnCode=0
        error=""
        test_ops=[]
        with open(f'containers/{container.name}/return_code.txt','r') as ret:
            returnCode=ret.read()
        with open(f'containers/{container.name}/error.txt','r') as err:
            error=err.read()
        returnCode=returnCode.strip()
        returnCode=int(returnCode)
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
    container.status=False
    container.save()
    return test_ops,error
def execute(container):
    command=f"sudo docker exec {container.cid} python3 src/sub.py"
    a=subprocess.run(command,shell=True,text=True)
def run_container():
    command= "sudo docker restart "
    for c in Container.objects.all():
        cid=0
        a=subprocess.run(command+c.cid,capture_output=True,shell=True,text=True)
        c.save()
def create_container():
    if(len(Container.objects.all())==0):
        subprocess.run('bash create.sh',shell=True,text=True)
        with open('containers/container.txt','r') as lst:
            lines=lst.readlines()
            for i in range(1,len(lines),2):
                obj=Container(name=(lines[i-1]).strip(),cid=(lines[i]).strip(),status=False)
                obj.save()
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
