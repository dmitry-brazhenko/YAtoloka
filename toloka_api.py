def create_toloka_project(project_params):
    req = requests.post("https://toloka.yandex.ru/api/v1/projects", headers=headers, json = project_params)
    assert(req.ok)
    new_project_id = req.json()['id']
    print("New project was created. New project id: ", new_project_id)
    return new_project_id


def create_toloka_pool(project_id, pool_params):
    pool_params['project_id'] = str(project_id)
    req = requests.post("https://toloka.yandex.ru/api/v1/pools", headers=headers, json = pool_params)
    assert(req.ok)
    new_pool_id = req.json()['id']
    print("New pool was created. New pool id: ", new_pool_id)
    return new_pool_id

def clone_toloka_pool(pool_id):
    req = requests.post("https://toloka.yandex.ru/api/v1/pools/{}/clone".format(pool_id), headers=headers)
    assert(req.ok)
    operation_id = req.json()['id']
    time.sleep(10)
    operation_status = requests.get("https://toloka.yandex.ru/api/v1/operations/{}".format(operation_id),
            headers=headers).json()

    assert(operation_status['status'] == 'SUCCESS')

    new_pool_id = operation_status['details']['pool_id']
    print("Pool was cloned. New pool was created. New pool id: ", new_pool_id)
    return new_pool_id


def upload_toloka_tasks(tasks):
    req = requests.post("https://toloka.yandex.ru/api/v1/task-suites?allow_defaults=true",
                   headers=headers, json = tasks)
    if not req.ok:
        print(req.text)
    assert(req.ok)

def run_toloka_pool(pool_id):
    req = requests.post("https://toloka.yandex.ru/api/v1/pools/{}/open".format(pool_id), headers=headers)
    assert(req.ok)
    print("Pool {} was started".format(pool_id))

def print_toloka_pool_link(pool_id):
    print("https://toloka.yandex.ru/requester/pool/{}".format(pool_id))


def get_winner_url(row):
    if row['result'] == "LEFT":
        return row['image_left']
    elif row['result'] == "RIGHT":
        return row['image_right']
    else:
        return None

def get_loser_url(row):
    if row['result'] == "LEFT":
        return row['image_right']
    elif row['result'] == "RIGHT":
        return row['image_left']
    else:
        return None

def get_pool_completed_tasks(pool_id):
    req = requests.get("https://toloka.yandex.ru/api/v1/assignments?pool_id={}&limit=10000".format(pool_id), headers = headers)
    completed_items = req.json()["items"]
    #return completed_items
    all_tasks = []
    all_solutions = []
    for i in completed_items:
        if i.get('solutions') is not None:
            tasks = i.get('tasks', [[]])
            tasks = list(map(lambda x: x['input_values'], tasks))
            all_tasks += tasks

            task_solutions = i.get('solutions', [[]])
            task_solutions = list(map(lambda x: x.get("output_values", [[]]), task_solutions))
            all_solutions += task_solutions

    df = pd.merge(pd.DataFrame(all_tasks), pd.DataFrame(all_solutions), left_index=True, right_index=True)
    df['winner_url'] = df.apply(get_winner_url, axis=1)
    df['loser_url'] = df.apply(get_loser_url, axis=1)
    return df


def get_pool_params(pool_id):
    req = requests.get("https://toloka.yandex.ru//api/v1/pools/{}".format(pool_id), headers = headers)
    assert req.ok
    return req.json()

def update_pool_params(pool_id, pool_params):
    req = requests.put("https://toloka.yandex.ru//api/v1/pools/{}".format(pool_id), headers = headers, json=pool_params)
    assert req.ok

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
