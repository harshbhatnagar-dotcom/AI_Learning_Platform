from pydantic import BaseModel,Field
from typing import List

class Question(BaseModel):
    question:str=Field(description="The quetion of quiz")
    options:List[str]=Field(description="The 4 option to the question")
    answer:str=Field(description="Answer to the question")

class Questions(BaseModel):
    questions:List[Question]=Field(description="List of generated questions")

class Flashcard(BaseModel):
    question: str = Field(
        description="The question or prompt displayed on the front of the flashcard."
    )
    answer: str = Field(
        description="The correct answer or explanation displayed on the back of the flashcard."
    )

class Flashcards(BaseModel):
    flashcards: List[Flashcard] = Field(
        description="A list of generated flashcards."
    )

class Topics(BaseModel):
    topics:List[str]=Field(description="List of the topics")