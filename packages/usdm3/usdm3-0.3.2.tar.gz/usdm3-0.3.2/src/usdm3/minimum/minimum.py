from usdm3.api.wrapper import Wrapper
from usdm3.api.study import Study
from usdm3.api.study_title import StudyTitle
from usdm3.api.code import Code
from usdm3.api.study_protocol_document_version import StudyProtocolDocumentVersion
from usdm3.api.study_protocol_document import StudyProtocolDocument
from usdm3.api.study_version import StudyVersion
from usdm3.api.study_identifier import StudyIdentifier
from usdm3.api.organization import Organization
from usdm3.base.api_instance import APIInstance
from usdm3.base.id_manager import IdManager
from usdm3.__version__ import __model_version__, __package_version__
from uuid import uuid4


class Minimum:
    @classmethod
    def minimum(cls, title: str, identifier: str, version: str) -> "Wrapper":
        """
        Create a minimum study with the given title, identifier, and version.

        """
        api_classes = [
            Study,
            StudyTitle,
            StudyProtocolDocumentVersion,
            StudyProtocolDocument,
            StudyVersion,
            StudyIdentifier,
            Organization,
            Code,
            "Wrapper",
        ]

        id_manager = IdManager(api_classes)
        api_instance = APIInstance(id_manager)
        cdisc_code_system = "cdisc.org"
        cdisc_code_system_version = "2023-12-15"

        # Define the codes to be used in the study
        title_type = api_instance.create(
            Code,
            {
                "code": "C207616",
                "codeSystem": cdisc_code_system,
                "codeSystemVersion": cdisc_code_system_version,
                "decode": "Official Study Title",
            },
        )
        organization_type = api_instance.create(
            Code,
            {
                "code": "C70793",
                "codeSystem": cdisc_code_system,
                "codeSystemVersion": cdisc_code_system_version,
                "decode": "Clinical Study Sponsor",
            },
        )
        doc_status = api_instance.create(
            Code,
            {
                "code": "C25425",
                "codeSystem": cdisc_code_system,
                "codeSystemVersion": cdisc_code_system_version,
                "decode": "Approved",
            },
        )

        study_title = api_instance.create(
            StudyTitle, {"text": title, "type": title_type}
        )

        # Define the protocol documents
        study_protocol_document_version = api_instance.create(
            StudyProtocolDocumentVersion,
            {"protocolVersion": version, "protocolStatus": doc_status},
        )
        study_protocol_document = api_instance.create(
            StudyProtocolDocument,
            {
                "name": "PROTOCOL",
                "label": "Study Protocol",
                "description": "The study protocol document",
                "versions": [study_protocol_document_version],
            },
        )

        # Define the organization and the study identifier
        organization = api_instance.create(
            Organization,
            {
                "name": "Sponsor",
                "organizationType": organization_type,
                "identifier": "To be provided",
                "identifierScheme": "To be provided",
                "legalAddress": None,
            },
        )
        study_identifier = api_instance.create(
            StudyIdentifier,
            {"studyIdentifier": identifier, "studyIdentifierScope": organization},
        )

        # Define the study version
        study_version = api_instance.create(
            StudyVersion,
            {
                "versionIdentifier": "1",
                "rationale": "To be provided",
                "titles": [study_title],
                "studyDesigns": [],
                "documentVersionId": study_protocol_document_version.id,
                "studyIdentifiers": [study_identifier],
            },
        )
        study = api_instance.create(
            Study,
            {
                "id": str(uuid4()),
                "name": "Study",
                "label": "",
                "description": "",
                "versions": [study_version],
                "documentedBy": study_protocol_document,
            },
        )

        # Return the wrapper for the study
        return api_instance.create(
            Wrapper,
            {
                "study": study,
                "usdmVersion": __model_version__,
                "systemName": "Python USDM3 Package",
                "systemVersion": __package_version__,
            },
        )
