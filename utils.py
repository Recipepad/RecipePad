import time
import json


# TODO Fulfill with meaningful tags
def get_tags_from_description_and_title(description, title):
    return {
        'tags': ['food']
    }


def get_cover_image_id(uid):
    ts_ms = round(time.time() * 1000)
    cover_id = f"{uid}-cover-{ts_ms}"
    return cover_id


# TODO Fulfill with meaningful image cnt
def get_image_count_from_steps(steps):
    return 1


def get_step_image_ids(uid, cnt):
    ts_ms = round(time.time() * 1000)
    image_ids = []
    for i in range(cnt):
        image_id = f"{uid}-step-{ts_ms}-{i}"
        image_ids.append(image_id)

    return image_ids


def get_updated_steps_with_image_ids(steps, image_ids):
    for idx in range(len(image_ids)):
        steps[idx]['image_id'] = image_ids[idx]

    return steps
