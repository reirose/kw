from bin.db_init import kw_db


def get_data(kw: str) -> list | None:
    db_response = kw_db.find({
                                "$or": [
                                    { "keyword": { "$in": [kw.lower()] } },
                                    { "keyword": { "$regex": kw.lower(), "$options": "i" } }
                                ]
                            }) if kw else kw_db.find({})
    response = [doc for doc in db_response]
    for i in response:
        i["keyword"] = ", ".join(i.get("keyword"))
    # print(response)
    try:
        if len(kw.split(" ")) > 1:
            for word in kw.split(" "):
                db_response = kw_db.find({"keyword": {"$in": [word]}})
                for one in [doc for doc in db_response]:
                    one["keyword"] = ", ".join(one["keyword"])
                    response.append(one)
    except AttributeError:
        pass
    return remove_duplicates(response)


def remove_duplicates(input_list: list) -> list:

    for i in input_list:
        if input_list.count(i) > 1:
            for _ in range(0, input_list.count(i) - 1):
                input_list.remove(i)

    return input_list
