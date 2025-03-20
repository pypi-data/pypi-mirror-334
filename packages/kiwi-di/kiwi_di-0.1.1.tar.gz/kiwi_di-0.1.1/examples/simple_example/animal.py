import abc
from typing import override, Annotated

from kiwi_di import named_component, Qualifier, component


class Animal(abc.ABC):

    @abc.abstractmethod
    def greeting(self) -> str: ...


@named_component("cat")
class Cat(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a cat."


@named_component("dog")
class Dog(Animal):

    @override
    def greeting(self) -> str:
        return "Hello, I'm a dog."


@component
class AnimalFamily:

    def __init__(
        self,
        cat: Annotated[Animal, Qualifier("cat")],
        dog: Annotated[Animal, Qualifier("dog")],
    ):
        self.cat = cat
        self.dog = dog
