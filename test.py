# define the DNA dictionary using binary keys
dna = {"00": "A", "01": "T", "10": "G", "11": "C"}

# define the DNA nucleotides using binary values
dna["A"] = [0, 0]
dna["T"] = [0, 1]
dna["G"] = [1, 0]
dna["C"] = [1, 1]

# use list comprehension and zip to simplify DNA xor
pairs = ["AA", "TT", "GG", "CC", "AG", "GA", "TC", "CT", "AC", "CA", "GT", "TG", "AT", "TA", "CG", "GC"]
for p in pairs:
    dna[p] = dna[p[0]][0] ^ dna[p[1]][0], dna[p[0]][1] ^ dna[p[1]][1]
    dna[p] = "A" if dna[p] == dna["00"] else "T" if dna[p] == dna["01"] else "G" if dna[p] == dna["10"] else "C"

print(dna)