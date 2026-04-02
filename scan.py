import ezdxf

try:
    doc = ezdxf.readfile("template.dxf")
    print("Найдены скрытые блоки в шаблоне:")
    for block in doc.blocks:
        # Отсекаем стандартные системные листы Автокада
        if not block.name.lower().endswith("_space"):
            print(f"- {block.name}")
except Exception as e:
    print(f"Ошибка при чтении шаблона: {e}")
