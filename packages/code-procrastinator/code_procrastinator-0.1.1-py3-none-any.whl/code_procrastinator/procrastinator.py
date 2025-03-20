import time, random


def excuse_wrapper(func):
    def wrapper(x, y):
        # Initial Message
        init_messages = ["Alright, let's get started!", "Preparing to output solution...", 
                         "Optimizing best possible answer"]
        print(random.choice(init_messages))
        time.sleep(5)
        print("Processing... 25% done.")
        time.sleep(2)
        print("Still thinking... 50% done.")
        time.sleep(3)

        # Excuse Message
        excuse_messages = ["Almost done! Just need a little more time...", 
                           "Wait, I just realized there's a better way to do this... let me rethink everything.",
                            "Someone just deleted my work... I need to start over again..."
                           ]
        print(random.choice(excuse_messages))
        time.sleep(5)

        # Ending Message
        end_message = ["Ok done!", "TBH... forget this I'll do it tomorrow."]
        res = random.randint(0, 1)
        if res == 0:
            print(end_message[0])
            time.sleep(1)
            return func(x, y)
        else:
            print(end_message[1])
    return wrapper