import tkinter
import csv
import plotly as py

data = "student_1100_2018.csv"

first_line = True
index_title = {}
actions = {}
item = {}
parent = {}
file = {}
student = {}
sankey_data = {}
tier_flags = [0,0,0]

tier_1_links = ["Learning Pathway", "Learning Resources" ]

test_data_one = ["18/02/2018 15:22", "viewed home page", "", "", ""]
test_data_two = ["18/02/2018 15:24", "viewed content item", "document1", "documents", "something.pdf"]
test_data_three = ["18/02/2018 15:22", "viewed folder", "Learning Pathway"]

# function to store one row of clickstream data into a dictionary
# data_dict is the dictionary structure for storing all students data
# raw_data is a row of clickstream data to be stored
# the clickstream data must be in the format below
# timestamp, actions, item, parent item, file
def store_chrono(data_dict, raw_data):

    d_month = {}
    day_actions = []
    day, month, remain = raw_data[0].split('/')
    year, time = remain.split(' ')

    # checks if the current month has been recorded
    if data_dict.get(month):
        d_month = data_dict.get(month)
        # checks if current day has been recorded
        if d_month.get(day):
            day_actions = d_month.get(day)

    temp_data = raw_data[1:5]
    temp_data.insert(0, time)
    # removes the empty string from the list
    temp_data = list(filter(None, temp_data))
    day_actions.append(temp_data)
    d_month[day] = day_actions
    data_dict[month] = d_month
    return

# actual storing of data in structure
def sankey_insert(storage, item, parentitem):

    tier_1 = {}
    value = 0

    if storage.get(parentitem):
        tier_1 = storage.get(parentitem)
        if tier_1.get(item):
            value = tier_1.get(item)

    value += 1
    tier_1[item] = value
    storage[parentitem] = tier_1

    result = row
    return result


def sankey_build(storage, row):

    if (len(row) == 3):
        sankey_insert(storage, row[2], "top")

    elif (len(row) > 3):
        if "Week" in row[3]:
            temp = row[3][0:9]
            word = temp.split(' ')
            week = "Week" + word[1]

            sankey_insert(storage, week, "Learning Pathway")
            sankey_insert(storage, row[2], week)
        elif "Learning Resources" in row[3]:
            sankey_insert(storage, row[3], "top")
            sankey_insert(storage, row[2], row[3])
        # elif "Workshops" in row[3]:
        #     sankey_insert(storage, row[3], "Learning Resources")
        #     sankey_insert(storage, row[2], row[3])
        # elif "Lectures" in row[3]:
        #     sankey_insert(storage, row[3], "Learning Resources")
        #     sankey_insert(storage, row[2], row[3])
        # elif "Engineering101" in row[3]:
        #     sankey_insert(storage, row[3], "Learning Resources")
        #     sankey_insert(storage, row[2], row[3])

        else:
            sankey_insert(storage, row[3], "Learning Resources")
            sankey_insert(storage, row[2], row[3])


# function to create a sankey data structure from the dataset
def sankey_structure(storage, student_data):

    months = student_data.keys()
    month = "02"
    # for month in months:
    #     days = student.get(month).keys()
    days = student.get(month).keys()
    for day in days:
        s_actions = student.get(month).get(day)
        for action in s_actions:
            sankey_build(storage, action)
    return

# prints all the clickstream data of p_student
# prints in the format as below
# index, month, day, time and actions
def print_chrono(p_student):

    months = p_student.keys()
    index = 1

    print("{:5} {:5} {:5} {:5}".format("Index", "Month", "Day", "Actions"))
    for month in months:
        days = student.get(month).keys()
        for day in days:
            p_actions = student.get(month).get(day)
            for action in p_actions:
                print("{:^5} {:^5} {:^5} {}".format(index, month, day, action))
                index += 1
                # print(month, day, action)
    return

def sankey_array(storage):

    label = []
    colour = []
    source = []
    target = []
    value = []
    result = []

    keys = storage.keys()

    for key in keys:
        links = storage.get(key).keys()
        for link in links:
            size = storage.get(key).get(link)
            if key not in label:
                label.append(key)
                colour.append("blue")
            if link not in label:
                label.append(link)
                colour.append("blue")

            index_key = label.index(key)
            index_link = label.index(link)
            source.append(index_key)
            target.append(index_link)
            value.append(size)


    result.append(label)
    result.append(colour)
    result.append(source)
    result.append(target)
    result.append(value)
    return result


with open(data, 'Ur') as csv_file:

    data_reader = csv.reader(csv_file)

    for row in data_reader:

        # skips the header of the csv file
        if first_line:
            first_line = False
            continue

        actions[row[1]] = 0
        item[row[2]] = 0
        parent[row[3]] = 0
        file[row[4]] = 0

        store_chrono(student, row)

sankey_structure(sankey_data, student)
# sankey_build(sankey_data, test_data_three)
# sankey_build(sankey_data, test_data_two)
# sankey_build(sankey_data, test_data_two)
# print(sankey_data.keys())
result = sankey_array(sankey_data)
print(result)


# print_chrono(student)
# print("actions: " ,len(actions.keys()), "\n")
# print("item: ", len(item.keys()), "\n")
# print("parent: ", len(parent.keys()), "\n")
# print("file: ", len(file.keys()), "\n")

data_trace = dict(
    type ='sankey',
    width = 100,
    height = 100,
    domain = dict(
        x = [0,2],
        y = [0,2]
    ),
    orientation = "v",
    valueformat = ".0f",
    valuesuffix = "visits",
    node = dict(
      pad = 15,
      thickness = 15,
      line = dict(
        color = "black",
        width = 0.5
      ),
      label = result[0],
      color = result[1]
    ),
    link = dict(
      source = result[2],
      target = result[3],
      value = result[4]
  ))

layout =  dict(
    title = "Students clickstream traffic",
    font = dict(
      size = 10
    )
)

fig = dict(data=[data_trace], layout=layout)
py.offline.plot(fig, validate=False)

#424009 - 425821
