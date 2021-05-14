import sys
import dinger

def main(file_name):
    dinger.fit(file_name)

if __name__ == "__main__":
    args = sys.argv[1:]
    file_name = sys.argv[0]
    main(file_name)
