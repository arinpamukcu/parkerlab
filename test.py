# alldata = []
# for dose in doses:
#     for drug in drugs:
#         data = get_stats(drug, dose)
#         if dose = 'vehicle':
#             alldata.append(data)
#         else:
#             m=mean(data)
#             s=sem(data)
#             bar(m,s)
#         m=mean(alldata)
#         s=sem(alldata)
#         bar(m,s)
#
# for dose in doses:
#     for drug in drugs:
#         data = get_stats(drug, dose)
#         if dose = 'vehicle':
#             alldata.append(data)
#         else:
#             for val in data.keys():
#                 m=mean(data[val])
#                 s=sem(data[val])
#                 bar(m,s)
#         m=mean(alldata)
#         s=sem(alldata)
#         bar(m,s)
#
# data['acc']=[]
# data['speed']=[]
# for val in data.keys():
#     alldata[val]=data[val]+data[val]
# for val,i in ennumerate(data.keys()):
#     subplot(i)
#     bar(m,s)
#     title(val)

# drug = clo, hal, mp10, ola
# dose = veh, low, high
# metric = event rate for (nospeed, lospeed, medspeed, hispeed, L turn, straight, R turn, acc, dec, constant, groom, rear)