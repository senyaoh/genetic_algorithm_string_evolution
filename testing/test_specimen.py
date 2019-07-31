from genetic_algorithm_string_evolution.ga_string_evolution import Specimen
import pytest

def test_specimen():
    specimen = Specimen("deoxyribonucleicacid")
    assert specimen.phenotype == "deoxyribonucleicacid"