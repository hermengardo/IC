def build_dir(func):
    def wrapper(path,
                train_size,
                test_size,
                val_size):
        paths = ("./Train", "./Test", "./Val")
        
        for files in zip(paths, func(
            path,
            train_size,
            test_size,
            val_size
        )):
            folder = files[0]
            
            os.makedirs(folder, 
                        exist_ok=True)
            
            for file in files[1]:
                shutil.move(f"{path}/{file}", f"{folder}/{file}")
            
    return wrapper

@build_dir
def partition(path,
              train_size,
              test_size,
              val_size):
    """ Dado um caminho contendo todos os embeddings e proporções, separa os embeddings nas pastas de treino, teste e validação. Se todos os embeddings já estão na pasta de origem, evita que elementos da mesma família estejam em pastas diferentes. """
    assert math.isclose(
        train_size + test_size + val_size, 1,
        rel_tol=1e-6
    )

    files = os.listdir(path)
    pattern = r'(\w+)\.\w+\.\w+\.\d{1,3}\.embeddings\.parquet'
    data = {}
    
    for f in files:
        fam = re.match(pattern, f).group(1)
        if data.get(fam):
            data[fam].append(f)
        else:
            data[fam] = [f]

    families = list(data.keys())
    shuffle(families)
    
    train_size = int(train_size * len(families))
    test_size  = int(test_size * len(families))
    val_size = len(families) - (train_size + test_size) 
    
    train_families = families[:train_size]
    test_families = families[train_size:train_size+test_size]
    val_families = families[train_size+test_size:]

    assert len(train_families) + len(test_families) + len(val_families) == len(families)
    
    train, test, val = [], [], []
    
    for part, fams in [
        (train, train_families), 
        (test, test_families), 
        (val, val_families)
    ]:
        for family in fams:
            part.extend(
                data[family]
            )

    
    assert set(train).intersection(set(test)).intersection(set(val)) == set()

    assert (
        len(train) == len(set(train)) and
        len(test) == len(set(test)) and
        len(val) == len(set(val))
    )
    
    return train, test, val

# Uso
# partition("embeddings", 0.7, 0.2, 0.1)
