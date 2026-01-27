import argparse
import hashlib
import os

import pandas as pd

DEFAULT_INPUT_TRAIN = "../data/raw/train.csv"
DEFAULT_INPUT_TEST = "../data/raw/test.csv"
DEFAULT_OUTPUT_DIR = "../data/sentence"

TIMEFRAMES = [
    "a few days",
    "a week",
    "two weeks",
    "a month",
    "several days",
    "about a week",
]

SEVERITIES = [
    "mild",
    "moderate",
    "pretty strong",
    "persistent",
    "on and off",
]

TIMES_OF_DAY = [
    "morning",
    "evening",
    "night",
    "afternoon",
]

FOLLOWUPS = [
    lambda ctx: f"It started about {ctx['timeframe']} ago.",
    lambda ctx: f"They feel {ctx['severity']}.",
    lambda ctx: "Some symptoms come and go.",
    lambda ctx: f"They seem worse in the {ctx['time_of_day']}.",
    lambda ctx: "It is affecting my daily routine.",
    lambda ctx: "Rest has not helped much.",
    lambda ctx: "It's been hard to focus because of this.",
    lambda ctx: "I'm not sleeping well lately.",
]

CLOSINGS = [
    "I'm not sure what is causing it.",
    "I'm worried it might be something serious.",
    "I would like to know what could be going on.",
    "I am looking for advice.",
]

ADD_ONS = [
    "and it hasn't really improved",
    "and it keeps coming back",
    "and it doesn't seem to go away",
    "and it's been hard to ignore",
    "and it bothers me most of the day",
]

ADD_ONS_SHORT = [
    "and it worries me a bit",
    "and it feels exhausting",
    "and it gets in the way",
    "and it is hard to manage",
    "and it has been distracting",
]

def split_symptoms(text):
    raw_text = str(text).strip()
    parts = [p.strip() for p in raw_text.split(",") if p.strip()]
    return parts


def join_symptoms(parts):
    if not parts:
        return "I feel unwell."
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return f"{', '.join(parts[:-1])}, and {parts[-1]}"


def pick_index(seed_text, count):
    digest = hashlib.md5(seed_text.encode("utf-8")).hexdigest()
    return int(digest, 16) % count


def split_groups(parts):
    if len(parts) <= 3:
        return parts, []
    mid = max(2, len(parts) // 2)
    return parts[:mid], parts[mid:]


def build_context(parts, seed_text):
    timeframe = TIMEFRAMES[pick_index(seed_text + "time", len(TIMEFRAMES))]
    severity = SEVERITIES[pick_index(seed_text + "severity", len(SEVERITIES))]
    time_of_day = TIMES_OF_DAY[pick_index(seed_text + "tod", len(TIMES_OF_DAY))]
    group1, group2 = split_groups(parts)
    symptoms_all = join_symptoms(parts)
    symptoms_group1 = join_symptoms(group1)
    symptoms_group2 = join_symptoms(group2) if group2 else ""
    symptom = parts[0] if parts else "a symptom"
    return {
        "timeframe": timeframe,
        "severity": severity,
        "time_of_day": time_of_day,
        "symptoms_all": symptoms_all,
        "symptoms_group1": symptoms_group1,
        "symptoms_group2": symptoms_group2,
        "has_group2": bool(group2),
        "symptom": symptom,
    }


def choose_opener(parts, ctx, seed_text):
    openers = [
        lambda c: f"For the last {c['timeframe']}, I've been dealing with {c['symptoms_all']}.",
        lambda c: f"I'm experiencing {c['symptoms_all']}.",
        lambda c: f"Lately I've noticed {c['symptoms_all']}.",
        lambda c: f"The main problems are {c['symptoms_all']}.",
    ]
    if ctx["has_group2"]:
        openers.append(
            lambda c: f"The main issues are {c['symptoms_group1']}, along with {c['symptoms_group2']}."
        )
        openers.append(
            lambda c: f"It started with {c['symptom']} and now I also have {c['symptoms_group2']}."
        )
    else:
        openers.append(lambda c: f"The main issue is {c['symptom']}.")
    opener = openers[pick_index(seed_text + "opener", len(openers))]
    return opener(ctx)


def extend_followup(sentence, seed_text, addons=None, key="addon"):
    suffixes = addons or ADD_ONS
    addon = suffixes[pick_index(seed_text + key, len(suffixes))]
    base = sentence.rstrip(".")
    return f"{base}, {addon}."


def to_patient_sentence(text):
    parts = split_symptoms(text)
    ctx = build_context(parts, text)
    opener = choose_opener(parts, ctx, text)

    followup_1 = FOLLOWUPS[pick_index(text + "followup1", len(FOLLOWUPS))](ctx)
    followup_1 = extend_followup(followup_1, text)
    followup_2 = FOLLOWUPS[pick_index(text + "followup2", len(FOLLOWUPS))](ctx)
    followup_2 = extend_followup(followup_2, text, ADD_ONS_SHORT, "addon2")
    closing = CLOSINGS[pick_index(text + "closing", len(CLOSINGS))]

    sentences = [opener, followup_1, followup_2]
    if len(parts) >= 5 or pick_index(text + "extra", 2) == 0:
        sentences.append(closing)
    return " ".join(sentences[:4])


def augment_file(input_path, output_path):
    df = pd.read_csv(input_path)
    df["text"] = df["text"].apply(to_patient_sentence)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-train", default=DEFAULT_INPUT_TRAIN)
    parser.add_argument("--input-test", default=DEFAULT_INPUT_TEST)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    train_out = os.path.join(args.output_dir, "train.csv")
    test_out = os.path.join(args.output_dir, "test.csv")

    augment_file(args.input_train, train_out)
    augment_file(args.input_test, test_out)
    print(f"Saved: {train_out}, {test_out}")


if __name__ == "__main__":
    main()
