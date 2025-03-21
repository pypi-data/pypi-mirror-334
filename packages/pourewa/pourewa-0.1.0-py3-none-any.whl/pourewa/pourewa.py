#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 10 November 2016

@author: Fraser M. Callaghan

Orthanc DB Management

    # Orthanc - A Lightweight, RESTful DICOM Store
    # Copyright (C) 2012-2016 Sebastien Jodogne, Medical Physics
    # Department, University Hospital of Liege, Belgium
    #
    # This program is free software: you can redistribute it and/or
    # modify it under the terms of the GNU General Public License as
    # published by the Free Software Foundation, either version 3 of the
    # License, or (at your option) any later version.
    # 
    # This program is distributed in the hope that it will be useful, but
    # WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    # General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
import os
import sys
import socket
import argparse
from datetime import datetime
import time
import json
from pourewa import OrthancRestToolbox as RestToolbox
from pourewa import helpers
from pourewa import pdf2dicom


DEFAULT_TABLE_HEADERS = ["ID", "PatientName", "PatientID", "PatientBirthDate", "PatientSex", 
          "StudyDate", "StudyID", "StudyDescription", "InstitutionName", "StudyInstanceUID", "IsStable", "NumberOfDICOMS"]
# ==========================================================
class OrthancDBManager(object):
    @classmethod
    def OrthancTimeToDateTime(cls, orthancTime):
        return datetime.strptime(orthancTime, '%Y%m%dT%H%M%S')
    
    
    def __init__(self, URL):
        self.url = URL
        self.VERBOSE = True
    
    def __str__(self):
        return f'Orthanc DB Manager at {self.url}'
    # -----------------------------------------------------
    # METHODS
    # -----------------------------------------------------
    def getAllDB_Subjects(self):
        """ return list of subjects"""
        try:
            return RestToolbox.DoGet('%s/patients'%(self.url))
        except Exception as e:
            print(f'ERROR from RestToolbox.DoGet: {e}')
            sys.exit(1)
        
    def getAllDB_Studies(self):
        """ retrun list of studies """
        try:
            return RestToolbox.DoGet('%s/studies'%(self.url))
        except Exception as e:
            print(f'ERROR from RestToolbox.DoGet: {e}')
            sys.exit(1)
        
    def getAllDB_Names(self):
        allNames = []
        for iSubject in self.getAllDB_Subjects():
            infos = RestToolbox.DoGet('%s/patients/%s' % (self.url, iSubject))
            allNames.append([infos['ID'],infos['MainDicomTags']['PatientName'].lower()])
        return allNames

    def findPatientName(self, searchName):
        """ Return list of [studyID, Name] for names matching name"""
        matchingNames = []
        for iStudy in self.getAllDB_Studies():
            infos = self.getStudyInfosForID(iStudy)
            name = infos['PatientMainDicomTags']['PatientName'].lower()
            if searchName.lower() in name:
                matchingNames.append([infos['ID'], name])
        return matchingNames
    
    def getStudiesWithinDates(self, sDate, eDate, LAST_UPDATED=False):
        studyIDsOut = []
        for iStudyID in self.getAllDB_Studies():
            study = self.getStudyInfosForID(iStudyID)
            if LAST_UPDATED:
                qDate = study['LastUpdate'][:8]
            else:
                qDate = self.getTag(study, 'StudyDate')[:8]
            try:
                if (int(qDate) >= int(sDate)) and int(qDate) <= int(eDate):
                    studyIDsOut.append(iStudyID)
            except ValueError: # not int - prob no date from ANON - skip
                pass
        return studyIDsOut

    def getSmallTagDictForEachStudy(self, studyIDList=None):
        studiesDict = {}
        for iSubject in self.getAllDB_Subjects():
            infos = self.getSubjectInfosForID(iSubject)
            for iStudyID in infos['Studies']:
                if studyIDList is not None:
                    if iStudyID not in studyIDList:
                        continue
                sInfos = self.getStudyInfosForID(iStudyID)
                studiesDict[iStudyID] = {'PatientName':infos['MainDicomTags']['PatientName'],
                                            'PatientID':infos['MainDicomTags']['PatientID'],
                                            'StudyID':sInfos['MainDicomTags']['StudyID'],
                                            'StudyDate':sInfos['MainDicomTags']['StudyDate'],
                                            'StudyInstanceUID':sInfos['MainDicomTags']['StudyInstanceUID']}
        return studiesDict

    def getSubjectInfosForID(self, ID):
        return RestToolbox.DoGet('%s/patients/%s' % (self.url, ID))
    
    def getStudyInfosForID(self, ID):
        infoDict = RestToolbox.DoGet('%s/studies/%s' % (self.url, ID))
        instanceIDs = []
        for iSeries in infoDict['Series']:
            instanceIDs += self.getSeriesInfosForID(iSeries)['Instances']
        infoDict["NumberOfDICOMS"] = len(instanceIDs)
        return infoDict
    
    def getSeriesInfosForID(self, ID):
        return RestToolbox.DoGet('%s/series/%s' % (self.url, ID))
    
    def getInstanceInfosForID(self, ID):
        return RestToolbox.DoGet('%s/instances/%s' % (self.url, ID))
    
    def getDataForStudy(self, ID):
        return RestToolbox.DoGet('%s/patients/%s/archive' % (self.url, ID))
    
    def getTotalNumberOfDICOMS(self):
        return len(RestToolbox.DoGet('%s/instances/' % (self.url)))

    def exportStudyToZip(self, studyID, outputDir):
        """ Will export study to zip - with organised name """
        infos = self.getStudyInfosForID(studyID)
        if not infos['IsStable']:
            raise NotStableError(infos)
        subjectData = RestToolbox.DoGet('%s/studies/%s/archive' % (self.url, studyID))
        folderOut = self.getOutputFolderNameForStudyID(studyID)
        zipOut = os.path.join(outputDir,'%s.zip'%(folderOut))
        with open(zipOut, 'wb') as fid:
            fid.write(subjectData)
        return zipOut
        
    def deleteStudy(self, studyID):
        studyInfos = self.getStudyInfosForID(studyID)
        if not studyInfos['IsStable']:
            raise NotStableError(studyInfos)
        return RestToolbox.DoDelete('%s/studies/%s'%(self.url, studyID))
        
    def deleteSeries(self, seriesID):
        seriesInfos = self.getSeriesInfosForID(seriesID)
        if not seriesInfos['IsStable']:
            raise NotStableError(seriesInfos)
        return RestToolbox.DoDelete('%s/series/%s'%(self.url, seriesID))

    def anonymizeStudy(self, studyID, jsonObj=None):
        if jsonObj is None:
            keepDict = {'Keep':['SeriesDescription',
                                    'StudyDescription']}
            jsonObj = json.dumps(keepDict, indent = 4)
        returnDict = RestToolbox.DoPost('%s/studies/%s/anonymize'%(self.url, studyID), jsonObj)
        newID = returnDict['ID']
        maxIt = 30
        for _ in range(maxIt):
            if self.isStudyStable(newID):
                break
            time.sleep(5.0) # Check every 5sec if stable (max 150 secs). 
        return returnDict

    def isStudyStable(self, studyID):
        studyInfos = self.getStudyInfosForID(studyID)
        return studyInfos['IsStable']
    
    def getSubjectIDFromStudyID(self, studyID):
        studyInfos = self.getStudyInfosForID(studyID)
        return studyInfos['ParentPatient']

    def getTagFromLevel(self, studyID, tag, level):
        """
        level = 'Patient' | 'Study' | 'Series'
        If 'Series' then return string from list as "|".join([...])
        """
        if level == 'Patient':
            infos = self.getSubjectInfosForID(self.getSubjectIDFromStudyID(studyID))
            return self.getTag(infos, tag)
        elif level == 'Study':
            infos = self.getStudyInfosForID(studyID)
            infos["MainDicomTags"].update(infos["PatientMainDicomTags"]) # flatten PatientMainDicomTags into main dict to help query
            return self.getTag(infos, tag)
        elif level == 'Series':
            return "|".join([self.getTag(self.getSeriesInfosForID(iSeries), tag) for iSeries in self.getAllSeriesForStudyID(studyID)])
        else:
            raise ValueError('Incorrect useage')


    def getTag(self, resourceInfos, tag):
        if ('MainDicomTags' in resourceInfos and
            tag in resourceInfos['MainDicomTags']):
            return resourceInfos['MainDicomTags'][tag]
        else:
            return 'unknown'
    
    def getListOfInstanceIDForStudy(self, studyID):
        studyInfos = self.getStudyInfosForID(studyID)
        instanceIDs = []
        for iSeries in studyInfos['Series']:
            instanceIDs += self.getSeriesInfosForID(iSeries)['Instances']
        return instanceIDs
    
    def getListOfSeriesIDForStudy(self, studyID):
        return self.getStudyInfosForID(studyID)['Series']
    
    def exportInstanceToFileName(self, instanceID, fileName):
        try:
            dcm = RestToolbox.DoGet(f'{self.url}/instances/{instanceID}/file')
        except Exception:
            return None
        with open(fileName, 'wb') as g:
            g.write(dcm)
        return fileName

    def exportInstancesToRemote(self, instanceIDList, remoteName):
        for iInstance in instanceIDList:
            res = RestToolbox.DoPost(f'{self.url}/modalities/{remoteName}/store', iInstance)
        return res

    def exportSeriesToRemote(self, seriesID, remoteName):
        instanceIDs = self.getSeriesInfosForID(seriesID)['Instances']
        return self.exportInstancesToRemote(instanceIDs, remoteName)

    def exportStudyToRemote(self, studyID, remoteName):
        seriesID = self.getListOfSeriesIDForStudy(studyID)
        for iSeries in seriesID:
            res = self.exportSeriesToRemote(iSeries, remoteName)
        return res


    def exportSeriesToDirectoryStructure(self, seriesID, topDir, IM_NAME=False):  
        series = RestToolbox.DoGet(f'{self.url}/series/{seriesID}')  
        seN = self.getTag(series, 'SeriesNumber')
        seriesDirName = helpers.cleanString('SE%s_%s'%(seN, self.getTag(series, 'SeriesDescription')))
        instanceIDs = self.getSeriesInfosForID(seriesID)['Instances']
        parentDir = os.path.join(topDir, 'DATA', seriesDirName)
        try: # Copy the DICOM file to the target path
            os.makedirs(parentDir)
        except: # Already existing directory, ignore the error
            nFilesAlready = len(os.listdir(parentDir))
            if nFilesAlready >= len(instanceIDs):
                return None
        for iInstanceID in instanceIDs:
            instance = RestToolbox.DoGet(f'{self.url}/instances/{iInstanceID}')
            if IM_NAME:
                try:
                    fileName = f'IM{int(seN):05d}_{int(self.getTag(instance, "InstanceNumber")):05d}.dcm'
                except ValueError:
                    IM_NAME = False
                    fileName = f'{self.getTag(instance, "SOPInstanceUID")}.dcm'
            else:
                fileName = f'{self.getTag(instance, "SOPInstanceUID")}.dcm'
            fullFileName = os.path.join(parentDir, helpers.fixPath(fileName))
            self.exportInstanceToFileName(iInstanceID, fullFileName)
    
    def exportStudyToDirectory(self, studyID, outputDir, ADD_ExamID=False):
        studyInfos = self.getStudyInfosForID(studyID)
        if not studyInfos['IsStable']:
            raise NotStableError(studyInfos)
        # Construct a target path
        topDir = self.getOutputFolderNameForStudyID(studyID, ADD_ExamNum=ADD_ExamID)
        topDir = os.path.join(outputDir, topDir)
        seriesID = self.getListOfSeriesIDForStudy(studyID)
        for iSeries in seriesID:
            self.exportSeriesToDirectoryStructure(iSeries, topDir)
        return topDir

    def buildSummaryFile(self, studyID, outputDir):
        ff = '%s.txt'%(self.getOutputFolderNameForStudyID(studyID))
        fileOut = os.path.join(outputDir, ff)
        strOut = self.getStudySummary(studyID)
        with open(fileOut, 'w') as fid:
            fid.write(strOut)
        return fileOut
    
    def getStudies(self):
        allStudiesList = []
        for iStudyID in self.getAllDB_Studies():
            studyInfos = self.getStudyInfosForID(iStudyID)
            allStudiesList.append([iStudyID, 
                                    studyInfos['PatientMainDicomTags'].get('PatientID','Not Specified'),
                                    studyInfos['MainDicomTags'].get('StudyInstanceUID','Not Specified'),
                                    studyInfos['PatientMainDicomTags'].get('PatientName','Not Specified'),
                                    studyInfos['PatientMainDicomTags'].get('PatientBirthDate','Not Specified'),
                                    studyInfos['PatientMainDicomTags'].get('PatientSex','Not Specified'),
                                    studyInfos['MainDicomTags'].get('StudyDate','Not Specified'),
                                    studyInfos['MainDicomTags'].get('StudyID','Not Specified'),
                                    studyInfos['MainDicomTags'].get('StudyDescription','Not Specified'),
                                    studyInfos['MainDicomTags'].get('InstitutionName','Not Specified'),
                                    studyInfos['IsStable'],
                                    len(studyInfos['Series']),
                                    len(self.getListOfInstanceIDForStudy(iStudyID))])
        return allStudiesList
    
    def getStudySummaryLine(self, studyID, headerLabels=DEFAULT_TABLE_HEADERS):
        studyInfos = self.getStudyInfosForID(studyID)
        resList = []
        for i in headerLabels:
            try: 
                val = studyInfos['PatientMainDicomTags'][i]
            except KeyError:
                try:
                    val = studyInfos['MainDicomTags'][i]
                except KeyError:
                    val = studyInfos.get(i,'Not Specified')
            resList.append(str(val))
        strOut = ",".join(resList)
        return strOut

    def seNum_sortKey(self, seriesID):
        seriesInfos = self.getSeriesInfosForID(seriesID)
        return int(self.getTag(seriesInfos, 'SeriesNumber'))

    def getStudyDataDict(self, studyID):
        dataDict = {'StudyDescription': self.getTagFromLevel(studyID, 'StudyDescription', 'Study'),
                    'Series': []}
        listOfSeriesIDs = sorted(self.getListOfSeriesIDForStudy(studyID), key=self.seNum_sortKey)
        for iSeries in listOfSeriesIDs:
            seriesInfos = self.getSeriesInfosForID(iSeries)
            sd = self.getTag(seriesInfos, 'SeriesDescription')
            sN = int(self.getTag(seriesInfos, 'SeriesNumber'))
            nFiles = len(seriesInfos['Instances'])
            dataDict['Series'].append({'SeriesDescription': sd, 'SeriesNumber': sN, 'NumberImages': nFiles})
        return dataDict

    def getStudySummary(self, studyID, headerLabels=DEFAULT_TABLE_HEADERS):
        strOut = self.getStudySummaryLine(studyID, headerLabels)
        listOfSeriesIDs = sorted(self.getListOfSeriesIDForStudy(studyID), key=self.seNum_sortKey)
        nTot = 0
        strOut += '  %-50s | %s\n'%('SeriesDescription', 'nImages')
        for iSeries in listOfSeriesIDs:
            seriesInfos = self.getSeriesInfosForID(iSeries)
            seriesDirName = helpers.cleanString('SE%s_%s'%(self.getTag(seriesInfos, 'SeriesNumber'), 
                                                    self.getTag(seriesInfos, 'SeriesDescription')))
            nFiles = len(seriesInfos['Instances'])
            strOut += '  %-50s | %d\n'%(seriesDirName, nFiles)
            nTot += nFiles
        strOut += 'Total | %d\n'%(nTot)
        return strOut
    
    def getSubjectSummaryDict(self, SubjectIDsList=[]):
        summaryDict = {}
        for iSubject in self.getAllDB_Subjects():
            if len(SubjectIDsList) > 0:
                if iSubject not in SubjectIDsList:
                    continue
            infos = self.getSubjectInfosForID(iSubject)
            summaryDict[iSubject] = [self.getStudySummary(studyID) for studyID in infos['Studies']]
        return summaryDict
    
    def getStudySummaryStr(self, studyIDsList=[]):
        summaryStr = ''
        for iStudyID in studyIDsList:
            summaryStr += self.getStudySummary(iStudyID)
        return summaryStr
    
    def getStudySummaryStrAll(self):
        summaryStr = ''
        for iStudyID in self.getAllDB_Studies():
            summaryStr += self.getStudySummary(iStudyID)
        return summaryStr
    
    def getName(self, studyID):
        infos = self.getStudyInfosForID(studyID)
        name = infos['PatientMainDicomTags']['PatientName']
        names = name.split('^')
        SURNAME = helpers.cleanString(names[0]).upper()
        try:
            FIRST_NAME = helpers.cleanString(names[1]).upper()
        except IndexError:
            FIRST_NAME = 'Unknown'
        return '%s_%s'%(SURNAME, FIRST_NAME)

    def getStudyDate(self, studyID, AS_DATETIME):
        # ValueError if e.g. "unknown"
        infos = self.getStudyInfosForID(studyID)
        dos = infos['MainDicomTags']['StudyDate']
        if AS_DATETIME:
            return helpers.dbDateToDateTime(dos)
        return dos

    def getOutputFolderNameForStudyID(self, studyID, ADD_ExamNum=True):
        name = self.getName(studyID)
        try:
            dbDate = self.getStudyDate(studyID, AS_DATETIME=True)
            ss = '%s_%s'%(datetime.strftime(dbDate, '%y_%m_%d'), name)
        except ValueError: # Likely from anonymised study
            ss = 'Scan_%s'%(name) # Append 'Scan' incase name is empty
        if ADD_ExamNum:
            dbExamID = self.getTag(self.getStudyInfosForID(studyID), 'StudyID')
            ss = '%s_%s'%(ss, str(dbExamID))
        return ss
    
    def getAllSeriesForStudyID(self, studyID):
        return self.getStudyInfosForID(studyID)['Series']

    def getStudyIDForExamIDs(self, examNumberList):
        examNumberList = [str(i) for i in examNumberList]
        exStudyIDList = []
        for iStudyID in self.getAllDB_Studies():
            dbExamID = self.getTag(self.getStudyInfosForID(iStudyID), 'StudyID')
            if dbExamID in examNumberList:
                exStudyIDList.append([dbExamID,iStudyID])
        return exStudyIDList
    
    def getAllExamIDs_StudyIDs_list(self):
        exStudyIDList = []
        for iStudyID in self.getAllDB_Studies():
            dbExamID = self.getTag(self.getStudyInfosForID(iStudyID), 'StudyID')
            exStudyIDList.append([dbExamID,iStudyID])
        return exStudyIDList
    
    def getSeriesIDMatchingNumber(self, examNumber, seriesNumber):
        esList = self.getStudyIDForExamIDs([examNumber])[0]
        for iSeriesID in self.getAllSeriesForStudyID(esList[1]):
            if str(seriesNumber) == self.getTag(self.getSeriesInfosForID(iSeriesID), 'SeriesNumber'):
                return iSeriesID
            
    def getSeriesLastUpdate(self, examNumber, seriesNumber):
        esList = self.getStudyIDForExamIDs([examNumber])[0]
        for iSeriesID in self.getAllSeriesForStudyID(esList[1]):
            infos = self.getSeriesInfosForID(iSeriesID)
            if str(seriesNumber) == self.getTag(infos, 'SeriesNumber'):
                return OrthancDBManager.OrthancTimeToDateTime(infos['LastUpdate'])
    
    def getListOfLastUpdateForExam(self, examNumber):
        esList = self.getStudyIDForExamIDs([examNumber])[0]
        lastUpdateTimes = []
        for iSeriesID in self.getAllSeriesForStudyID(esList[1]):
            infos = self.getSeriesInfosForID(iSeriesID)
            lastUpdateTimes.append(OrthancDBManager.OrthancTimeToDateTime(infos['LastUpdate']))
        return lastUpdateTimes
    
    def getInstancesForExamSeries(self, examNumber, seriesNumber):
        try:
            seriesID = self.getSeriesIDMatchingNumber(examNumber, seriesNumber)
            return self.getSeriesInfosForID(seriesID)['Instances']
        except Exception as e:
            if str(e) == '404':
                return []
            else:
                raise e

    def getFirstInstanceForExamSeries(self, examNumber, seriesNumber):
        return self.getInstancesForExamSeries(examNumber, seriesNumber)[0]
    
    def getTodaysStudies(self, LAST_UPDATE=False):
        timeNow = datetime.now()
        return self.getStudiesWithinDates(timeNow.strftime('%Y%m%d'), timeNow.strftime('%Y%m%d'), LAST_UPDATE)
    
    def _uploadFile(self,path):
        with open(path, "r", newline="", encoding='latin') as f:
            content = f.read()#.decode("UTF-8")
        return RestToolbox.DoPost('%s/instances' % (self.url), content)
    
    def uploadDirectory(self, dirName, DEBUG=False, IGNORE_JSONS=True):
        # Recursively upload a directory
        count, skipped, alreadyPresent = 0, 0, 0
        for root, _, files in os.walk(dirName):
            if DEBUG:
                print(f'{helpers.getDateNow()} : {root} : {len(os.listdir(root))}')
            for f in files:
                if IGNORE_JSONS and (f.endswith('json')):
                    continue
                res = self._uploadFile(os.path.join(root, f))
                if res['Status'] == 'Success':
                    count += 1
                elif res['Status'] == 'AlreadyStored':
                    alreadyPresent += 1
                else:
                    skipped += 1
        if self.VERBOSE:
            print(f'Upload from {dirName}: {count} images added, {alreadyPresent} already present, {skipped} non-dicoms')
        return res
    
