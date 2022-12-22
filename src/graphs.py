import sys


def main(args):
    try:
        pass
    except Exception as ex:
        print(ex)
    return 1


if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(main(sys.argv[1:]))
