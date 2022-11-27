import random, string

def update_case(db, case_id, data):
    if not case_id == None:
        db.collection("cases").document(case_id).set(data)
        return
    
    while True:
        case_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        if case_id not in db.collection("cases").stream():
            break

    db.collection("cases").document(case_id).set(data)

    target_links_ref = db.collection("target_links").document(str(data["Target"]))
    target_links_ref.set({str(len(target_links_ref.get().to_dict() or {}.keys()) + 1): case_id})

    moderator_links_ref = db.collection("moderator_links").document(str(data["Moderator"]))
    moderator_links_ref.set({str(len(moderator_links_ref.get().to_dict() or {}.keys()) + 1): case_id})

