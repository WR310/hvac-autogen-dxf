import ezdxf
from ezdxf import bbox


def generate_scheme(source_data):
    try:
        doc = ezdxf.readfile("template.dxf")
    except IOError:
        raise FileNotFoundError(
            "Ошибка: Не найден файл шаблона template.dxf. Убедитесь, что он лежит в папке."
        )

    msp = doc.modelspace()

    block_map = {
        "ПРИТОЧКА": "приточка",
        "ФИЛЬТР": "фильтр",
        "ВЕНТУСТАНОВКА_ПРИТОК_ВОДА": "Вентустановка_Приток_Вода",
        "ШУМОГЛУШИТЕЛЬ": "шумоглушитель",
        "ВР": "Вытяжной вентилятор",
        "РЕШЕТКА": "ОВ_Зонт",
        "КЛАПАН": "обратный клапан",
    }

    block_bounds = {}
    for logic_name, real_name in block_map.items():
        try:
            block = doc.blocks.get(real_name)
            box = bbox.extents(block, cache=bbox.Cache())
            if box.has_data:
                center_y = (box.extmin.y + box.extmax.y) / 2
                block_bounds[logic_name] = (box.extmin.x, box.extmax.x, center_y)
            else:
                block_bounds[logic_name] = (0, 2000, 0)
        except Exception:
            block_bounds[logic_name] = (0, 2000, 0)

    y_offset = 0
    systems = source_data.get("systems", [])

    for system in systems:
        system_name = system.get("name", "Без названия")
        equipment_list = system.get("equipment", [])

        chain = []
        for eq in equipment_list:
            title = eq.get("title", "")
            title_lower = title.lower()

            logic_name = None
            if "установка" in title_lower:
                logic_name = "ПРИТОЧКА"
            elif "фильтр" in title_lower:
                logic_name = "ФИЛЬТР"
            elif "нагреват" in title_lower or "калорифер" in title_lower:
                logic_name = "ВЕНТУСТАНОВКА_ПРИТОК_ВОДА"
            elif "шумоглушител" in title_lower:
                logic_name = "ШУМОГЛУШИТЕЛЬ"
            elif "вентилятор" in title_lower:
                logic_name = "ВР"
            elif (
                "решетк" in title_lower
                or "диффузор" in title_lower
                or "зонт" in title_lower
                or "выброс" in title_lower
            ):
                logic_name = "РЕШЕТКА"
            elif "клапан" in title_lower:
                logic_name = "КЛАПАН"

            if logic_name:
                chain.append((logic_name, title))

        if not chain:
            continue

        first_bounds = block_bounds.get(chain[0][0], (0, 2000, 0))
        x_offset = -first_bounds[0]

        mtext = msp.add_mtext(f"Система {system_name}", dxfattribs={"char_height": 250})
        mtext.set_location(insert=(0, y_offset + 1500))

        for i, item in enumerate(chain):
            logic_name, real_title = item
            real_name = block_map.get(logic_name)
            min_x, max_x, center_y = block_bounds.get(logic_name, (0, 2000, 0))

            if i == 0:
                msp.add_line((x_offset - 1000, y_offset), (x_offset, y_offset))

            insert_y = y_offset - center_y
            msp.add_blockref(real_name, (x_offset, insert_y))

            center_x = x_offset + (max_x - min_x) / 2

            label = msp.add_mtext(
                real_title,
                dxfattribs={"char_height": 120, "attachment_point": 8, "width": 2800},
            )
            label.set_location(insert=(center_x, y_offset - 1200))

            current_right_edge = x_offset + max_x

            line_start = current_right_edge
            line_end = line_start + 3000
            msp.add_line((line_start, y_offset), (line_end, y_offset))

            if i < len(chain) - 1:
                next_logic = chain[i + 1][0]
                next_bounds = block_bounds.get(next_logic, (0, 2000, 0))
                x_offset = line_end - next_bounds[0]

        y_offset -= 6000

    output_filename = "demo_result.dxf"
    doc.saveas(output_filename)
    return output_filename
