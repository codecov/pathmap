import random
import time

from pathmap import (
    longest_common_substring,
    resolve_paths
)

 
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
    with open('tests/test_files/longfix.txt', 'r') as input_data:
        for line in input_data:
            if line.strip() == '<<<<<< network':
                break
            files.append(line.strip())
    return files

def main():
    toc = ','.join(get_file_fixture())
    print('Benchmark function: longest_common_substring')
    with Timer():
        longest = longest_common_substring('something/var/.htaccess', toc)
    mock_paths = [
        '../google/Auth/Abstract.php',
        'grid.phtml',
        'Entity/Attribute/Frontend/CardType.php'
    ]
    resolved = []
    print('Benchmark function: resolve_paths')
    with Timer():
        resolved = resolve_paths(toc, mock_paths)

    print(list([r for r in resolved]))
if __name__ == '__main__':
    main()
