from random import choice
from typing import Iterator
from collections import Counter, defaultdict

from viral_rna_simulation.site import Site
from viral_rna_simulation.utils import mutations_str


class Genome:
    def __init__(self, sites: list[Site] | str | None = None, length: int = 0) -> None:
        if sites:
            self.sites = (
                sites if isinstance(sites, list) else [Site(base) for base in sites]
            )
        elif length:
            self.sites = [Site(choice("ACGT")) for _ in range(length)]
        else:
            raise ValueError(
                "You must provide either the genome sites or a non-zero genome length."
            )

    def __iter__(self) -> Iterator[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)

    def __getitem__(self, offset) -> Site:
        return self.sites[offset]

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Genome):
            return all(a == b for (a, b) in zip(self.sites, other.sites))
        return NotImplemented

    def __str__(self) -> str:
        result = [f"<Genome length {len(self.sites)}>"]

        for site in self.sites:
            result.append(f"  {site}")

        return "\n".join(result)

    def replicate(self, mutation_rate: float = 0.0) -> "Genome":
        """
        Copy the new genome (reverse complemented), possibly with mutations.
        """
        return Genome([site.replicate(mutation_rate) for site in reversed(self.sites)])

    def rc(self) -> "Genome":
        """
        Get a reverse-complemented genome.
        """
        return Genome([site.rc() for site in reversed(self.sites)])

    def mutations(self) -> Counter:
        """
        Get the mutations that have occurred in this genome.
        """
        mutations = Counter()
        for site in self.sites:
            mutations += site.mutations

        return mutations


def genomes_str(
    genome_1: Genome,
    genome_2: Genome,
    title_1: str = "",
    title_2: str = "",
    differences_title: str = "Differences: ",
    mutations_title: str | None = None,
) -> str:
    s_1 = "".join(site.base for site in genome_1)
    s_2 = "".join(site.base for site in genome_2)

    mutations = defaultdict(int)

    difference = []
    for base_1, base_2 in zip(s_1, s_2):
        if base_1 == base_2:
            difference.append(" ")
        else:
            difference.append("|")
            mutations[base_1 + base_2] += 1

    if mutations_title is None:
        mutations_title = f"Mutations ({sum(mutations.values())}): "

    if mutations:
        width = max(len(title_1), len(title_2), len(differences_title), len(mutations_title))

        return "\n".join([
            f"{title_1:{width}}" + s_1,
            f"{differences_title:{width}}" + "".join(difference),
            f"{title_2:{width}}" + s_2,
            f"{mutations_title:{width}}{mutations_str(mutations)}"
        ])
    else:
        width = max(len(title_1), len(title_2))

        return "\n".join([
            f"{title_1:{width}}" + s_1,
            f"{title_2:{width}}Identical",
        ])
