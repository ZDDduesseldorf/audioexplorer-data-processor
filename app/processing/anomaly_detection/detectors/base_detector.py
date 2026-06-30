from abc import ABC, abstractmethod

# Import ABC (Abstract Base Class) and abstractmethod to create an abstract parent class.

# ABSTRACT BASIS CLASS
# MUST BE IMPLEMENTED BY OTHER DETECTORS


# Define an abstract base class for all anomaly detectors.
class BaseDetector(ABC):
    # Mark this method as abstract, forcing all subclasses to implement it.
    @abstractmethod

    # Define a method that should train the detector
    # and return prediction results.
    def fit_predict(self, embeddings):

        # Placeholder implementation.
        # Subclasses must provide their own logic.
        pass
