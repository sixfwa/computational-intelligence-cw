from tools import load_data

train_data, train_targets = load_data("cwk_train")

print(list(train_data[0]))
for i in range(len(train_data)):
    print(list(train_data[i]))
