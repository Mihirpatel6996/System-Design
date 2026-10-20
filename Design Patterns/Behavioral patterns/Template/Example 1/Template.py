"""
IN tmplate method what we do is we keep the pipeline steps fixed and variable steps are implemented in the child classes. This way we can avoid code duplication and make the code more maintainable and extensible.
"""

# base class / template owner 

from abc import ABC, abstractmethod


class ModelTrainer(ABC):

    # TEMPLATE METHOD (final-like behavior by convention)
    def train_pipeline(self, data_path):
        self.load_data(data_path) # for now this is a common step, but in future it can be overridden by child classes if needed
        self.preprocess_data()    # same with this step, for now this is a common step, but in future it can be overridden by child classes if needed. Note this is not an abstract method, so child classes are not forced to implement it. But they can override it if needed.
        self.train_model()        # must be implemented
        self.evaluate_model()     # must be implemented
        self.save_model()         # optional override

    # Common steps
    def load_data(self, path):
        print(f"[Common] Loading dataset from {path}")

    def preprocess_data(self):
        print("[Common] Splitting into train/test and normalizing")

    # Variable steps
    @abstractmethod
    def train_model(self):
        pass

    @abstractmethod
    def evaluate_model(self):
        pass

    # Hook / default implementation
    def save_model(self):
        print("[Common] Saving model in default format")



# lets define concrete classes -- Neural network 

class NeuralNetworkTrainer(ModelTrainer):

    def train_model(self):
        print("[NeuralNet] Training Neural Network for 100 epochs")

    def evaluate_model(self):
        print("[NeuralNet] Evaluating accuracy and loss")

    def save_model(self):
        print("[NeuralNet] Saving weights as .h5 file")


class DecisionTreeTrainer(ModelTrainer):

    def train_model(self):
        print("[DecisionTree] Building tree with max_depth=5")

    def evaluate_model(self):
        print("[DecisionTree] Computing precision/recall")

    # uses default save_model()



# Usage 

if __name__ == "__main__":
    print("=== Neural Network Training ===")
    nn = NeuralNetworkTrainer()
    nn.train_pipeline("data/images/")

    print("\n=== Decision Tree Training ===")
    dt = DecisionTreeTrainer()
    dt.train_pipeline("data/iris.csv")