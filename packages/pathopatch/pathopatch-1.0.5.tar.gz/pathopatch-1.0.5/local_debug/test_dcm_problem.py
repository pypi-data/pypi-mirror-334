from openslide import OpenSlide
from pathopatch.wsi_interfaces.wsidicomizer_openslide import DicomSlide
from wsidicom import WsiDicom
from wsidicom.file import WsiDicomFileSource
from pathlib import Path

slide_folder = "/Users/fhoerst/Fabian-Projekte/DICOM-WSI/Example-DCM-Local/E6805_20-1A.1_4_28_012043/"
# slide_folder = "/Volumes/digitalpathology/2024-02-08/_1_1_100851"
slide_folder = Path(slide_folder)
slide_list = list(slide_folder.glob("*.dcm"))
slide_os = OpenSlide(slide_list[0])

slide_dcm = DicomSlide(slide_folder)