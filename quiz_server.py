import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

ipaddr = "127.0.0.1"
port = 7500

server.bind((ipaddr,port))
server.listen()

list_of_clients = []

questions = [
    "What is the italian word for PIE? \n a. Mozarella\n b.Pasty \n c.Patty \n d.Pizza",
    "Water boils at 212 units at which scale? \n a. Fahrenhite\n b.Celsius \n c.Rankine \n d.Kelvin",
    "Which sea has three hearts? \n a. Dolphin\n b.Octopus \n c.Walrus \n d.Seal",
    "Who was the famous character in our childhood rhymes associate with a lamb \n a. Mary\n b.Jack \n c.Jonny \n d.Mukesh",
    "How many bones does a adult human have? \n a. 206\n b.208 \n c.201 \n d.196",
    "How many wonders are there in the world? \n a. 7\n b. 8\n c. 10\n d. 4",
    "Which element does not exist? \n a. Xf\n b. Re\n c. Si\n d. Pa",
    "How many states are there in India? \n a. 24\n b. 29\n c. 30\n d. 31",
    "Who invented the telephone? \n a. A.G Bell\n b. John Wick\n c. Thomas Edison\n d. G Marconi",
    "Who is Loki? \n a. God Of Thunder\n b. God Of Dwarves\n c. God Of Mischeif\n d. God Of Gods"
]

answers = ['d','a','b','a','a','a','a','b','a','c']

def get_random_question_answer(conn):
    randomindex = random.randint(0, len(questions) - 1)
    randomques = questions[randomindex]
    randomans = answers[randomindex]
    conn.send(randomques.encode('utf-8'))
    return randomindex, randomques, randomans

def remove(conn):
    if conn in list_of_clients:
        conn.remove()

def remove_ques(index):
    questions.pop(index)
    answers.pop(index)

def clientThread(conn):
    score = 0
    conn.send("Welcome to this quiz game".encode('utf-8'))
    conn.send("You will recive a question, the answer could be a/b/c/d\n".encode('utf-8'))
    conn.send("Good Luck\n \n".encode('utf-8'))
    index,question,answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send("Yay! Right Answer!\n".encode('utf-8'))
                else:
                    conn.send("Oops! Wrong Answer!\n".encode('utf-8'))
                remove_ques(index)
                index,question,answer = get_random_question_answer(conn)
            else:
                remove(conn)
        except:
            continue

while True:
    conn,addr = server.accept()
    list_of_clients.append(conn)

    new_thread = Thread(target= clientThread, args=(conn,addr))
    new_thread.start()