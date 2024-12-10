import os

def inputfile():
    return os.path.join(os.path.dirname(__file__), 'input.txt')

def getinput(f, test=False):
    test_input = ['2333133121414131402']   
    return test_input if test else f.read().splitlines()

def checksum(fs):
    # fs == [id0,....,idN]
    total = 0
    for idx, id in enumerate(fs):
        if id and id != '.':
          total += idx * int(id)
    return total

def build_file_list(fs):
    file_list, free_list, file_size_list, file_idx_list = [], [], [], []
    for idx, sz in enumerate(fs):
        sz = int(sz)
        if idx % 2 == 0:
            file_list.extend([idx//2 for _ in range(sz)])
            file_size_list.append(sz)
            file_idx_list.append(len(file_list)-sz)
        else:
            if sz:
                free_list.append((sz, len(file_list)))
            file_list.extend([None for _ in range(sz)])
    return file_list, free_list, file_size_list, file_idx_list

def available_space(file_size_list, free_list, id, max_idx):
    sz = file_size_list[id]
    for idx, (fsz, free_idx) in enumerate(free_list):
        if max_idx < free_idx:
            return None
        if sz <= fsz:
            return idx
        
def update_free_list(free_list, free_list_idx, decrement):
    entry_sz, entry_idx = free_list[free_list_idx]
    if entry_sz == decrement:
        free_list.pop(free_list_idx)
    else:
        free_list[free_list_idx] = (entry_sz - decrement, entry_idx + decrement)

def get_last_id(file_list):
    for e in reversed(file_list):
        if e:
            return e

def remove_file(file_list, file_id):
    while file_id in file_list:
        file_list[file_list.index(file_id)] = None

def add_file(file_list, file_size_list, id, file_list_idx):
    for i in range(file_size_list[id]):
        file_list[file_list_idx+i] = id

def defrag_a(file_list):
    while None in file_list:
        entry = file_list.pop(-1)
        if entry:
            file_list[file_list.index(None)] = entry

def defrag_b(file_list, free_list, file_size_list, file_idx_list):
    last_id = get_last_id(file_list)
    for id in range(last_id, 0, -1):
        max_idx = file_idx_list[id]
        free_list_idx = available_space(file_size_list, free_list, id, max_idx)
        if free_list_idx is None: continue
        _, file_list_idx = free_list[free_list_idx]
        update_free_list(free_list, free_list_idx, file_size_list[id])
        remove_file(file_list, id)
        add_file(file_list, file_size_list, id, file_list_idx)
    
with open(inputfile()) as f:
    input = getinput(f)[0]

    file_list_a, _, _, _= build_file_list(input)
    defrag_a(file_list_a)
    print('Part A: %i' % checksum(file_list_a))

    file_list_b, free_list, file_size_list,file_idx_list = build_file_list(input)
    defrag_b(file_list_b, free_list, file_size_list, file_idx_list)
    print('Part B: %i' % checksum(file_list_b))