# ============================================================================
# ============================================================================
    
# ============================================================================
# ============================================================================
# Not Stable Error
class NotStableError(Exception):
    """ NotStableError
            Simple exception for when a study is not stable - still transferring """
    def __init__(self, infos):
        self.infos = infos
        
    def __str__(self):
        return 'Error ID %s (type: %s) is not stable'%(self.infos['ID'], self.infos['Type'])
    

# =============================================================================
# =============================================================================
def getDBStudyIDs_fromArgs(args, ODB):
    db_studyIDs = []
    if args.ALL_STUDIES:
        db_studyIDs = ODB.getAllDB_Studies()

    else:
        esListAt = []
        db_studyIDs += args.StudyIDs
        if args.patientName is not None:
            esListAt += ODB.findPatientName(args.patientName)
            for i in esListAt:
                db_studyIDs.append(i[0])
        if len(args.examNumberToSearchList) > 0:
            esListAt += ODB.getStudyIDForExamIDs(args.examNumberToSearchList)
            for i in esListAt:
                db_studyIDs.append(i[0])
        
        if len(args.dates) == 2:
            esListAt = ODB.getStudiesWithinDates(args.dates[0], args.dates[1])
            for i in esListAt:
                db_studyIDs.append(i)
        
        if len(args.tag) == 2:
            for i in ODB.getAllDB_Studies():
                val = ODB.getTagFromLevel(i, args.tag[0], 'Study')
                if args.tag[1].lower() in val.lower():
                    db_studyIDs.append(i)

    db_studyIDs = list(set(db_studyIDs))
    #
    return db_studyIDs




