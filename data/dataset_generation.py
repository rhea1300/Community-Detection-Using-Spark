# libraries
import random
from datetime import datetime, timedelta
import csv
import sys


# set immutable variables for data generation
random.seed(42)
minimum_start_time = datetime(2024, 1, 1, 0, 0, 0)
maximum_start_time = datetime(2025, 1, 1, 0, 0, 0)
print(sys.getrecursionlimit())
sys.setrecursionlimit(10000000)
print(sys.getrecursionlimit())


# functions for generating data
# generate start & end datetime
def random_start_datetime(start, end):
  start_datetime = start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
  
  # check if start_datetime is not after end datetime, if so rerun the function
  if start_datetime >= end:
    start_datetime = random_start_datetime(start, end)

  return start_datetime

def random_end_datetime(start, end):
  # call time between 1 minute and 8 hours after start time
  end_datetime = start + timedelta(seconds=random.randint(60, 28800)) 

  # check if end_datetime is not after end datetime, if so rerun the function
  if end_datetime >= end:
    end_datetime = random_end_datetime(start, end)

  return end_datetime

# create fake data
def create_fake_data(num_nodes, num_avg_calls, minimum_start_time, maximum_start_time):
  num_calls = num_nodes * num_avg_calls

  nodes = list(range(1, num_nodes + 1))
  fake_data = []

  # keep track of ongoin calls between nodes for overlap
  # use a dictionary of lists, of which the key is the node1 number and the value is list of tuples of (node2, start, end)
  ongoing_calls = {node: [] for node in nodes}

  for _ in range(num_calls):
    # pick 2 random nodes that are not the same
    node1, node2 = random.sample(nodes, 2)
    # ensure that the random nodes are in ascending order, makes checking for overlap easier
    node1, node2 = sorted([node1, node2])

    # generate random start and end time
    call_start = random_start_datetime(minimum_start_time, maximum_start_time)
    call_end = random_end_datetime(call_start, maximum_start_time)

    # check that node1 and node2 arent overlapping a ongoin call between the two
    overlap = False
    for (node, start, end) in ongoing_calls[node1]:
      if node == node2:
        if not ((call_end <= start) or (call_start >= end)):
          overlap = True
          break

    # add call to data and ongoing calls
    if not overlap:
      fake_data.append((node1, node2, call_start.strftime('%Y%m%d%H%M%S'), call_end.strftime('%Y%m%d%H%M%S')))
      ongoing_calls[node1].append((node2, call_start, call_end))

  return fake_data


# functions for saving dataset
def create_dataset_name(size, avg_relations, additional_info=""):
  return f"{additional_info}_data_{size}_{avg_relations}.csv"

def save_dataset(filename, dataset):
  with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['nodeNaam1', 'nodeNaam2', 'begintijd', 'eindtijd'])
    for row in dataset:
      writer.writerow(row)


# function to generate multiple datasets and save them
def generate_save_multiple_datasets(list_sizes, list_avg_relations, additional_info=""):
  for size in list_sizes:
    for avg_relations in list_avg_relations:
      dataset = create_fake_data(size, avg_relations, minimum_start_time, maximum_start_time)
      filename = create_dataset_name(size, avg_relations, additional_info)
      save_dataset(filename, dataset)
      print(f"Data generated and saved to {filename}")
  

# dataset variations  
dataset_sizes = [3000, 5000, 10000, 15000, 20000, 30000]
dataset_avg_relations = [3, 5, 10, 15, 20]


# generate datasets for avg relations, default size is 50000
# generate_save_multiple_datasets([20000], dataset_avg_relations, "data/size20k")


# generate datasets for sizes, default avg relations is 20
generate_save_multiple_datasets(dataset_sizes, [10], "data/avgRela10")