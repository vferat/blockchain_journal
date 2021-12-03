from models import UserModel, PaperModel


def populate_database(db, n_users=100, n_papers=10):
    for user in range(n_users):
        username = f'user{user}'
        email = f'{username}@test.ch'
        password = username
        User = UserModel(email=email, username=username)
        User.set_password(password)
        for paper in range(n_papers):
            paper = PaperModel(doi='https://doi.org/10.1109/5.771073')
            User.papers.append(paper)
        db.session.add(User)

    db.session.commit()