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

    animal_ids = []
    for folder in next(os.walk(temp_path))[1]:
        animal_path = os.path.join(temp_path, folder)
        animal_id = os.path.basename(animal_path)
        animal_ids.append(animal_id)

    return animal_ids