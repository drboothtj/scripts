'''
takes a binary table and produces a rarifaction curve
  args:
    argv[1]: filename
'''
from sys import argv
import csv
import random
import matplotlib.pyplot as plt

def read_csv_to_data(filename): #add errors
  with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)[1:]  # skip "Genome", keep gene names
    data = []
    for row in reader:
      genome = row[0]
      genes = set(g for g, val in zip(header, row[1:]) if val == '1')
      data.append((genome, genes))
  return data
  
def compute_rarefaction(matrix, max_n=None, steps=None, reps=100):
  if max_n is None:
    max_n = len(matrix)
  if steps is None:
    steps = len(matrix)

  step_size = max(1, max_n // steps)
  x_vals = list(range(1, max_n + 1, step_size))
  y_vals = []
  new_x_vals = []
    
  for n in x_vals:
    richness_list = []
    for _ in range(reps):
      sample = random.sample(matrix, n)
      all_genes = set()
      for _, gene_set in sample:
        all_genes.update(gene_set)
        richness_list.append(len(all_genes))
      avg_richness = sum(richness_list) / len(richness_list)
      y_vals.append(avg_richness)
      new_x_vals.append(n)
  return new_x_vals, y_vals

def plot_curve(x, y):
  print(x,y)
  plt.plot(x, y, marker='o')
  plt.xlabel("Number of genomes sampled")
  plt.ylabel("Average number of unique genes")
  plt.title("Rarefaction Curve")
  plt.grid(True)
  plt.savefig("rarefaction_curve.png", dpi=300)

def main(filename):
  data = read_csv_to_data(filename)
  x_vals, y_vals = compute_rarefaction(data)
  plot_curve(x_vals, y_vals)

filename = argv[1]
main(filename)


