'''
takes a binary table and produces a rarifaction curve
  args:
    argv[1]: filename
'''
from sys import argv
from collections import Counter

import csv
import random

import matplotlib.pyplot as plt

def read_csv_to_data(filename): #add errors
  with open(filename) as f:
    reader = csv.reader(f)
    header = next(reader)[1:]  # skip headers
    data = []
    for row in reader:
      genome = row[0]
      genes = set(g for g, val in zip(header, row[1:]) if val == '1')
      data.append((genome, genes))
  return data

def count_unique_genes(sample):
  richness_list = []
  all_genes = set()
  for _, gene_set in sample:
    all_genes.update(gene_set)
    richness_list.append(len(all_genes))
  avg_richness = sum(richness_list) / len(richness_list)
  return avg_richness

def count_singletons(sample):
  gene_sets = []
  # probably should combine these loops (see function above) but its not so slow...
  for _, gene_set in sample: 
    gene_sets.append(gene_set)
    counter = Counter()
  for s in gene_sets:
    counter.update(s)
  unique_values = {x for x in counter if counter[x] == 1}
  return len(unique_values)

def compute_rarefaction(matrix, max_n=None, steps=10, reps=100): #make argument when parser exists
  if max_n is None:
    max_n = len(matrix)
  if steps is None:
    steps = len(matrix) // 10

  step_size = max(1, max_n // steps)
  x_vals = list(range(1, max_n + 1, step_size))

  x_unique = []
  y_unique = []
  y_singletons = []
  
  for n in x_vals:
    for _ in range(reps):
      sample = random.sample(matrix, n)
      y_unique.append(count_unique_genes(sample))
      y_singletons.append(count_singletons(sample))
      x_unique.append(n)
  return x_unique, y_unique, y_singletons #, y_singletons

def plot_curve(x, y1, y2):
  fig, ax1 = plt.subplots(figsize=(8, 6))
  ax1.plot(x, y1, marker='o', linestyle='None', color='#1f77b4', label="unique genes")
  ax1.set_xlabel("Number of genomes sampled")
  ax1.set_ylabel("unique genes")

  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
  ax2.plot(x, y2, marker='o', linestyle='None', color ="#ff7f0e")
  ax2.set_ylabel("singletons")

  plt.title("Rarefaction Curve")
  plt.grid(True)
  plt.tight_layout()
  plt.savefig("rarefaction_curve.png", dpi=300)

def main(filename):
  data = read_csv_to_data(filename)
  x1_vals, y1_vals, y2_vals = compute_rarefaction(data)
  plot_curve(x1_vals, y1_vals, y2_vals)

filename = argv[1]
main(filename)


