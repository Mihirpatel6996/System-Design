# dulicate full pipeline everywhere

class NeuralNetworkTrainer:
    def train_pipeline(self, data_path):
        print(f"[Common] Loading dataset from {data_path}")
        print("[Common] Splitting and normalizing")

        print("[NeuralNet] Training for 100 epochs")
        print("[NeuralNet] Evaluating accuracy and loss")
        print("[NeuralNet] Saving model as .h5")

# these are just print statements to simulate the training process. In a real-world scenario, these would be replaced with actual data loading, preprocessing, model training, evaluation, and saving logic.


class DecisionTreeTrainer:
    def train_pipeline(self, data_path):
        print(f"[Common] Loading dataset from {data_path}")
        print("[Common] Splitting and normalizing")

        print("[DecisionTree] Building tree with max_depth=5")
        print("[DecisionTree] Computing precision/recall")
        print("[Common] Saving model to default format")


# as you can see, both classes have a lot of duplicated code in the train_pipeline method. The only difference is the specific training steps for each model. This violates the DRY (Don't Repeat Yourself) principle and makes it harder to maintain and extend the code in the future.

# Usage 

nn = NeuralNetworkTrainer()
nn.train_pipeline("data/images/")

print()

dt = DecisionTreeTrainer()
dt.train_pipeline("data/iris.csv")

# problems here

"""
1. tommorow there might be a changes in the pipeline, we will have to make changs in all the classes
2. what if someone changes the order of the steps in the pipeline, Ex training step before the data loading step very fragile and error prone
3.At scale 20 models and 20 dfferent pipelines, very hard to maintain and extend the code in the future.

"""