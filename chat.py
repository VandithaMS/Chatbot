import json
import torch
from model import NeuralNet
from nltk_utils import tokenize,stem,bag_of_words
from train import data
from date import date, times
from sql import query, fetch
from schedule import arr

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('data.json', 'r') as f:
    intent=json.load(f)

FILE ="output.pth"
# with open('data.json', 'r') as f:
#     data=torch.load(FILE)

input_size=data["input_size"]
hidden_size=data["hidden_size"]
output_size=data["output_size"]
all_words=data["all_words"]
tags=data["tags"]
model_state=data["model_state"]

model =NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def details():
    name=input("Enter your name: ")
    while True:
        phone=input("Enter your phone number(10 numbers): ")
        if phone.isdigit() and len(phone)==10:
            break
    addr=input("Enter your address: ")
    print(f"{bot_name}: {intent['intents'][0]['responses'][1]}")
    return name, phone, addr

bot_name="Jax"
print("Welcome!\nEnter 'q' to exit..")
name, phone, addr=details()
while True:
    sentence=input('You: ')
    if sentence == "q":
        break
    s=sentence
    sentence=tokenize(sentence)
    x=bag_of_words(sentence,all_words)
    x.reshape(1,x.shape[0])
    x=torch.from_numpy(x)

    output=model(x)
    _, predicted = torch.max(output, dim=0)
    tag = tags[predicted.item()]

    probs=torch.softmax(output,dim=0)
    # print(probs)
    # print(predicted.item())
    # l=probs[0]
    # print(l)
    prob=probs[predicted.item()]

    if prob.item() > 0.75:

        if tag == "slot":
                slot = date(s)
                if slot:
                    t=times(s)
                    while not t:
                        t=input("At What time you want? ")
                        t=times(t)
                    res=query(f"INSERT INTO list(name,phone,addr,date,time) VALUES('{name}','{phone}','{addr}','{slot}','{t}')")
                    if res is True:
                        print(f"{bot_name}: {intent['intents'][3]['responses'][0]} on {slot} at {t}")
                    else:
                        l=arr(slot,t)
                        print(f"{bot_name}: Sorry cannot book appointment!!... That slot has been booked.")
                        if len(l)>0:
                            for i in range(len(l)):
                                print(f"    {i+1}. {str(l[i])}")
                            i=input((f"{bot_name}: These slots are free.. \n   If you want to schedule enter the number: "))
                            if i.isdigit() and int(i)-1 in range(len(l)):
                                res=query(f"INSERT INTO list(name,phone,addr,date,time) VALUES('{name}','{phone}','{addr}','{slot}','{l[int(i)-1]}')")
                                if res:
                                    print(f"{bot_name}: {intent['intents'][3]['responses'][0]} on {slot} at {l[int(i)-1]}")

                else:
                    print(f"{bot_name}: {intent['intents'][3]['responses'][1]}")

        elif tag == "cancel":
            res=fetch(f"SELECT date,time FROM list WHERE name='{name}'AND phone='{phone}' AND addr='{addr}'")
            if len(res)>0:
                print(f"{bot_name}: You have appointment(s) on: ")
                for i in range(len(res)):
                    print("   "+str(i+1)+". "+str(res[i][0])+", "+str(res[i][1]))
                i=int(input(f"{bot_name}: Which appointment you want to remove? (Enter number) "))
                if i in range(1,len(res)):
                    rem=query(f"DELETE FROM list WHERE date='{res[i-1][0]}' AND time='{res[i-1][1]}'")
                    if rem:
                        print(f"{bot_name}: Your appointment has been cancelled!")
                    else:
                        print(f"{bot_name}: Sorry couldn't cancel your appointment... Retry")
                else:
                    print(f"{bot_name}: Enter the number properly")

            else:
                print(f"{bot_name}: You don't have any appointment scheduled")

        elif tag == "detail":
            res=fetch(f"SELECT name,date,time FROM list WHERE phone='{phone}'")
            if len(res)>0:
                print(f"{bot_name}: You have appointment(s) on: ")
                for i in range(len(res)):
                    print("   "+str(i+1)+". "+str(res[i][0])+", "+str(res[i][1])+", "+str(res[i][2]))
                    ppl=fetch(f"SELECT COUNT(*) FROM list WHERE date='{res[i][1]}' AND time<'{res[i][2]}'")
                    print(f"    At present {ppl[0][0]} people are before you!..")
            else:
                print(f"{bot_name}: You don't have any appointment scheduled")

        elif tag=="goodbye":
            print(f"{bot_name}: Thank You!")
            break

        else:
            for i in intent['intents']:
                if tag == i['tag']:
                    print(f"{bot_name}: {i['responses'][0]}")
    
    else:
        print(f"{bot_name}: Not understood..")
