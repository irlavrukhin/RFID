import random

Tquery = 1
Tqrep = 1
T1 = 1
T2 = 1
T3 = 1
Trn16 = 1
Tack = 1
Tresponse = 1
model_time = 0
round_n = 0
Ncollison = 0
round_N = 1
K = 4
Q = 3
Nreads = [0] * K
probability_rn16 = 0.7
probability_response = 0.7


while round_n < round_N:

    reader_slot = 0
    while reader_slot < 2 ** Q:



        # <-- Here the slot starts, reader is sending Query or QueryRep,
        #     tags select random slots for responding
        if reader_slot == 0:
            model_time += Tquery

            # Selecting random slots for responding
            tag_slots = []
            for i in range(0, K):
                tag_slots.append(random.randrange(0, 2 ** Q, 1))
        else:
            model_time += Tqrep

        # Check which tags are going to respond in current slot
        replying_tags = []
        for i in range(0, len(tag_slots)):
            if tag_slots[i] == 0:
                replying_tags.append(i)

        print("Slot #{}: tag slots: {}, replying tags: {} ".format(reader_slot, tag_slots, replying_tags))

        # Checking how many tags are going to respond
        ntags = len(replying_tags)

        rand_prob_rn16 = random.uniform(0, 1)
        rand_prob_response = random.uniform(0, 1)

        if ntags == 0:
            model_time += T3

        elif ntags == 1:

            if rand_prob_rn16 < probability_rn16:
                #Imitation send ACK
                model_time += Tack + T1 + Tresponse + T2

                if rand_prob_response < probability_response:
                    for i in replying_tags:
                        Nreads[i] += 1

        else:
            Ncollison += 1

        # <-- Here the slot ends. Decrement the number of slots till response (tag_slots),
        #     increment the main slot counter (reader_slot)
        reader_slot += 1
        for i in range(0, len(tag_slots)):
            tag_slots[i] -= 1

        print("rand_prob_rn16: {}, rand_prob_response: {} Nreads: {}".format(rand_prob_rn16, rand_prob_response, Nreads ))
    else:
        round_n += 1
