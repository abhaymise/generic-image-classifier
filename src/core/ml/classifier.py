import numpy as np
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import logging
import sys
logger = logging.Logger("classifier")
logging.basicConfig(stream=sys.stdout)

class SimilarityCalculator:
    @staticmethod
    def compute_similarity(image_features, text_features):
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity_scores = (image_features @ text_features.T).squeeze(0)
        return similarity_scores

class ProbabilityConverter:
    @staticmethod
    def to_probabilities(similarity_scores):
        return torch.softmax(similarity_scores, dim=-1).numpy()

class ZeroShotClassifier:
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        # Load the CLIP model and processor
        self.model_name = model_name
        self.__load_model()
        self.classes = []
        self.prompts = []

    def __load_model(self):
        model_name = self.model_name
        try:
            self.model = CLIPModel.from_pretrained(model_name,local_files_only=True)
            self.processor = CLIPProcessor.from_pretrained(model_name,local_files_only=True)
            print(f"model and processor loaded successfully ...")
        except Exception as e:
            print(f"Failed to load the model.{e}")

    def set_classes(self, classes):
        """
        Sets new classes and generates prompts based on the classes.
        Args:
            classes (list): A list of class labels (e.g., ["cat", "dog", "car"]).
        """
        self.classes = classes
        # Create prompts dynamically based on class labels
        self.prompts = [f"a photo of a {label}" for label in self.classes]
        print(f"Classes set to: {self.classes}")
        print(f"Prompts generated: {self.prompts}")

    def reset_classes(self):
        """Resets the classes and prompts to an empty state."""
        self.classes = []
        self.prompts = []
        print("Classes and prompts have been reset.")

    def classify_image(self, image_array):
        """
        Classifies an image based on the current set of prompts.
        Args:
            image_path (str): The file path of the image to classify.
        Returns:
            dict: Classification results with labels and their confidence scores.
        """
        if not self.prompts:
            raise ValueError("No classes have been set. Use set_classes() to define the classes "
                             "before classification.")

        # Load and preprocess the image
        inputs = self.processor(text=self.prompts, images=image_array, return_tensors="pt", padding=True, truncation=True)
        # Compute the embeddings and similarity scores
        with torch.no_grad():
            outputs = self.model(**inputs)
            image_features = outputs.image_embeds
            text_features = outputs.text_embeds

        similarity_scores = SimilarityCalculator.compute_similarity(image_features,text_features)
        # Convert similarity scores to probabilities
        probabilities = ProbabilityConverter.to_probabilities(similarity_scores)
        cls_idx = np.argmax(probabilities)
        # Prepare output with class labels and confidence scores
        results = [{"label": self.classes[i], "confidence": float(probabilities[i])} for i in range(len(self.classes))]
        prediction = results[cls_idx]
        print(f"Predicted class info :: {prediction}")
        results.sort(key=lambda x: x["confidence"], reverse=True)
        return {
            "prediction": prediction,
            "other_predictions": results,
            "model_name": self.model_name
        }

# Example usage
if __name__ == "__main__":
    # Initialize the classifier
    classifier = ZeroShotClassifier()

    # Set classes for classification
    classifier.set_classes(["biryani", "cake", "no-food"])
    # Classify an image
    image_path = "/Users/abhaykumar/Documents/datasets/food/images/test/biryani/biryani.jpg"  # Replace with the actual image path
    image = Image.open(image_path)
    image_array = np.array(image)
    results = classifier.classify_image(image_array)

    #Print the results
    print(results)

    # Reset classes
    classifier.reset_classes()
