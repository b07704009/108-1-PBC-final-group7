dict = dict()
while True:
    article = input()
    while article != "BREAK":
        for word in range(len(article)-2):
            key = article[word] + '_' + article[word+2]
            if key not in dict:
                dict[key] = 1
            else:
                dict[key] += 1
        break

    while article == 'BREAK':
        answer = []
        length = len(dict.keys())
        for times in range(length):
            big_num = 0
            for keys in dict:
                if dict[keys] >= big_num:
                    big_num = dict[keys]
                    big_keys = keys
            answer.append([big_num, big_keys])
            del dict[big_keys]
        # print(answer)
        finalans = []
        namelist = []
        for i in range(length-1):
            if answer[i][0] > answer[i+1][0]:
                finalans.append(answer[i])
                finalans += namelist
                namelist = []

            elif answer[i][0] == answer[i+1][0]:
                namelist.append(answer[i][1])
        for i in range(10):
            if type(finalans[i]) == list:
                print(finalans[i][1], finalans[i][0])
            elif type(finalans[i]) == str:
                print(finalans[i], finalans[i-1][0])

        exit()
