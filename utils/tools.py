def drop_false(obj):
    if isinstance(obj, dict):
        # Si l'objet est un dictionnaire, parcourez les clés et les valeurs
        for key, value in obj.items():
            # Si la valeur est "False", remplacez-la par une chaîne vide
            if value is False or value == "false":
                obj[key] = ""
            # Si la valeur est un autre objet itérable (liste, dictionnaire, etc.),
            # appelez la fonction récursivement sur cet objet
            elif isinstance(value, (list, dict)):
                drop_false(value)
    elif isinstance(obj, list):
        # Si l'objet est une liste, parcourez chaque élément de la liste
        for i in range(len(obj)):
            # Si l'élément est "False", remplacez-le par une chaîne vide
            if obj[i] is False or obj[i] == "false":
                obj[i] = ""
            # Si l'élément est un autre objet itérable (liste, dictionnaire, etc.),
            # appelez la fonction récursivement sur cet objet
            elif isinstance(obj[i], (list, dict)):
                drop_false(obj[i])
    return obj
