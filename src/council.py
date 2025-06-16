import random
import time
import json
from os import listdir, environ
from os.path import isfile, join

from google import genai
from google.genai import types
from termcolor import colored

print("\033[H\033[2J", end="")
print("\033[H\033[3J", end="")

PERSONALITIES_PATH = "/personalities"

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

client = genai.Client(api_key=environ['KEY_GENAI'])

class Councilor:
    last_id = 0

    def __init__(self, path: str, *, base_color: RandColor):
        Councilor.last_id += 1
        self.anon_id = f'C-{Councilor.last_id}'
        self.real_id = path.split(".")[0].split("-")[-1]
        self.phrase = path.split("-")[0]
        self.color = base_color.variation(90)
        with open(f"{PERSONALITIES_PATH}/{path}") as f:
            self.personality = json.loads(f.read())["personality"]

    def _normalize_history(self, history: list[tuple[str, str]]) -> list[str]:
        return [f"{h[0]}: {h[1]}" for h in history]

    def _generate_response(self, history: list[str]) -> str:
        time.sleep(3)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=f"You are a part of an AI council designed to resolve dilemmas through cooperation, councilor {self.anon_id}. Your goal is to convince others and the listening audience of your worldview. Follow the proper debate practices and try not to repeat your argumentation. Your responses should be short, no more than a few sentences. Assume following personality:\n\n{self.personality}",
                max_output_tokens=11000,
            ),
            contents=history
        )
        return response.text

    def _sanitize_response(self, response: str) -> str:
        if ':' in response and response.find(":") < 16:
            response = ":".join(response.split(":")[1:])
        response = response.strip()
        return response

    def respond(self, *, history: list[tuple[str, str]]) -> str:
        return self._sanitize_response(self._generate_response(self._normalize_history(history)))

    def respond_final(self, *, history: list[tuple[str, str]]) -> str:
        return self._sanitize_response(self._generate_response(self._normalize_history(history)+["SYSTEM: This is your last round of discussion, please summarise and give your final remarks"]))


class CouncilSession:
    def __init__(self):
        paths = [f for f in listdir(PERSONALITIES_PATH) if isfile(join(PERSONALITIES_PATH, f)) and f.endswith(".person")]
        random.shuffle(paths)
        base_color = RandColor(400)
        self.councilors = [Councilor(p, base_color=base_color) for p in paths]

    def session(self) -> None:
        print(colored(f"[ Awaiting dilemma... ]", "white", attrs=["bold"]))
        input_dilemma = input()

        councilor_names = [c.real_id for c in self.councilors]
        councilor_names.sort()
        print(colored(f"[ Session convened: {', '.join(councilor_names)} ]", "white", attrs=["bold"]))
        rounds = 12
        last_speaker = None
        history = [("Dilemma", input_dilemma)]

        for i in range(rounds):
            speaker: Councilor = random.choice([c for c in self.councilors if last_speaker != c])
            last_speaker = speaker
            response = speaker.respond(history=history)
            history.append((speaker.anon_id, response))
            print(colored(f"{speaker.anon_id}: {response}", speaker.color))

        for speaker in self.councilors:
            response = speaker.respond_final(history=history)
            history.append((speaker.anon_id, response))
            print(colored(f"{speaker.anon_id}: {response}", speaker.color))

        print(colored(f"[ Session adjourned ]", "white", attrs=["bold"]))


CouncilSession().session()