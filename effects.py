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
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        for coord in iterator:
            yield coord

    return effect


def parity_effect(parity_number: int) -> EffectRecipe:
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        parities_cache: list[list[CoordData]] = [[] for _ in range(parity_number - 1)]
        parity = 0
        for coord in iterator:
            if parity == 0:
                yield coord
            else:
                parities_cache[parity - 1].append(coord)
            parity += 1
            if parity == parity_number:
                parity = 0
        for cache in parities_cache:
            yield from cache

    return effect


def reverse_effect() -> EffectRecipe:
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        cache: list[CoordData] = []
        for coord in iterator:
            cache.append(coord)
        yield from reversed(cache)

    return effect
