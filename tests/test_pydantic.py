from pydantic import BaseModel

class TestModel(BaseModel):
    name: str
    age: int

# Create a test instance
test_data = TestModel(name="Test User", age=25)
print("Test successful!")
print(f"Created model with name: {test_data.name} and age: {test_data.age}")
