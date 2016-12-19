from datetime import date
from lxml import etree
import re
import dateutil.parser
import psycopg2
from xbrl_fundamentals import FundamentantalAccountingConcepts

import constants as c
import utils

class XBRL:

    def __init__(self, XBRLInstanceLocation, opener=None):
        self.XBRLInstanceLocation = XBRLInstanceLocation
        self.fields = {}
        self.tags = []
        if opener:
            # Allow us to read directly from a ZIP archive without extracting
            # the whole thing.
            self.EntireInstanceDocument = opener(XBRLInstanceLocation,'r').read()
        else:
            self.EntireInstanceDocument = open(XBRLInstanceLocation,'r').read()
            lst = [line for line in open(XBRLInstanceLocation,'r').read().splitlines()]
            #print(len(lst))
            #print lst
            try:
                for item in lst:
                #print(item)
                    if 'fsa:' or 'e:' in item:
                    #print item
                    #print('weeeee')
                    
                        str = item
                        while str[0] == ' ':
                            str = str[1:]
                        if str[0] == '<': self.tags.append(str.split(' ')[0][1:])
                        else: self.tags.append(str.split(' ')[0])
                    else:continue
            except:
                print('ollololo')
                l = []
                self.tags=[]
                for item in lst:
                    items = item.split('><')
                    for element in items:
                        l.append(element)
                for item in l:
                    try:
                        if 'e:' or 'd:' or 'c:' or 'f:' in item:
                            if item[0] == '<':
                                item = item.replace('<','')
                            if item[0] == '/':
                                item = item.replace('/','')
                            if '>' in item:
                                item = item.split('>')[0]
                            if item[:2] == 'e:' or item[:2] == 'c:' or item[:2] == 'f:' or item[:2] == 'd:':
                                self.tags.append(item.split(' ')[0])
                    except:continue          
                        
                        
            
            print(len(self.tags))
            self.tags = list(set(self.tags))
            
            if len(lst) == 1:
                for item in lst:
                    items = item.split('><')
                for element in items:
                    if 'fsa:' or 'e:' in element:
                        str = element
                        self.tags.append(str.split(' ')[0])
                    else:continue
                    
                    
                    
            
            for item in self.tags:
                if item.split(':')[0] == 'fsa':
                    if 'Disclosure' in item: # NE RABOTAET UBERI DISCLOSURE ! ! ! 
                        #print(item)
                        self.tags.remove(item)
                    continue
                else:
                    #print(item)
                    self.tags.remove(item)
         
        self.oInstance = etree.fromstring(self.EntireInstanceDocument)
        self.ns = {}
        for k in self.oInstance.nsmap.keys():
            if k != None:
                self.ns[k] = self.oInstance.nsmap[k]
        self.ns['xbrli'] = 'http://www.xbrl.org/2003/instance'
        self.ns['xlmns'] = 'http://www.xbrl.org/2003/instance'
        self.GetBaseInformation()
        self.loadYear(0)
        
        self._context_start_dates = {}
        self._context_end_dates = {}

    def loadYear(self,yearminus=0):
        try:
            currentEnd = self.getNode("gsd:ReportingPeriodEndDate").text
        except: currentEnd = self.getNode("//c:ReportingPeriodEndDate[@contextRef]").text
        asdate = re.match('\s*(\d{4})-(\d{2})-(\d{2})\s*', currentEnd)
        if asdate:
            year = int(asdate.groups()[0]) - yearminus
            thisend = '%s-%s-%s' % (year,asdate.groups()[1],asdate.groups()[2])
            self.GetCurrentPeriodAndContextInformation(thisend)
            FundamentantalAccountingConcepts(self)
            return True
        else:
            #print(currentEnd, ' is not a date')
            return False
            
    def getNodeList(self, xpath, root=None):
        if root is None:
            root = self.oInstance
        oNodelist = root.xpath(xpath, namespaces=self.ns)
        return oNodelist
        
    def getNode(self,xpath,root=None):
        oNodelist = self.getNodeList(xpath,root)
        if len(oNodelist):
            return oNodelist[0]
        return None

    def iter_namespace(self, ns='us-gaap'):
        """
        Iterates over all namespace elements, yielding each one.
        """
        SeekConcept = '%s:*' % (ns,)
        node_list = self.getNodeList("//" + SeekConcept)# + "[@contextRef='" + ContextReference + "']")
        total = len(node_list)
        for node in node_list:
            yield node, total

    def GetFactValue(self, SeekConcept, ConceptPeriodType):
                
        factValue = None
            
        if ConceptPeriodType == c.INSTANT:
            ContextReference = self.fields['ContextForInstants']
        elif ConceptPeriodType == c.DURATION:
            ContextReference = self.fields['ContextForDurations']
        else:
            #An error occured
            return "CONTEXT ERROR"
        
        if not ContextReference:
            return None

        oNode = self.getNode("//" + SeekConcept + "[@contextRef='" + ContextReference + "']")
        if oNode is not None:
            factValue = oNode.text
            if 'nil' in oNode.keys() and oNode.get('nil')=='true':
                factValue=0
                #set the value to ZERO if it is nil
            #if type(factValue)==str:
            try:
                factValue = float(factValue)
            except:
                #print('couldnt convert %s=%s to string' % (SeekConcept,factValue)
                factValue = None
                pass
            
        return factValue

    def GetBaseInformation(self):
        #print(123,self.fields['ContextForDurations']
        #Registered Name
        try:
            oNode = self.getNode("//gsd:NameOfReportingEntity" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")
        except:
            try:oNode = self.getNode("//gsd:NameOfReportingEntity[@contextRef]")
            except:
                try:
                    oNode = self.getNode("//c:NameOfReportingEntity" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")
                    print oNode.text
                
                except:
                    oNode = self.getNode("//c:NameOfReportingEntity[@contextRef]")
                    print oNode.text
        print(123123123,oNode.text)
            #print(oNode)
                
        #oNode = self.getNode("//gsd:NameOfReportingEntity[@contextRef]")
        if oNode is not None:
            self.fields['EntityRegistrantName'] = oNode.text
        else:
            self.fields['EntityRegistrantName'] = "Registered name not found"

        #Fiscal year
        #oNode = self.getNode("gsd:ReportingPeriodEndDate[@contextRef]")        
        #if oNode is not None:
        #    self.fields['FiscalYear'] = oNode.text
        #else:
        #    self.fields['FiscalYear'] = "Fiscal year not found"

        #EntityCentralIndexKey
        try:
            oNode = self.getNode("//gsd:IdentificationNumberCvrOfReportingEntity" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")
        except:
            try:oNode = self.getNode("//gsd:IdentificationNumberCvrOfReportingEntity[@contextRef]")
            except:
                try:
                    oNode = self.getNode('//c:IdentificationNumberCvrOfReportingEntity" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")')
                    #print oNode.text

                except:
                    oNode = self.getNode("//c:IdentificationNumberCvrOfReportingEntity[@contextRef]")
                    #print oNode.text

        if oNode is not None:
            self.fields['EntityCentralIndexKey'] = oNode.text
        else:
            self.fields['EntityCentralIndexKey'] = "CIK not found"

        #EntityFilerCategory
        #oNode = self.getNode("//dei:EntityFilerCategory[@contextRef]")
        #if oNode is not None:
        #    self.fields['EntityFilerCategory'] = oNode.text
        #else:
        #    self.fields['EntityFilerCategory'] = "Filer category not found"

        #TradingSymbol
        #oNode = self.getNode("//dei:TradingSymbol[@contextRef]")
        #if oNode is not None:
        #    self.fields['TradingSymbol'] = oNode.text
        #else:
        #    self.fields['TradingSymbol'] = None

        #DocumentFiscalYearFocus
        #oNode = self.getNode("//dei:DocumentFiscalYearFocus[@contextRef]")
        #if oNode is not None:
        #    self.fields['DocumentFiscalYearFocus'] = oNode.text
        #else:
        #    self.fields['DocumentFiscalYearFocus'] = "Fiscal year focus not found"

        #DocumentFiscalPeriodFocus
        #oNode = self.getNode("//dei:DocumentFiscalPeriodFocus[@contextRef]")
        #if oNode is not None:
        #    self.fields['DocumentFiscalPeriodFocus'] = oNode.text
        #else:
        #    self.fields['DocumentFiscalPeriodFocus'] = "Fiscal period focus not found"
        
        #DocumentType

        try:
            oNode = self.getNode("//gsd:InformationOnTypeOfSubmittedReport" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")
        except:
            try:oNode = self.getNode("//gsd:InformationOnTypeOfSubmittedReport[@contextRef]")
            except:
                try:
                    oNode = self.getNode('//c:InformationOnTypeOfSubmittedReport" + "[@contextRef='" + self.fields['ContextForDurations'] + "']")')
                    #print oNode.text

                except:
                    oNode = self.getNode("//c:InformationOnTypeOfSubmittedReport[@contextRef]")
                    #print oNode.text

        if oNode is not None:
            self.fields['DocumentType'] = oNode.text.encode('ascii', 'ignore').decode('ascii')
        else:
            self.fields['DocumentType'] = "Fiscal period focus not found"
        
    def get_context_start_date(self, context_id):
        if context_id not in self._context_start_dates:
            node = self.getNode("//xbrli:context[@id='" + context_id + "']/xbrli:period/xbrli:startDate")
            if node is None:
                node = self.getNode("//xbrli:context[@id='" + context_id + "']/xbrli:period/xbrli:instant")
            dt = None
            if node is not None and node.text:
                #dt = date(*map(int, node.text.split('-')))
                dt = utils.str_to_date(node.text)
            self._context_start_dates[context_id] = dt
        return self._context_start_dates[context_id]

    def get_context_end_date(self, context_id):
        if context_id not in self._context_end_dates:
            node = self.getNode("//xbrli:context[@id='" + context_id + "']/xbrli:period/xbrli:endDate")
            dt = None
            if node is not None and node.text:
                #dt = date(*map(int, node.text.split('-')))
                dt = utils.str_to_date(node.text)
            self._context_end_dates[context_id] = dt
        return self._context_end_dates[context_id]
        
    def GetCurrentPeriodAndContextInformation(self, EndDate):
        #Figures out the current period and contexts for the current period instance/duration contexts

        self.fields['BalanceSheetDate'] = "ERROR"
        self.fields['IncomeStatementPeriodYTD'] = "ERROR"
        
        self.fields['ContextForInstants'] = "ERROR"
        self.fields['ContextForDurations'] = "ERROR"

        #This finds the period end date for the database table, and instant date (for balance sheet):        
        UseContext = "ERROR"
        #EndDate = self.getNode("//dei:DocumentPeriodEndDate").text
        #This is the <instant> or the <endDate>
        
        #Uses the concept ASSETS to find the correct instance context
        #This finds the Context ID for that end date (has correct <instant> date plus has no dimensions):    
        try:
            oNodelist2 = self.getNodeList("fsa:Assets | fsa:AssetsCurrent | fsa:LiabilitiesAndStockholdersEquity")
        except: oNodelist2 = self.getNodeList("e:Assets | e:AssetsCurrent | e:LiabilitiesAndStockholdersEquity")
        #Nodelist of all the facts which are us-gaap:Assets
        for i in oNodelist2:
            #print i.XML
            
            ContextID = i.get('contextRef') 
            ContextPeriod = self.getNode("//xbrli:context[@id='" + ContextID + "']/xbrli:period/xbrli:instant").text
            #print ContextPeriod
            
            #Nodelist of all the contexts of the fact us-gaap:Assets
            oNodelist3 = self.getNodeList("//xbrli:context[@id='" + ContextID + "']")
            for j in oNodelist3:
            
                #Nodes with the right period
                if self.getNode("xbrli:period/xbrli:instant",j) is not None and self.getNode("xbrli:period/xbrli:instant",j).text==EndDate:
                    
                    oNode4 = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember",j)
                                        
                    if not len(oNode4):
                        UseContext = ContextID
                        #print UseContext
                                                    
            
        """
        #NOTE: if the DocumentPeriodEndDate is incorrect, this attempts to fix it by looking for a few commonly occuring concepts for the current period...
        if UseContext=="ERROR":
            print 'if the DocumentPeriodEndDate is incorrect, this attempts to fix it by looking for a few commonly occuring concepts for the current period...'                    
            oNodelist_Error = self.getNode("//dei:DocumentPeriodEndDate | fsa:OrganizationConsolidationAndPresentationOfFinancialStatementsDisclosureTextBlock | fsa:SignificantAccountingPoliciesTextBlock")
            #print "Nodelist, trying to find alternative: " + oNodelist_Error.length
            
            ContextID = oNodelist_Error.get('contextRef')
            ContextPeriod = self.getNode("//xbrli:context[@id='" + ContextID + "']/xbrli:period/xbrli:endDate").text
            
            print "Found Alternative: " + ContextPeriod
            
            oNodelist3 = self.getNodeList("//xbrli:context[xbrli:period/xbrli:instant='" + ContextPeriod + "']")
            #print "Found alternative contexts:" + oNodelist3.length
            
            for j in oNodelist3:
                #print j.XML
                
                #Nodes with the right period
                if self.getNode("xbrli:period/xbrli:instant",j).text==ContextPeriod:
                    oNode4 = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember",j)
                    #print "Found dimension: " + oNode4.XML
                    #WHATS GOING ON HERE                
                    
                    if len(oNode4):
                        #Not the right context
                        print "Note4: " + oNode4[0].text
                    else:
                        #print "SELECTED CONTEXT: " + oNodelist3.Item(j).selectSingleNode("./@id").text 'oNodelist3(j).XML
                        ContextID = j.get("id")
                        UseContext = ContextID
                        #print UseContext
                                        
                    #print j.XML
                                    
            #EndDate = ContextPeriod
            """           
        
       
        
        ContextForInstants = UseContext
        self.fields['ContextForInstants'] = ContextForInstants
        
        
        ###This finds the duration context
        ###This may work incorrectly for fiscal year ends because the dates cross calendar years
        #Get context ID of durations and the start date for the database table
        try:
            oNodelist2 = self.getNodeList("fsa:CashAndCashEquivalentsPeriodIncreaseDecrease | fsa:CashPeriodIncreaseDecrease | fsa:NetIncomeLoss | gsd:ReportingPeriodEndDate")
        except: oNodelist2 = self.getNodeList("e:CashAndCashEquivalentsPeriodIncreaseDecrease | e:CashPeriodIncreaseDecrease | e:NetIncomeLoss | c:ReportingPeriodEndDate")

        StartDate = "ERROR"
        StartDateYTD = "2099-01-01"
        UseContext = "ERROR"
        
        for i in oNodelist2:
            #print i.XML
            
            ContextID = i.get('contextRef')
            ContextPeriod = self.getNode("//xbrli:context[@id='" + ContextID + "']/xbrli:period/xbrli:endDate")
            #Usecontext = ContextID
            #print ContextPeriod
            
            #Nodelist of all the contexts of the fact us-gaap:Assets
            oNodelist3 = self.getNodeList("//xbrli:context[@id='" + ContextID + "']")
            for j in oNodelist3:
            
                #Nodes with the right period
                if self.getNode("xbrli:period/xbrli:endDate",j).text==EndDate:
                    
                    oNode4 = self.getNodeList("xbrli:entity/xbrli:segment/xbrldi:explicitMember",j)
                                        
                    if not len(oNode4): #Making sure there are no dimensions. Is this the right way to do it?
                    
                        #Get the year-to-date context, not the current period
                        StartDate = self.getNode("xbrli:period/xbrli:startDate",j).text
                        #print "Context start date: " + StartDate
                        #print "YTD start date: " + StartDateYTD
                        
                        if StartDate <= StartDateYTD:
                            #MsgBox "YTD is greater"
                            #Start date is for quarter
                            #print "Context start date is less than current year to date, replace"
                            #print "Context start date: " + StartDate
                            #print "Current min: " + StartDateYTD
                            
                            StartDateYTD = StartDate
                            UseContext = j.get('id')
                            #MsgBox j.selectSingleNode("@id").text
                        else:
                            #MsgBox "Context is greater"
                            #Start date is for year
                            #print "Context start date is greater than YTD, keep current YTD"
                            #print "Context start date: " + StartDate
                            
                            StartDateYTD = StartDateYTD

                        
                        #print "Use context ID: " + UseContext
                        #print "Current min: " + StartDateYTD
                        #print " "
                                        
                        #print "Use context: " + UseContext
                            

        #Balance sheet date of current period
        self.fields['BalanceSheetDate'] = EndDate
        
        #MsgBox "Instant context is: " + ContextForInstants
        if ContextForInstants=="ERROR":
            #MsgBox "Looking for alternative instance context"
            
            ContextForInstants = self.LookForAlternativeInstanceContext()
            self.fields['ContextForInstants'] = ContextForInstants
        
        
        #Income statement date for current fiscal year, year to date
        self.fields['IncomeStatementPeriodYTD'] = StartDateYTD
        
        ContextForDurations = UseContext
        self.fields['ContextForDurations'] = ContextForDurations

    def LookForAlternativeInstanceContext(self):
        #This deals with the situation where no instance context has no dimensions
        #Finds something
            
        something = None
        
        #See if there are any nodes with the document period focus date
        oNodeList_Alt = self.getNodeList("//xbrli:context[xbrli:period/xbrli:instant='" + self.fields['BalanceSheetDate'] + "']")

        #MsgBox "Node list length: " + oNodeList_Alt.length
        for oNode_Alt in oNodeList_Alt:
            #Found possible contexts
            #MsgBox oNode_Alt.selectSingleNode("@id").text
            try: something = self.getNode("fsa:Assets[@contextRef='" + oNode_Alt.get("id") + "']")
            except: something = self.getNode("g:Assets[@contextRef='" + oNode_Alt.get("id") + "']")
            if something is not None:
                #MsgBox "Use this context: " + oNode_Alt.selectSingleNode("@id").text
                return oNode_Alt.get("id")

