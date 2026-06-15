from collections.abc import Callable, Iterator
from generators import CoordData, GeneratorRecipe

EffectRecipe = Callable[[Iterator[CoordData]], Iterator[CoordData]]


def apply_effects(
    generator: GeneratorRecipe,
    *effects: EffectRecipe,
) -> GeneratorRecipe:
    def new_generator(height: int, width: int) -> Iterator[CoordData]:
        iterator = generator(height, width)
        for effect in effects:
            iterator = effect(iterator)
        return iterator

    return new_generator


def normal_effect() -> EffectRecipe:
    def effect(
        iterator: Iterator[CoordData]
    ) -> Iterator[CoordData]:
        for coord in iterator:
            yield coord
    return effect
