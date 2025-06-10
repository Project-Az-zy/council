import random
from termcolor import colored

print("\033[H\033[2J", end="")
print("\033[H\033[3J", end="")

class RandColor:
    def __init__(self, strength: int):
        r = random.random()
        g = random.random()
        b = random.random()
        t = r+g+b

        self.color = (
            int(r/t*strength),
            int(g/t*strength),
            int(b/t*strength),
        )

    def variation(self, strength: int) -> tuple[int, int, int]:
        r = random.random()
        g = random.random()
        b = random.random()
        t = r+g+b

        nr = min(255, max(0, int(self.color[0] + strength*r/t*random.choice([1, -1]))))
        ng = min(255, max(0, int(self.color[1] + strength*g/t*random.choice([1, -1]))))
        nb = min(255, max(0, int(self.color[2] + strength*b/t*random.choice([1, -1]))))
        nt = nr+ng+nb
        ot = self.color[0]+self.color[1]+self.color[2]

        return (
            min(255, max(0, int(nr/nt*ot))),
            min(255, max(0, int(ng/nt*ot))),
            min(255, max(0, int(nb/nt*ot))),
        )


class Councilor:
    last_id = 0

    def __init__(self, phrase: str, *, base_color: RandColor):
        Councilor.last_id += 1
        self.id = Councilor.last_id
        self.phrase = phrase
        self.color = base_color.variation(90)

    @property
    def real_id(self) -> str:
        return self.phrase

    def respond(self) -> str:
        return f"C-{self.id}: {self.phrase}"

    def respond_final(self) -> str:
        return f"C-{self.id}: {self.phrase} {self.phrase}"


class CouncilSession:
    def __init__(self, phrases: list[str]):
        phrases = [*phrases]
        random.shuffle(phrases)
        base_color = RandColor(400)
        self.councilors = [Councilor(p, base_color=base_color) for p in phrases]

    def session(self) -> None:
        councilor_names = [c.real_id for c in self.councilors]
        councilor_names.sort()
        print(colored(f"[ Session convened: {', '.join(councilor_names)} ]", "white", attrs=["bold"]))
        rounds = 8
        last_speaker = None

        for i in range(rounds):
            speaker: Councilor = random.choice([c for c in self.councilors if last_speaker != c])
            last_speaker = speaker
            print(colored(speaker.respond(), speaker.color))

        for c in self.councilors:
            print(colored(c.respond_final(), c.color))

CouncilSession(["beep", "boop", "blep", "blop?"]).session()