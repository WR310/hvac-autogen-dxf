import ezdxf


def print_block_names():
    doc = ezdxf.readfile("Вентиляция для ИИ ГИП.dxf")

    blocks = [
        b.name
        for b in doc.blocks
        if not b.name.startswith("*") and b.name not in ("MODEL_SPACE", "PAPER_SPACE")
    ]

    print("Названия блоков в файле:")
    for name in blocks:
        print(name)


if __name__ == "__main__":
    print_block_names()
