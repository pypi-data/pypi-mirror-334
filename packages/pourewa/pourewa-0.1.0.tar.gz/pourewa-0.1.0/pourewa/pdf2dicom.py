import pydicom
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian


def pdf_to_dicom(pdfFilePath, templateDicomFilePath, dicomOutFilePath=None):
    """
    Convert a PDF file to a DICOM file.

    Args:
        pdfFilePath (str): Path to the PDF file to convert.
        templateDicomFilePath (str): Path to the DICOM file to use as a template.
        dicomOutFilePath (str, optional): Path to save the output DICOM file. If not provided, the function will return the DICOM dataset.

    Returns:
        pydicom.dataset.Dataset: The DICOM dataset.
    """
    # Read the PDF file
    with open(pdfFilePath, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    # Read template DICOM file
    template_ds = pydicom.dcmread(templateDicomFilePath)

    # Create metadata for new file
    meta = FileMetaDataset()
    meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.104.1"  # Encapsulated PDF Storage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = ExplicitVRLittleEndian

    # Create new dataset and copy relevant attributes from template
    ds = Dataset()
    ds.file_meta = meta
    ds.SOPClassUID = meta.MediaStorageSOPClassUID
    ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
    
    # Copy patient and study information from template
    for elem in template_ds:
        if elem.keyword in ['PatientName', 'PatientID', 'PatientBirthDate', 'PatientSex',
                          'StudyInstanceUID', 'StudyID', 'StudyDate', 'StudyTime',
                          'AccessionNumber', 'ReferringPhysicianName']:
            setattr(ds, elem.keyword, elem.value)
    # Set series-specific attributes
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesNumber = "999"
    ds.Modality = "OT" 
    # Set PDF-specific attributes
    ds.EncapsulatedDocument = pdf_bytes
    ds.MIMETypeOfEncapsulatedDocument = "application/pdf"
    # Set encoding attributes
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    if dicomOutFilePath is not None:
        ds.save_as(dicomOutFilePath, write_like_original=False)
        print(f"Saved {dicomOutFilePath}")
    return ds