def run(args):
    # --------------------------------------------------------------------------
    DB_URL = f'http://{args.URL}:{args.PORT}/{args.EXPOSED}'
    ODB = OrthancDBManager(DB_URL)
    print(ODB)

    if args.TEST_LIVE:
        try: 
            SS = ODB.getAllDB_Studies()
            print(f'ORTHANC LIVE ({len(SS)} studies)')
        except socket.error:
            print('ORTHANC NOT LIVE')
    #
    if args.INFO:
        try: 
            SS = ODB.getAllDB_Studies()
            nDICOMS = ODB.getTotalNumberOfDICOMS()
            print(f'ORTHANC LIVE: {len(SS)} studies, {nDICOMS} total images')
        except socket.error:
            print('ORTHANC NOT LIVE')
    #
    db_studyIDs = getDBStudyIDs_fromArgs(args, ODB)
    print(f"Querying {len(db_studyIDs)} studies")
    print(" ")
    if args.TO_PRINT_SUMMARY:
        print(",".join(DEFAULT_TABLE_HEADERS))
        for iStudy in db_studyIDs:
            print(ODB.getStudySummaryLine(iStudy, DEFAULT_TABLE_HEADERS))
    if args.TO_PRINT_INFO_FULL:
        for iStudy in db_studyIDs:
            print(ODB.getStudySummary(iStudy, DEFAULT_TABLE_HEADERS))
            print('')

    if args.TO_EXPORT:
        if args.outputDir is None:
            sys.exit('ERROR: Need outputDir to export to.')
        if len(db_studyIDs) == 0:
            sys.exit('ERROR: Need Exam ID(s) to export.')
        print(f"EXPORTING {len(db_studyIDs)} studies to {args.outputDir}")
        for iStudy in db_studyIDs:
            if ODB.isStudyStable(iStudy):
                ODB.exportStudyToDirectory(iStudy, args.outputDir)
            else:
                print(f"WARNING: {iStudy} is not stable. Skipping.")

    if args.TO_PUSH is not None:
        if len(args.StudyIDs) == 0:
            sys.exit('ERROR: Need Study ID(s) to push.')
        print(f"PUSHING {len(db_studyIDs)} studies to {args.TO_PUSH}")
        for iStudy in db_studyIDs:
            if ODB.isStudyStable(iStudy):
                ODB.exportStudyToRemote(iStudy, args.TO_PUSH)
            else:
                print(f"WARNING: {iStudy} is not stable. Skipping.")

    if args.TO_DELETE:
        if len(db_studyIDs) == 0:
            sys.exit('ERROR: Need Study ID(s) to delete.')
        print(f"DELETING {len(db_studyIDs)} studies")
        for iStudy in db_studyIDs:
            if ODB.isStudyStable(iStudy):
                ODB.deleteStudy(iStudy)
            else:
                print(f"WARNING: {iStudy} is not stable. Skipping.")
            
    if args.loadDirectory:
        if not os.path.isdir(args.loadDirectory):
            sys.exit('ERROR: Directory does not exist')
        ODB.uploadDirectory(args.loadDirectory, args.DEBUG)

    if args.loadPDF:
        if not os.path.isfile(args.loadPDF):
            sys.exit('ERROR: PDF file does not exist')
        workingDir = os.path.dirname(args.loadPDF)
        cleanUpFiles = []
        if args.loadPDFDCM is None:
            if len(db_studyIDs) == 0:
                sys.exit('ERROR: Need a DICOM template to base pdf-2-dicom off (provide this or -s or query with -pdf)')
            elif len(db_studyIDs) != 1:
                sys.exit(f'ERROR: Found multiple ({len(db_studyIDs)}) potential studies from query - result must be 1 study')
            else:
                # Found one study - downlod a temp file of first instance in first series.
                studyInfos = ODB.getStudyInfosForID(db_studyIDs[0])
                instanceIDs = []
                for iSeries in studyInfos['Series']:
                    instanceIDs += ODB.getSeriesInfosForID(iSeries)['Instances']
                    break
                instanceID = instanceIDs[0]
                templateDCM = os.path.join(workingDir, "template.dcm")
                args.loadPDFDCM = ODB.exportInstanceToFileName(instanceID, templateDCM)
                cleanUpFiles.append(templateDCM)
        elif not os.path.isfile(args.loadPDFDCM):
            sys.exit('ERROR: DICOM template does not exist - pass a path to a DICOM file via -pdfDCM or query a study')
        dicomOutputTEMP = args.loadPDF.replace('.pdf', '.dcm')
        pdf2dicom.pdf_to_dicom(args.loadPDF, args.loadPDFDCM, dicomOutputTEMP)
        ODB._uploadFile(dicomOutputTEMP)
        cleanUpFiles.append(dicomOutputTEMP)
        for f in cleanUpFiles:
            os.remove(f)

