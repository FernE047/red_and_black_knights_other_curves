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
        yield from iterator

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


def permutation_effect(permutation: list[int]) -> EffectRecipe:
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        cache: list[CoordData] = []
        for coord in iterator:
            cache.append(coord)
            if len(cache) == len(permutation):
                for index in permutation:
                    yield cache[index]
                cache = []
        if len(cache):
            yield from cache

    return effect


def section_effect(section_size: int) -> EffectRecipe:
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        sections: list[list[CoordData]] = []
        current_section: list[CoordData] = []
        for coord in iterator:
            current_section.append(coord)
            if len(current_section) == section_size:
                sections.append(current_section)
                current_section = []
        if sections[-1] != current_section:
            sections.append(current_section)
        for index in range(section_size):
            for section in sections:
                if index < len(section):
                    yield section[index]

    return effect


def gravity_effect() -> EffectRecipe:
    def effect(iterator: Iterator[CoordData]) -> Iterator[CoordData]:
        y_coords: dict[int, int] = {}
        for coord in iterator:
            _, x = coord
            if x not in y_coords:
                y_coords[x] = 0
            yield (y_coords[x], x)
            y_coords[x] += 1

    return effect
