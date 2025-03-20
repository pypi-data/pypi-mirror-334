from animal import AnimalFamily
from kiwi_di import inject
from garden.garden import Garden


@inject
def main(animal_family: AnimalFamily, my_garden: Garden) -> AnimalFamily:
    print(my_garden.rose)
    print(my_garden.tulip)
    print(my_garden.sunflower)

    print(animal_family.dog)
    print(animal_family.cat)

    return animal_family


if __name__ == '__main__':
    ret = main()
    assert isinstance(ret, AnimalFamily)
