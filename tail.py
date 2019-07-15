import os
import argparse


def tail(file, n):
    # each time tries to read block_size from the end of file
    # check if the block read already has n lines
    # if not, read the block before that until we got n lines
    block_size = 256

    with open(file, "rb") as f:
        # find the length of file
        f.seek(0, os.SEEK_END)
        f_length = f.tell()

        blocks = []
        lines_found = 0
        offset = 0

        while -offset < f_length and lines_found < n:
            offset -= block_size
            # if offset is larger than file length, use the beginning of file instead
            if -offset > f_length:
                offset = -f_length

            # search backward and read 1 block
            f.seek(offset, os.SEEK_END)
            content = f.read(block_size)
            blocks.append(content)

            lines_found += content.decode("utf-8").count('\n')
            if lines_found < n:
                continue

        block = b''.join(blocks[::-1])
        lines = block.decode("utf-8").split('\n')
        print('\n'.join(lines[-n:]))
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num-of-lines", type=int, required=True,
                        help="How many lines do you want to tail")
    parser.add_argument("file_name", type=str,
                        help="Name of the file you want to tail")
    args = parser.parse_args()

    tail(args.file_name, args.num_of_lines)
