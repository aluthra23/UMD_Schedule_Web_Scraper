import plexe
import pandas as pd

df = pd.read_csv('cs_courses.csv')

# Define the model
model = plexe.Model(
    intent="Predict sentiment from news articles",
    input_schema={"headline": str, "content": str},
    output_schema={"sentiment": str}
)

# Build and train the model
model.build(
    datasets=[df],
    provider="openai/gpt-4o-mini",
    max_iterations=10
)

# Use the model
prediction = model.predict({
    "headline": "New breakthrough in renewable energy",
    "content": "Scientists announced a major advancement..."
})

# Save for later use
plexe.save_model(model, "sentiment-model")
loaded_model = plexe.load_model("sentiment-model.tar.gz")
