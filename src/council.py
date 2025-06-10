import random

print("\033[H\033[2J", end="")
print("\033[H\033[3J", end="")

class Councilor:
    last_id = 0

    def __init__(self, phrase: str):
        Councilor.last_id += 1
        self.id = Councilor.last_id
        self.phrase = phrase

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
        self.councilors = [Councilor(p) for p in phrases]

    def session(self) -> None:
        councilor_names = [c.real_id for c in self.councilors]
        councilor_names.sort()
        print(f"[ Session convened: {', '.join(councilor_names)} ]")
        rounds = 8
        last_speaker = None

        for i in range(rounds):
            speaker = random.choice([c for c in self.councilors if last_speaker != c])
            last_speaker = speaker
            print(speaker.respond())

        for c in self.councilors:
            print(c.respond_final())

CouncilSession(["beep", "boop", "blep", "blop?"]).session()