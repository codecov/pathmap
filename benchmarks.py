import random
import time

from pathmap.tree import Tree

from lcs import longest_common_substring

 
class Timer():
 
    def __init__(self):
        self.start = time.time()
 
    def __enter__(self):
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = 'The function took {time} seconds to complete'
        print(msg.format(time=runtime))


# ========== Fixtures ============
def get_file_fixture():
    files = []
    with open('tests/test_files/toc_benchmark.txt', 'r') as input_data:
        for line in input_data:
            files.extend(line.strip().split(','))
    return files

def main():
    toc = ','.join(get_file_fixture())
    tree = Tree()
    tree.construct_tree(toc)
    print('Benchmark Tree::find_longest_common')
    with Timer():
        longest = tree.find_longest_common('c:/projects/media-server/source/calldetailrecords/esncdr/esncdr.cpp')
        print(longest)

    print('Benchmark lcs::longest_common_substring')
    with Timer():
        longest = longest_common_substring('c:/projects/media-server/source/calldetailrecords/esncdr/esncdr.cpp', toc)
        print(longest)

if __name__ == '__main__':
    main()
