def prepare_toloka_task_for_2_screens(url1, url2, overlap, pool_id,
                                      default_question = "Какой вариант вам больше нравится?"):
    assert(overlap >=2)
    tasks = []

    toloka_overlap = int(overlap) / 2
    tasks = [{
            "pool_id": str(pool_id),
            "tasks": [

                {
                  "input_values": {
                      "question":default_question,
                      "image_left": url1,
                      "image_right": url2
                   },

                },
            ],
            "overlap": toloka_overlap,
        },
        {

            "pool_id": str(pool_id),
            "tasks": [
                {
                  "input_values": {
                      "question":default_question,
                      "image_left": url2,
                      "image_right": url1
                   },

                }
            ],
            "overlap": toloka_overlap,
        }
    ]
    return tasks


def prepare_toloka_task_for_many_screens(urls_array, overlap, pool_id,
                                      default_question = "Какой вариант вам больше нравится?"):
    assert(overlap >=2)
    tasks = []


    for left_side in urls_array:
        for right_side in urls_array:
            if left_side != right_side:
                tasks.append({
                    "pool_id": str(pool_id),
                    "tasks": [

                        {
                          "input_values": {
                              "question":default_question,
                              "image_left": left_side,
                              "image_right": right_side
                           },

                        },
                    ],
                    "overlap": overlap,
                })

    return tasks
