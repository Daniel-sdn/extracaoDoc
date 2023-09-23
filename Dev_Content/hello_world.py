from prefect import flow


@flow(log_prints=True)
def hello_world(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")

    if goodbye:
        print(f"Ate mais meu rei:{name}!")


if __name__ == "__main__":
    hello_world.serve(name="my-SECOND-deployment",
                      tags=["sextou"],
                      parameters={"goodbye": True},
                      interval=60)