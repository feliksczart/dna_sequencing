def pairUp(reads):
  pairs = []
  reversed_pairs = []

  for i in range(len(reads)):
    for j in range(len(reads)):

      if (j == i):
        continue

      pairs.append([reads[i],reads[j]])
      reversed_pairs.append([reads[j],reads[i]])

    return pairs, reversed_pairs
