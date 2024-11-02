from pathlib import Path
import tempfile
from extractor.specializations_extractor import SpecializationsExtractor

def test_main():
	temp_dir = tempfile.TemporaryDirectory(dir=str(Path(__file__).parent))
	base_path = Path(temp_dir.name)
	extractor = SpecializationsExtractor(base_path)
	extractor.extract_and_print_tables()
	file_path = base_path / "specializations/09 Elektroenergiesysteme und Hochspannungstechnik/output.pmwiki"
	assert file_path.exists(), "pmwiki file does not exist"
	expected_content = """
* [[2302117 Measurement Technology | 2302117 Measurement Technology]]
* [[2302118 Exercise for 2302117 Measurement Technology | 2302118 Exercise for 2302117 Measurement Technology]]
* [[2303183 Optimization of Dynamic Systems | 2303183 Optimization of Dynamic Systems]]
* [[2303185 Übungen zu 2303183 Optimization of Dynamic Systems | 2303185 Übungen zu 2303183 Optimization of Dynamic Systems]]
* [[2306357 Leistungselektronische Systeme in der Energietechnik | 2306357 Leistungselektronische Systeme in der Energietechnik]]
* [[2306358 Übung zu 2306357 Leistungselektronische Systeme in der Energietechnik | 2306358 Übung zu 2306357 Leistungselektronische Systeme in der Energietechnik]]
* [[2307360 Hochspannungstechnik | 2307360 Hochspannungstechnik]]
* [[2307362 Übungen zu 2307360 Hochspannungstechnik | 2307362 Übungen zu 2307360 Hochspannungstechnik]]
* [[2307371 Elektrische Energienetze | 2307371 Elektrische Energienetze]]
* [[2307373 Übungen zu 2307371 Elektrische Energienetze | 2307373 Übungen zu 2307371 Elektrische Energienetze]]
* [[2307392 Hochspannungsprüftechnik | 2307392 Hochspannungsprüftechnik]]
* [[2307394 Übungen zu 2307392 Hochspannungsprüftechnik | 2307394 Übungen zu 2307392 Hochspannungsprüftechnik]]
""".strip()
	file_content = file_path.read_text().strip()

	# Assert that the file content matches the expected content
	assert file_content == expected_content, "File content does not match the expected content"