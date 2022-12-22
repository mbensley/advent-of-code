def get_marker_index(datastream: str, size: int) -> int:
  data_list = list(datastream)
  for i in range(len(data_list)):
    if len(set(data_list[i:i + size])) == size:
      return i + size
  return -1


def get_input() -> str:
  with open('input.txt', 'r') as f:
    return f.readline().strip()


def main():
  test_input = [
    'bvwbjplbgvbhsrlpgdmjqwftvncz', 'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
  ]
  real_input = get_input()
  for entry in test_input:
    print(entry + ':' + str(get_marker_index(entry, 4)))
  print(get_marker_index(real_input, 4))

  test_input = ['mjqjpqmgbljsphdztnvjfqwrcgsmlb']
  for entry in test_input:
    print(entry + ':' + str(get_marker_index(entry, 14)))
  print(get_marker_index(real_input, 14))


main()