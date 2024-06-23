from worker import start_automl

def main():
    model = start_automl.delay("../data/boston_housing/Boston_dataset_Train_data.csv", "medv").get()
    print(model)
    
if __name__ == '__main__':
    main()