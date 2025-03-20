from basicApiModel.models.project import Project


def app():
    Project.create()


if __name__ == "__main__":
    app()
