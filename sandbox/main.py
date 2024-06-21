from tasks import add

def main():
    result = add.delay(4, 4).get()
    print(result)
    
if __name__ == '__main__':
    main()