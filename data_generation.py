# doel;
#   - data genereren dat bestaat uit; nodeNaam1, nodeNaam2, begintijd, eindtijd
# condities;
#   - data moet uniek zijn
#   - nodeNaam1 en nodeNaam2 mogen niet hetzelfde zijn
#   - begintijd moet kleiner zijn dan eindtijd
#   - nodeNaam1 en nodeNaam2 mogen elkaar niet meerdere keren in hetzelfde tijdpunt bellen

# stappen
# - node functies
  # - functie die 1 - N aantal nodes genereert
  # - functie die voor een node voor een random aantal keren contact met een node maakt
# - tijd-functies
  # - functie die een random begin tijd genereert, die niet al eens voorkomt voor deze node naar deze andere node
  # - functie die een random lengte van tijd genereert
  # - functie die een eindtijd berekent op basis van begintijd en lengte van tijd
# - functie die de data in een csv schrijft

# data example;
# nodeNaam1, nodeNaam2, begintijd, eindtijd
# 5, 7, 2409080630, 2405101140
# 7, 10, 209080630, 2402101140
# 7, 8, 2409080630, 1409101140
# 2405101140 = 2024-05-10 11:40:00

# libraries
import random
from datetime import datetime, timedelta
import csv


# limitations of data generation
random.seed(42)
num_nodes = 1000  # number of nodes was decides semi-arbitrarily, on average a node has 20 relations
num_calls = 20000
minimum_start_time = datetime(2024, 1, 1, 0, 0, 0)
maximum_start_time = datetime(2025, 1, 1, 0, 0, 0)


# functions
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
def create_fake_data(num_nodes, num_calls, minimum_start_time, maximum_start_time):
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


# export data to csv
def export_data_to_csv(data, filename):
  with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['nodeNaam1', 'nodeNaam2', 'begintijd', 'eindtijd'])
    for row in data:
      writer.writerow(row)
  print(f"Data exported to {filename}")


# generate fake data
raw_data = create_fake_data(num_nodes, num_calls, minimum_start_time, maximum_start_time)


# export data to csv
# csv_filename = 'small_test2_data.csv' # small test data of 50 records
csv_filename_20000 = 'full_data_20000.csv' # data of 20000 records, average of 20 relations per node
csv_filename_10000 = 'full_data_10000.csv' # data of 10000 records, average of 10 relations per node
csv_filename_5000 = 'full_data_5000.csv' # data of 5000 records, average of 5 relations per node
csv_filename_1000 = 'full_data_1000.csv' # data of 1000 records, average of 1 relations per node


export_data_to_csv(raw_data, csv_filename_20000)
export_data_to_csv(random.sample(raw_data, 10000), csv_filename_10000)
export_data_to_csv(random.sample(raw_data, 5000), csv_filename_5000)
export_data_to_csv(random.sample(raw_data, 1000), csv_filename_1000)
