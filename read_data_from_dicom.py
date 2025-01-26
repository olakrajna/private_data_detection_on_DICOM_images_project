import pydicom
import csv
import os

def save_dicom_attributes_to_tsv_2(ds, output_tsv_file="dicom_data.tsv"):

        sensitive_data_attributes = [
        ("Study Date", 'StudyDate'),
        ("Series Date", 'SeriesDate'),
        ("Acquisition Date", 'AcquisitionDate'),
        ("Content Date", 'ContentDate'),
        ("Acquisition Datetime", 'AcquisitionDatetime'),
        ("Study Time", 'StudyTime'),
        ("Series Time", 'SeriesTime'),
        ("Acquisition Time", 'AcquisitionTime'),
        ("Content Time", 'ContentTime'),
        ("Accession Number", 'AccessionNumber'),
        ("Patient's Name", 'PatientName'),
        ("Patient ID", 'PatientID'),
        ("Patient's Birth Date", 'PatientsBirthDate'),
        ("Patient's Birth Time", 'PatientsBirthTime'),
        ("Patient's Sex", 'PatientsSex'),
        ("Patient's Birth Name", 'PatientsBirthName'),
        ("Patient's Age", 'PatientsAge'),
        ("Patient's Address", 'PatientsAddress'),
        ("Patient's Mother's Birth Name", 'PatientsMothersBirthName'),
        ("Patient's Telephone Numbers", 'PatientsTelephoneNumbers'),
        ("Study ID", 'StudyID'),
        ("DateTime", 'DateTime'),
        ("Date", 'Date'),
        ("Time", 'Time'),
        ("Person Name", 'PersonName'),
    ]
        
        normal_attributes = [
    ("Specific Character Set", 'SpecificCharacterSet'),
    ("Image Type", 'ImageType'),
    ("Instance Creation Date", 'InstanceCreationDate'),
    ("Modality", 'Modality'),
    ("Manufacturer", 'Manufacturer'),
    ("Study Description", 'StudyDescription'),
    ("Series Description", 'SeriesDescription'),
    ("Manufacturer's Model Name", 'ManufacturerModelName'),
    ("Irradiation Event UID", 'IrradiationEventUID'),
    ("Patient Identity Removed", 'PatientIdentityRemoved'),
    ("De-identification Method", 'DeidentificationMethod'),
    ("Private Creator", 'PrivateCreator'),
    ("Body Part Examined", 'BodyPartExamined'),
    ("Scan Options", 'ScanOptions'),
    ("Slice Thickness", 'SliceThickness'),
    ("KVP", 'KVP'),
    ("Spacing Between Slices", 'SpacingBetweenSlices'),
    ("Data Collection Diameter", 'DataCollectionDiameter'),
    ("Software Versions", 'SoftwareVersions'),
    ("Protocol Name", 'ProtocolName'),
    ("Reconstruction Diameter", 'ReconstructionDiameter'),
    ("Distance Source to Detector", 'DistanceSourceToDetector'),
    ("Distance Source to Patient", 'DistanceSourceToPatient'),
    ("Gantry/Detector Tilt", 'GantryDetectorTilt'),
    ("Table Height", 'TableHeight'),
    ("X-Ray Tube Current", 'XRayTubeCurrent'),
    ("Exposure", 'Exposure'),
    ("Filter Type", 'FilterType'),
    ("Convolution Kernel", 'ConvolutionKernel'),
    ("Patient Position", 'PatientPosition'),
    ("Acquisition Type", 'AcquisitionType'),
    ("Revolution Time", 'RevolutionTime'),
    ("Single Collimation Width", 'SingleCollimationWidth'),
    ("Total Collimation Width", 'TotalCollimationWidth'),
    ("Table Speed", 'TableSpeed'),
    ("Table Feed per Rotation", 'TableFeedPerRotation'),
    ("Spiral Pitch Factor", 'SpiralPitchFactor'),
    ("Exposure Modulation Type", 'ExposureModulationType'),
    ("Estimated Dose Saving", 'EstimatedDoseSaving'),
    ("CTDIvol", 'CTDIvol'),
    ("Study Instance UID", 'StudyInstanceUID'),
    ("Series Instance UID", 'SeriesInstanceUID'),
    ("Series Number", 'SeriesNumber'),
    ("Acquisition Number", 'AcquisitionNumber'),
    ("Instance Number", 'InstanceNumber'),
    ("Image Position (Patient)", 'ImagePositionPatient'),
    ("Image Orientation (Patient)", 'ImageOrientationPatient'),
    ("Frame of Reference UID", 'FrameOfReferenceUID'),
    ("Position Reference Indicator", 'PositionReferenceIndicator'),
    ("Slice Location", 'SliceLocation'),
    ("Image Comments", 'ImageComments'),
    ("Samples per Pixel", 'SamplesPerPixel'),
    ("Photometric Interpretation", 'PhotometricInterpretation'),
    ("Rows", 'Rows'),
    ("Columns", 'Columns'),
    ("Pixel Spacing", 'PixelSpacing'),
    ("Bits Allocated", 'BitsAllocated'),
    ("Bits Stored", 'BitsStored'),
    ("High Bit", 'HighBit'),
    ("Pixel Representation", 'PixelRepresentation'),
    ("Longitudinal Temporal Information Modified", 'LongitudinalTemporalInformationModified'),
    ("Window Center", 'WindowCenter'),
    ("Window Width", 'WindowWidth'),
    ("Rescale Intercept", 'RescaleIntercept'),
    ("Rescale Slope", 'RescaleSlope'),
]

        attributes_to_save = []
        for name, tag in sensitive_data_attributes:
            if tag in ds and ds.get(tag):
                attributes_to_save.append((name, getattr(ds, tag), 1)) 

        for name, tag in normal_attributes:
            if tag in ds and ds.get(tag):
                attributes_to_save.append((name, getattr(ds, tag), 0)) 

        if attributes_to_save:
            with open(output_tsv_file, mode='a', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                if file.tell() == 0:
                    writer.writerow(["tags", "value", "label"])  

                writer.writerows(attributes_to_save) 

            print(f"Dane zapisano do {output_tsv_file}")
        else:
            print("Brak dostępnych atrybutów do zapisania.")


dicom_folder = r'case2'
dicom_files = [os.path.join(dicom_folder, f) for f in os.listdir(dicom_folder) if f.endswith(".dcm")]

for dicom_file in dicom_files:
    ds = pydicom.dcmread(dicom_file) 
    save_dicom_attributes_to_tsv_2(ds)
