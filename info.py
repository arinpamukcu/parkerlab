# Created by Arin Pamukcu, PhD on August 2022 in Chicago, IL

import os

# path
# calcium_dir = 'R:\Basic_Sciences\Phys\Kennedylab\Parkerlab\Calcium_v2' #pc
calcium_dir = '/Volumes/fsmresfiles/Basic_Sciences/Phys/Kennedylab/Parkerlab/Calcium_v2' #mac

def get_drug():

    drugs = []
    for folder in next(os.walk(calcium_dir))[1]:
        drug_path = os.path.join(calcium_dir, folder)
        drug = os.path.basename(drug_path)
        drugs.append(drug)

    return drugs


def get_dose(drug):

    temp_path = os.path.join(calcium_dir, drug)

    doses = []
    for folder in next(os.walk(temp_path))[1]:
        dose_path = os.path.join(temp_path, folder)
        dose = os.path.basename(dose_path)
        doses.append(dose)

    return doses


def D1_D2_names():

    D1_animals = ['m085', 'm040', 'm298', 'm404', 'f487', 'f694', 'f857', 'f859', 'm794', 'm797', 'm795',
                  'm659', 'm973', 'm974', 'm975', 'f976', 'f977', 'f979']  # count: 18 animals
    D2_animals = ['m971', 'm972', 'm106', 'm120', 'm377', 'm380', 'f414', 'f480', 'm483', 'm485',
                  'm241', 'm242', 'm523', 'f605', 'f808', 'f811', 'f840']  # count: 17 animals

    return D1_animals, D2_animals


def get_animal_id(drug, dose):

    temp_path = os.path.join(calcium_dir, drug, dose)

    D1_animals, D2_animals = D1_D2_names()

    experiments = []
    animals = []
    D1_folders = []
    D2_folders = []

    try:
        for folder in next(os.walk(temp_path))[1]:
            if folder[-4:] != 'amph':
                experiments.append(folder)

                animal = folder[9:13]
                animals.append(animal)

                if animal in D1_animals:
                    D1_folders.append(folder)
                elif animal in D2_animals:
                    D2_folders.append(folder)
    except StopIteration:
        pass

    return experiments, animals, D1_folders, D2_folders
