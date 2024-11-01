# set up system
```
conda env create --prefix .conda -f install_environment/environment.yml
```

# update environment.yml
```
python install_environment/clean_yml.py
```

# remove conda environment
```
conda env remove -p .conda
```

# update conda environment
```
conda env update --file install_environment/environment.yml -p ./.conda
```

# create envirronment.yml file
```
conda env export --file install_environment/environment.yml --from-history
conda env export --file install_environment/environment_with_pip.yml
```