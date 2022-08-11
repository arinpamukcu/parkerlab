import os

# iterate over files in
# that directory

def get_drug():

    calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium'

    drugs = []
    for folder in next(os.walk(calcium_dir))[1]:
        drug_path = os.path.join(calcium_dir, folder)
        drug = os.path.basename(drug_path)
        drugs.append(drug)

    return drugs

def get_dose(drug):

    calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium'
    temp_path = os.path.join(calcium_dir, drug)

    doses = []
    for folder in next(os.walk(temp_path))[1]:
        dose_path = os.path.join(temp_path, folder)
        dose = os.path.basename(dose_path)
        doses.append(dose)

    return doses

def get_animal_id(drug, dose):

    calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium'
    temp_path = os.path.join(calcium_dir, drug, dose)

    D1_animals = ['m085', 'm040', 'm298', 'm404', 'f487', 'f694', 'f857', 'f859', 'm794', 'm797', 'm795']
    D2_animals = ['m971', 'm972', 'm106', 'm120', 'm377', 'm380', 'f414', 'f480', 'm483', 'm485']

    experiments = []
    animal_ids = []
    D1_folders = []
    D2_folders = []

    try:
        for folder in next(os.walk(temp_path))[1]:
            experiments.append(folder)

            animal_id = folder[9:13]
            animal_ids.append(animal_id)

            if animal_id in D1_animals:
                D1_folders.append(folder)
            elif animal_id in D2_animals:
                D2_folders.append(folder)
    except StopIteration:
        pass

    return experiments, D1_folders, D2_folders
