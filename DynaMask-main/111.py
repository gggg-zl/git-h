def auto_discover_keypoints(data: list) -> tuple:
    """从标注名数字前缀发现关键点顺序(1鼻子/2左眼/...)，退回alias字母序。"""
    kp_by_num, kp_by_alias = {}, {}
    for item in data:
        annotations = item.get("annotations") or {}
        if not isinstance(annotations, dict):
            continue
        objects = annotations.get("objects") or {}
        if not isinstance(objects, dict):
            continue
        for obj in objects.values():
            if not isinstance(obj, dict) or obj.get("type") != "SKELETON_2D":
                continue
            cls = obj.get("classification") or {}
            alias = cls.get("alias", "")
            name = cls.get("name", "") or alias
            if not alias or alias in BBOX_ALIASES:
                continue
            m = re.match(r"^(\d+)", name)
            if m:
                kp_by_num.setdefault(int(m.group(1)), (alias, name[m.end():].strip() or alias))
            else:
                kp_by_alias.setdefault(alias, name)
    if kp_by_num:
        nums = sorted(kp_by_num)
        return {kp_by_num[n][0]: i for i, n in enumerate(nums)}, [kp_by_num[n][1] for n in nums]
    if kp_by_alias:
        sorted_aliases = sorted(kp_by_alias)
        return {a: i for i, a in enumerate(sorted_aliases)}, [kp_by_alias[a] for a in sorted_aliases]
    return {}, []