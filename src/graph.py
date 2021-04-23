def pairUp(reads,min_overlap):
  pairs = []
  reversed_pairs = []

  for i in range(len(reads)):
    for j in range(len(reads)):

      if (j == i):
        continue
      
      r1, r2 = reads[i], reads[j]

      if (calculate_overlap(r1,r2) >= min_overlap):
        pairs.append([r1,r2])

      if (calculate_overlap(r2,r1) >= min_overlap):
        reversed_pairs.append([r2,r1])

  return pairs, reversed_pairs

def calculate_overlap(r1,r2):
  
  overlap = 0
  l = len(r1)

  for i in range(l):
    if r1 == r2:
      overlap = len(r1)
      break

    r1 = r1[1:]
    r2 = r2[:-1]

  return overlap