from pathlib import Path
import tempfile
from extractor.study_plan_extractor import main

def test_main():
	temp_dir = tempfile.TemporaryDirectory(dir=str(Path(__file__).parent))
	base_path = Path(temp_dir.name)
	main(base_path)
	file_path = base_path / "study_plan_with_links.pmwiki"
	assert file_path.exists(), "pmwiki file does not exist"
	expected_content = """
||!Key ||!Art ||!LP ||!Link ||
||88-048-H-2018 – Elektrotechnik und Informationstechnik Master 2018 || ||120,0 ||[[https://campus.kit.edu/sp/campus/all/abstractProductView.asp?gguid=0xF654B5E6CC6842A8B943858D89F69741&capvguid=0x32F8959548FE4CE8A0EA1FCE19956FB7&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||    Masterarbeit ||PF ||30,0 ||[[https://campus.kit.edu/sp/campus/all/abstractFieldView.asp?gguid=0x559748BB56AC4CC18CEF0C64FE9879A4&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-104495 – Masterarbeit ||PF ||30,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x68127720476542AB849CEAE994753E90&camvguid=0xBE78B928F60246EAAA0A1A3EBA73A628&cafiguid=0x559748BB56AC4CC18CEF0C64FE9879A4&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-109186 – Masterarbeit | T-ETIT-109186 – Masterarbeit]] ||PF ||30,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0xF2565576FB564728AE56FA3340FDA2A0&cabvguid=0x73452AA9F370462E841840D61B5F4525&camvguid=0xBE78B928F60246EAAA0A1A3EBA73A628&cafiguid=0x559748BB56AC4CC18CEF0C64FE9879A4&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||    Grundlagen zur Vertiefungsrichtung ||PF ||11,0 - 15,0 ||[[https://campus.kit.edu/sp/campus/all/abstractFieldView.asp?gguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-100565 – Antennen und Mehrantennensysteme ||WP: Grundlagen zur Vertiefungsrichtung ||5,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x4C52A005FAEC2540982F07A35CB3ACE0&camvguid=0x0839EC74814F4A12987F3C1A03C58DCB&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-106491 – Antennen und Mehrantennensysteme | T-ETIT-106491 – Antennen und Mehrantennensysteme]] ||PF ||5,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0xD4FE9E0312254C39A2979749B48E2F11&cabvguid=0x0BBD3C0FFD9744A4A87DD57AE52513AD&camvguid=0x0839EC74814F4A12987F3C1A03C58DCB&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-102651 – Bildverarbeitung ||WP: Grundlagen zur Vertiefungsrichtung ||3,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x665C304812C30948BD9D7C2E5BD3DFFA&camvguid=0xD80C52E037AD1C4A92D78AC0C6A52C79&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-105566 – Bildverarbeitung | T-ETIT-105566 – Bildverarbeitung]] ||PF ||3,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0x274BDED1CDC10D4685C80F0528A64141&cabvguid=0xE6FB47CFDCFE344782030F67EFED7E88&camvguid=0xD80C52E037AD1C4A92D78AC0C6A52C79&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-100539 – Communication Systems and Protocols ||WP: Grundlagen zur Vertiefungsrichtung ||5,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x378DC443BFEDFA4982E6AA6155AD91CC&camvguid=0xE945392F08AB4144842E51E76BEC029C&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-101938 – Communication Systems and Protocols | T-ETIT-101938 – Communication Systems and Protocols]] ||PF ||5,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0xB810B45E42D1D140B8E38F596DC36C62&cabvguid=0x0E70881974C2AA42B889F8E8F54B8BF9&camvguid=0xE945392F08AB4144842E51E76BEC029C&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-100449 – Hardware Modeling and Simulation ||WP: Grundlagen zur Vertiefungsrichtung ||4,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x231D69D33406CD45B8C44FE2C0E2E59D&camvguid=0xA998A0917D534198BA6C9C18D6ADAEDB&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-100672 – Hardware Modeling and Simulation | T-ETIT-100672 – Hardware Modeling and Simulation]] ||PF ||4,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0x25C9ADF2B396504E83AE5FA1016B2171&cabvguid=0xDE5B8D65AA7F4810BFBE9ECDE50474CB&camvguid=0xA998A0917D534198BA6C9C18D6ADAEDB&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-103264 – Informationsfusion ||WP: Grundlagen zur Vertiefungsrichtung ||4,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0xCC315DBA354D42509CD6B12381CE4F50&camvguid=0x1ED1B4CB630E4C96A6058B06058CA59E&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||            [[T-ETIT-106499 – Informationsfusion | T-ETIT-106499 – Informationsfusion]] ||PF ||4,0 ||[[https://campus.kit.edu/sp/campus/all/abstractBrickView.asp?gguid=0x0E14C35D6351482B9B3E88B1B3D5C901&cabvguid=0x8A7D322E5CC74CE0A25F0025875E7D26&camvguid=0x1ED1B4CB630E4C96A6058B06058CA59E&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
||        M-ETIT-105982 – Measurement Technology ||WP: Grundlagen zur Vertiefungsrichtung ||5,0 ||[[https://campus.kit.edu/sp/campus/all/abstractModuleView.asp?gguid=0x0401218B10B2495C8E23426404F2406D&camvguid=0x3EAD688B19E14C4D9111E148732F7E8A&camvceid=CMPEL_1C5C3341&cafiguid=0x87CF8F857B454E4B9E6465DC030218FC&tguid=0x8B8BEF2D6B894380973363ED68D60E22 | link]] ||
""".strip()
	file_content = file_path.read_text().strip()

	# Assert that the file content matches the expected content
	assert file_content.startswith(expected_content), "File content does not match the expected content"