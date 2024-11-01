from pathlib import Path
import tempfile
from extractor.pdf_modules_extractor import PdfModulesExtractor

def test_main():
	temp_dir = tempfile.TemporaryDirectory(dir=str(Path(__file__).parent))
	base_path = Path(temp_dir.name)
	PdfModulesExtractor(base_path).main()
	file_path = base_path / "VR09_empfohlene_Wahlmodule.pmwiki"
	assert file_path.exists(), "pmwiki file does not exist"
	expected_content = """
|| border=1
||!                                                                ||! WS       ||||! SS       ||||
||!Empfohlene Wahlmodule zur Vertiefungsrichtung                   ||! SWS ||! LP ||! SWS ||! LP ||
||Components of Power Systems                                      ||      ||     || 2    || 3   ||
||Die Energiewende im Stromtransportnetz                           ||      ||     || 2    || 3   ||
||Echtzeitregelung elektrischer Antriebe                           || 3+1  || 6   ||      ||     ||
||Einführung in die Energiewirtschaft                              ||      ||     || 2+2  || 5   ||
||Elektronische Systeme und EMV                                    ||      ||     || 2    || 3   ||
||Energietechnisches Praktikum                                     || 4    || 6   ||      ||     ||
||Energiewirtschaft                                                || 2    || 3   ||      ||     ||
||Energy Storage and Network Integration                           ||      || 4   ||      ||     ||
||Entwurf elektrischer Maschinen                                   ||      || 5   ||      ||     ||
||Leistungselektronik für die Photovoltaik und Windenergie         ||      ||     || 2    || 3   ||
||Leistungselektronische Systeme in der Energietechnik             || 3+1  || 6   ||      ||     ||
||Photovoltaik                                                     ||      ||     || 4    || 6   ||
||Praktikum Informationssysteme in der elektrischen Energietechnik ||      ||     || 4    || 6   ||
||Praktikum: Smart Energy System Lab                               ||      ||     || 2    || 6   ||
||Praxis elektrischer Antriebe                                     || 2+1  || 4   ||      ||     ||
||Schutz- und Leittechnik in elektrischen Netzen                   || 2    || 3   ||      ||     ||
""".strip()
	file_content = file_path.read_text().strip()

	# Assert that the file content matches the expected content
	assert file_content == expected_content, "File content does not match the expected content"