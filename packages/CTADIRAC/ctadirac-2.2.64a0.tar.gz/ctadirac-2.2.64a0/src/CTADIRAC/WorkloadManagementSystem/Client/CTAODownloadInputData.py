""" Download Input Data specific to CTAO
    It derived voName from lfn to download both lfns starting with /vo.cta.in2p3.fr and /ctao
"""
import os

from DIRAC import S_ERROR, S_OK
from DIRAC.Core.Utilities.ReturnValues import returnSingleResult
from DIRAC.Resources.Storage.StorageElement import StorageElement
from DIRAC.WorkloadManagementSystem.Client.DownloadInputData import DownloadInputData


class CTAODownloadInputData(DownloadInputData):
    """
    retrieve InputData LFN from localSEs (if available) or from elsewhere.
    """

    #############################################################################
    def __init__(self, argumentsDict):
        """Standard constructor"""
        DownloadInputData.__init__(self, argumentsDict)

    def _downloadFromSE(self, lfn, seName, reps, guid):
        """Download a local copy from the specified Storage Element."""
        if not lfn:
            return S_ERROR("LFN not specified: assume file is not at this site")

        self.log.verbose("Attempting to download file", f"{lfn} from {seName}:")

        downloadDir = self._DownloadInputData__getDownloadDir()
        fileName = os.path.basename(lfn)
        for localFile in (
            os.path.join(os.getcwd(), fileName),
            os.path.join(downloadDir, fileName),
        ):
            if os.path.exists(localFile):
                self.log.info(f"File already exists locally {fileName} as {localFile}")
                fileDict = {
                    "turl": "LocalData",
                    "protocol": "LocalData",
                    "se": seName,
                    "pfn": reps[seName],
                    "guid": guid,
                    "path": localFile,
                }
                return S_OK(fileDict)

        localFile = os.path.join(downloadDir, fileName)
        se = StorageElement(seName)
        voName = lfn.split("/")[1]
        se.vo = voName
        result = returnSingleResult(se.getFile(lfn, localPath=downloadDir))
        if not result["OK"]:
            self.log.warn(
                f"Problem getting lfn {lfn} from {seName}:\n{result['Message']}"
            )
            self.__cleanFailedFile(lfn, downloadDir)
            return result

        if os.path.exists(localFile):
            self.log.verbose(
                "File successfully downloaded locally", f"({lfn} to {localFile})"
            )
            fileDict = {
                "turl": "Downloaded",
                "protocol": "Downloaded",
                "se": seName,
                "pfn": reps[seName],
                "guid": guid,
                "path": localFile,
            }
            return S_OK(fileDict)
        else:
            self.log.warn("File does not exist in local directory after download")
            return S_ERROR("OK download result but file missing in current directory")


# EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#EOF#
