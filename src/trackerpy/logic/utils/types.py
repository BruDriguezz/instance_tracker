class ObjectSet(dict):
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        items_repr = ", \n".join(
            f'{v.obj.id} - Object("{v.obj.name}", "{type(v).__name__}", "{len(v.obj._instances)}")'
            for v in self.values()
        )
        return f"({items_repr})"