# =============================================================================
def main():

    # --------------------------------------------------------------------------
    #  ARGUMENT PARSING
    # --------------------------------------------------------------------------
    ap = argparse.ArgumentParser(description='Orthanc DB Manager. Note, defaults defined in OrthancManager.conf ')

    groupSP = ap.add_argument_group('Script parameters')
    groupSP.add_argument('-u',dest='URL',help='URL of database',type=str,default=helpers.ORTHANC_URL)
    groupSP.add_argument('-p',dest='PORT',help='PORT of database',type=int,default=helpers.ORTHANC_PORT)
    groupSP.add_argument('-exposed',dest='EXPOSED',help='Path exposed by nginx',type=str,default=helpers.ORTHANC_EXPOSED)
    groupSP.add_argument('-n',dest='patientName',help='patient name to search for',type=str,default=None)
    groupSP.add_argument('-f',dest='examNumberToSearchList',help='exam IDs of interest (Scanner assigned)',nargs='*',type=str,default=[])
    # groupSP.add_argument('-i',dest='SubjectID',help='SubjectID - to list studies',type=str,default=None)
    groupSP.add_argument('-s',dest='StudyIDs',help='Study IDs list',nargs='*',type=str,default=[])
    groupSP.add_argument('-D',dest='TO_DELETE',help='To delete subject',action='store_true')
    groupSP.add_argument('-I',dest='TO_PRINT_INFO_FULL',help='To print full info',action='store_true')
    groupSP.add_argument('-S',dest='TO_PRINT_SUMMARY',help='To print summary',action='store_true')
    groupSP.add_argument('-A',dest='ALL_STUDIES',help='To use all STUDIES',action='store_true')
    groupSP.add_argument('-TL',dest='TEST_LIVE',help='test that live',action='store_true')
    groupSP.add_argument('-INFO',dest='INFO',help='return DB info',action='store_true')
    groupSP.add_argument('-E',dest='TO_EXPORT',help='To export subject to directory',action='store_true')
    groupSP.add_argument('-PUSH',dest='TO_PUSH',help='To push to remote (named modality in e.g. Orthanc.json)',type=str, default=None)
    groupSP.add_argument('-l',dest='loadDirectory',help='To load a directory recursively',type=str, default=None)
    groupSP.add_argument('-pdf',dest='loadPDF',help='To load a PDF file and convert to DICOM (will add to study specified by -s or a query)',type=str, default=None)
    groupSP.add_argument('-pdfDCM',dest='loadPDFDCM',help='A DICOM template to base pdf-2-dicom off (provide this or -s or query with -pdf)',type=str, default=None)
    groupSP.add_argument('-DEBUG',dest='DEBUG',help='debug (see *.conf file)',action='store_true', default=helpers.DEBUG)
    groupSP.add_argument('-Z',dest='TO_ZIP',help='To export subject to zip',action='store_true')
    groupSP.add_argument('-o',dest='outputDir',help='Output directory for export', type=str, default=None)
    groupSP.add_argument('-d',dest='dates',help='Dates to search within - -can be combined with other actions, alone will print studyIDs YYYMMDD', nargs='+', type=str, default=[])
    groupSP.add_argument('-tag',dest='tag',help='Find studies based on tag-value pair', nargs=2, type=str, default=[])
    ##
    
    argsA = ap.parse_args()
    run(argsA)
    




# =============================================================================
# =============================================================================
# S T A R T
#    
if __name__ == '__main__':
    main()
    
