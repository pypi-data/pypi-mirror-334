from galamo import GalaxyMorph

# Initialize the classifier (update paths if necessary)
galaxy_classifier = GalaxyMorph(model_path="model.keras", encoder_path="../encoder.pkl")

# Test with a sample image
result = galaxy_classifier.predict("test.jpg")
print("Predicted Class:", result)
