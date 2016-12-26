from datetime import datetime, timedelta
from dateutil import relativedelta, parser
import datetime
import sys
import os
import psycopg2
import unicodedata
class FundamentantalAccountingConcepts:               

    def __init__(self,xbrl):               

        self.xbrl = xbrl


         
        
        #Assets
        
        try:self.xbrl.fields['Assets'] = self.xbrl.GetFactValue("fsa:Assets","Instant")
        except:self.xbrl.fields['Assets'] = self.xbrl.GetFactValue("g:Assets","Instant")
        print(self.xbrl.fields['Assets'])
        if self.xbrl.fields['Assets']== None:
            self.xbrl.fields['Assets'] = 0

        #Current Assets
        try:self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue("fsa:CurrentAssets", "Instant")
        except: self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue("g:CurrentAssets", "Instant")
        if self.xbrl.fields['CurrentAssets']== None:
            self.xbrl.fields['CurrentAssets'] = 0

        #Noncurrent Assets
        try:self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("fsa:AssetsNoncurrent", "Instant")
        except:self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("g:AssetsNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentAssets']==None:
            try: self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("fsa:NoncurrentAssets", "Instant")
            except: self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("g:NoncurrentAssets", "Instant")
            if self.xbrl.fields['NoncurrentAssets']==None:
                if self.xbrl.fields['Assets'] and self.xbrl.fields['CurrentAssets']:
                    self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']
                else:
                    self.xbrl.fields['NoncurrentAssets'] = 0

        #LiabilitiesAndEquity
        try: self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndStockholdersEquity", "Instant")
        except: self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("g:LiabilitiesAndStockholdersEquity", "Instant")
        if self.xbrl.fields['LiabilitiesAndEquity']== None:
            try: self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndPartnersCapital", "Instant")
            except: self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("g:LiabilitiesAndPartnersCapital", "Instant")
            if self.xbrl.fields['LiabilitiesAndEquity']== None:
                self.xbrl.fields['LiabilitiesAndEquity'] = 0

        #Liabilities
        try: self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue("fsa:Liabilities", "Instant")
        except: self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue("g:Liabilities", "Instant")
        if self.xbrl.fields['Liabilities']== None:
            self.xbrl.fields['Liabilities'] = 0
        #CurrentLiabilities
        try: self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue("fsa:LiabilitiesCurrent", "Instant")
        except: self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue("g:LiabilitiesCurrent", "Instant")
        if self.xbrl.fields['CurrentLiabilities']== None:
            self.xbrl.fields['CurrentLiabilities'] = 0

        #Noncurrent Liabilities
        try: self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("fsa:LiabilitiesNoncurrent", "Instant")
        except: self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("g:LiabilitiesNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentLiabilities']== None:
            try: self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("fsa:NoncurrentLiabilities", "Instant")
            except: self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("g:NoncurrentLiabilities", "Instant")
            if self.xbrl.fields['NoncurrentLiabilities']== None:
                if self.xbrl.fields['Liabilities'] and self.xbrl.fields['CurrentLiabilities']:
                    self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - self.xbrl.fields['CurrentLiabilities']
                else:
                    self.xbrl.fields['NoncurrentLiabilities'] = 0

        #CommitmentsAndContingencies
        try: self.xbrl.fields['CommitmentsAndContingencies'] = self.xbrl.GetFactValue("fsa:CommitmentsAndContingencies", "Instant")
        except: self.xbrl.fields['CommitmentsAndContingencies'] = self.xbrl.GetFactValue("g:CommitmentsAndContingencies", "Instant")
        if self.xbrl.fields['CommitmentsAndContingencies']== None:
            self.xbrl.fields['CommitmentsAndContingencies'] = 0

        #TemporaryEquity
        try: self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityRedemptionValue", "Instant")
        except: self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:TemporaryEquityRedemptionValue", "Instant")
        if self.xbrl.fields['TemporaryEquity'] == None:
            try:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:RedeemablePreferredStockCarryingAmount", "Instant")
            except:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:RedeemablePreferredStockCarryingAmount", "Instant")
            if self.xbrl.fields['TemporaryEquity'] == None:
                try:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityCarryingAmount", "Instant")
                except:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:TemporaryEquityCarryingAmount", "Instant")
                if self.xbrl.fields['TemporaryEquity'] == None:
                    try:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityValueExcludingAdditionalPaidInCapital", "Instant")
                    except:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:TemporaryEquityValueExcludingAdditionalPaidInCapital", "Instant")
                    if self.xbrl.fields['TemporaryEquity'] == None:
                        try:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityCarryingAmountAttributableToParent", "Instant")
                        except:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:TemporaryEquityCarryingAmountAttributableToParent", "Instant")
                        if self.xbrl.fields['TemporaryEquity'] == None:
                            try:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityFairValue", "Instant")
                            except:self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("g:RedeemableNoncontrollingInterestEquityFairValue", "Instant")
                            if self.xbrl.fields['TemporaryEquity'] == None:
                                self.xbrl.fields['TemporaryEquity'] = 0

        #RedeemableNoncontrollingInterest (added to temporary equity)
        RedeemableNoncontrollingInterest = None

        '''RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityCarryingAmount", "Instant")
        if RedeemableNoncontrollingInterest == None:
            RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityCommonCarryingAmount", "Instant")
            if RedeemableNoncontrollingInterest == None:
                RedeemableNoncontrollingInterest = 0

        #This adds redeemable noncontrolling interest and temporary equity which are rare, but can be reported seperately
        if self.xbrl.fields['TemporaryEquity']:
            self.xbrl.fields['TemporaryEquity'] = float(self.xbrl.fields['TemporaryEquity']) + float(RedeemableNoncontrollingInterest)'''


        #Equity
        try: self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "Instant")
        except: self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "Instant")
        if self.xbrl.fields['Equity'] == None:
            try: self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:Equity", "Instant")
            except: self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:Equity", "Instant")
            if self.xbrl.fields['Equity'] == None:
                try:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest", "Instant")
                except: self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest", "Instant")
                if self.xbrl.fields['Equity'] == None:
                    try:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:PartnersCapital", "Instant")
                    except:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:PartnersCapital", "Instant")
                    if self.xbrl.fields['Equity'] == None:
                        try:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:CommonStockholdersEquity", "Instant")
                        except:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:CommonStockholdersEquity", "Instant")
                        if self.xbrl.fields['Equity'] == None:
                            try:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:MemberEquity", "Instant")
                            except:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:MemberEquity", "Instant")
                            if self.xbrl.fields['Equity'] == None:
                                try:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:AssetsNet", "Instant")
                                except:self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("g:AssetsNet", "Instant")
                                if self.xbrl.fields['Equity'] == None:
                                    self.xbrl.fields['Equity'] = 0


        #EquityAttributableToNoncontrollingInterest
        try:self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:MinorityInterest", "Instant")
        except:self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("g:MinorityInterest", "Instant")
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
            try:self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:PartnersCapitalAttributableToNoncontrollingInterest", "Instant")
            except:self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("g:PartnersCapitalAttributableToNoncontrollingInterest", "Instant")

            if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
                self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = 0

        #EquityAttributableToParent
        try:self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("fsa:StockholdersEquity", "Instant")
        except:self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("g:StockholdersEquity", "Instant")
        if self.xbrl.fields['EquityAttributableToParent'] == None:
            try:self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndPartnersCapital", "Instant")
            except:self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("g:LiabilitiesAndPartnersCapital", "Instant")
            if self.xbrl.fields['EquityAttributableToParent'] == None:
                self.xbrl.fields['EquityAttributableToParent'] = 0



        #BS Adjustments
        #if total assets is missing, try using current assets
        if self.xbrl.fields['Assets'] == 0 and self.xbrl.fields['Assets'] == self.xbrl.fields['LiabilitiesAndEquity'] and self.xbrl.fields['CurrentAssets'] == self.xbrl.fields['LiabilitiesAndEquity']:
            self.xbrl.fields['Assets'] = self.xbrl.fields['CurrentAssets']

        #Added to fix Assets
        if self.xbrl.fields['Assets'] == 0 and self.xbrl.fields['LiabilitiesAndEquity'] != 0 and (self.xbrl.fields['CurrentAssets'] == self.xbrl.fields['LiabilitiesAndEquity']):
            self.xbrl.fields['Assets'] = self.xbrl.fields['CurrentAssets']

        #Added to fix Assets even more
        if self.xbrl.fields['Assets'] == 0 and self.xbrl.fields['NoncurrentAssets'] == 0 and self.xbrl.fields['LiabilitiesAndEquity'] != 0 and (self.xbrl.fields['LiabilitiesAndEquity']==self.xbrl.fields['Liabilities']+self.xbrl.fields['Equity']):
            self.xbrl.fields['Assets'] = self.xbrl.fields['CurrentAssets']

        if self.xbrl.fields['Assets']!=0 and self.xbrl.fields['CurrentAssets']!=0:
            self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']

        if self.xbrl.fields['LiabilitiesAndEquity']==0 and self.xbrl.fields['Assets']!=0:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.fields['Assets']
        #Impute: Equity based no parent and noncontrolling interest being present
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest']!=0 and self.xbrl.fields['EquityAttributableToParent']!=0:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent'] + self.xbrl.fields['EquityAttributableToNoncontrollingInterest']

        if self.xbrl.fields['Equity']==0 and self.xbrl.fields['EquityAttributableToNoncontrollingInterest']==0 and self.xbrl.fields['EquityAttributableToParent']!=0:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent']

        if self.xbrl.fields['Equity']==0:
            self.xbrl.fields['Equity'] = self.xbrl.fields['EquityAttributableToParent'] + self.xbrl.fields['EquityAttributableToNoncontrollingInterest']

        #Added: Impute Equity attributable to parent based on existence of equity and noncontrolling interest.
        if self.xbrl.fields['Equity']!=0 and self.xbrl.fields['EquityAttributableToNoncontrollingInterest']!=0 and self.xbrl.fields['EquityAttributableToParent']==0:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.fields['Equity'] - self.xbrl.fields['EquityAttributableToNoncontrollingInterest']

        #Added: Impute Equity attributable to parent based on existence of equity and noncontrolling interest.
        if self.xbrl.fields['Equity']!=0 and self.xbrl.fields['EquityAttributableToNoncontrollingInterest']==0 and self.xbrl.fields['EquityAttributableToParent']==0:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.fields['Equity']

        #if total liabilities is missing, figure it out based on liabilities and equity
        if self.xbrl.fields['Liabilities']==0 and self.xbrl.fields['Equity']!=0:
            self.xbrl.fields['Liabilities'] = self.xbrl.fields['LiabilitiesAndEquity'] - (self.xbrl.fields['CommitmentsAndContingencies'] + self.xbrl.fields['TemporaryEquity'] + self.xbrl.fields['Equity'])

        #This seems incorrect because liabilities might not be reported
        if self.xbrl.fields['Liabilities']!=0 and self.xbrl.fields['CurrentLiabilities']!=0:
            self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - self.xbrl.fields['CurrentLiabilities']

        #Added to fix liabilities based on current liabilities
        if self.xbrl.fields['Liabilities']==0 and self.xbrl.fields['CurrentLiabilities']!=0 and self.xbrl.fields['NoncurrentLiabilities']==0:
            self.xbrl.fields['Liabilities'] = self.xbrl.fields['CurrentLiabilities']

        lngBSCheck1 = self.xbrl.fields['Equity'] - (self.xbrl.fields['EquityAttributableToParent'] + self.xbrl.fields['EquityAttributableToNoncontrollingInterest'])
        #lngBSCheck2 = self.xbrl.fields['Assets'] - self.xbrl.fields['LiabilitiesAndEquity']
        if self.xbrl.fields['CurrentAssets']==0 and self.xbrl.fields['NoncurrentAssets']==0 and self.xbrl.fields['CurrentLiabilities']==0 and self.xbrl.fields['NoncurrentLiabilities']==0:
            #if current assets/liabilities are zero and noncurrent assets/liabilities;: don't do this test because the balance sheet is not classified
           lngBSCheck3 = 0
           lngBSCheck4 = 0

        else:
            #balance sheet IS classified
            lngBSCheck3 = self.xbrl.fields['Assets'] - (self.xbrl.fields['CurrentAssets'] + self.xbrl.fields['NoncurrentAssets'])
            lngBSCheck4 = self.xbrl.fields['Liabilities'] - (self.xbrl.fields['CurrentLiabilities'] + self.xbrl.fields['NoncurrentLiabilities'])

        lngBSCheck5 = self.xbrl.fields['LiabilitiesAndEquity'] - (self.xbrl.fields['Liabilities'] + self.xbrl.fields['CommitmentsAndContingencies'] + self.xbrl.fields['TemporaryEquity'] + self.xbrl.fields['Equity'])



        #Income statement

        #Revenue
        try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:Revenue", "Duration")
        except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:Revenue", "Duration")
        if self.xbrl.fields['Revenue'] == None:
            try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:SalesRevenueNet", "Duration")
            except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:SalesRevenueNet", "Duration")
            if self.xbrl.fields['Revenue'] == None:
                try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:SalesRevenueervicesNet", "Duration")
                except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:SalesRevenueervicesNet", "Duration")
                if self.xbrl.fields['Revenue'] == None:
                    try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RevenueNetOfInterestExpense", "Duration")
                    except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:RevenueNetOfInterestExpense", "Duration")
                    if self.xbrl.fields['Revenue'] == None:
                        try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                        except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                        if self.xbrl.fields['Revenue'] == None:
                            try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:HealthCareOrganizationRevenue", "Duration")
                            except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:HealthCareOrganizationRevenue", "Duration")
                            if self.xbrl.fields['Revenue'] == None:
                                try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:InterestAndDividendIncomeOperating", "Duration")
                                except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:InterestAndDividendIncomeOperating", "Duration")
                                if self.xbrl.fields['Revenue'] == None:
                                    try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RealEstateRevenueNet", "Duration")
                                    except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:RealEstateRevenueNet", "Duration")
                                    if self.xbrl.fields['Revenue'] == None:
                                        try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RevenueMineralSales", "Duration")
                                        except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:RevenueMineralSales", "Duration")
                                        if self.xbrl.fields['Revenue'] == None:
                                            try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:OilAndGasRevenue", "Duration")
                                            except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:OilAndGasRevenue", "Duration")
                                            if self.xbrl.fields['Revenue'] == None:
                                                try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:FinancialServicesRevenue", "Duration")
                                                except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:FinancialServicesRevenue", "Duration")
                                                if self.xbrl.fields['Revenue'] == None:
                                                    try:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                                                    except:self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("g:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                                                    if self.xbrl.fields['Revenue'] == None:
                                                        self.xbrl.fields['Revenue'] = 0


        #CostOfRevenue
        try:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfRevenue", "Duration")
        except:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("g:CostOfRevenue", "Duration")
        if self.xbrl.fields['CostOfRevenue'] == None:
            try:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfServices", "Duration")
            except:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("g:CostOfServices", "Duration")
            if self.xbrl.fields['CostOfRevenue'] == None:
                try:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfGoodsSold", "Duration")
                except:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("g:CostOfGoodsSold", "Duration")
                if self.xbrl.fields['CostOfRevenue'] == None:
                    try:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfGoodsAndServicesSold", "Duration")
                    except:self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("g:CostOfGoodsAndServicesSold", "Duration")
                    if self.xbrl.fields['CostOfRevenue'] == None:
                        self.xbrl.fields['CostOfRevenue'] = 0

        #GrossProfit
        try:self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("fsa:GrossProfit", "Duration")
        except:self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("g:GrossProfit", "Duration")
        if self.xbrl.fields['GrossProfit'] == None:
            try:self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("fsa:GrossProfit", "Duration")
            except:self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("g:GrossProfit", "Duration")
            if self.xbrl.fields['GrossProfit'] == None:
                self.xbrl.fields['GrossProfit'] = 0

        #OperatingExpenses
        try:self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("fsa:OperatingExpenses", "Duration")
        except:self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("g:OperatingExpenses", "Duration")
        if self.xbrl.fields['OperatingExpenses'] == None:
            try:self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("fsa:OperatingCostsAndExpenses", "Duration")  #This concept seems incorrect.
            except:self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("g:OperatingCostsAndExpenses", "Duration")  #This concept seems incorrect.
            if self.xbrl.fields['OperatingExpenses'] == None:
                self.xbrl.fields['OperatingExpenses'] = 0
        #CostsAndExpenses
        try:self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("fsa:CostsAndExpenses", "Duration")
        except:self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("g:CostsAndExpenses", "Duration")
        if self.xbrl.fields['CostsAndExpenses'] == None:
            try:self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("fsa:CostsAndExpenses", "Duration")
            except:self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("g:CostsAndExpenses", "Duration")
            if self.xbrl.fields['CostsAndExpenses'] == None:
                self.xbrl.fields['CostsAndExpenses'] = 0

        #OtherOperatingIncome
        try:self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("fsa:OtherOperatingIncome", "Duration")
        except:self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("g:OtherOperatingIncome", "Duration")
        if self.xbrl.fields['OtherOperatingIncome'] == None:
            try:self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("fsa:OtherOperatingIncome", "Duration")
            except:self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("g:OtherOperatingIncome", "Duration")
            if self.xbrl.fields['OtherOperatingIncome'] == None:
                self.xbrl.fields['OtherOperatingIncome'] = 0

        #OperatingIncomeLoss
        try:self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:OperatingIncomeLoss", "Duration")
        except:self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("g:OperatingIncomeLoss", "Duration")
        if self.xbrl.fields['OperatingIncomeLoss'] == None:
            try:self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:OperatingIncomeLoss", "Duration")
            except:self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("g:OperatingIncomeLoss", "Duration")
            if self.xbrl.fields['OperatingIncomeLoss'] == None:
                self.xbrl.fields['OperatingIncomeLoss'] = 0

        #NonoperatingIncomeLoss
        try:self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:NonoperatingIncomeExpense", "Duration")
        except:self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("g:NonoperatingIncomeExpense", "Duration")
        if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
            try:self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:NonoperatingIncomeExpense", "Duration")
            except:self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("g:NonoperatingIncomeExpense", "Duration")
            if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
                self.xbrl.fields['NonoperatingIncomeLoss'] = 0

        #InterestAndDebtExpense
        try:self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("fsa:InterestAndDebtExpense", "Duration")
        except:self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("g:InterestAndDebtExpense", "Duration")
        if self.xbrl.fields['InterestAndDebtExpense'] == None:
            try:self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("fsa:InterestAndDebtExpense", "Duration")
            except:self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("g:InterestAndDebtExpense", "Duration")
            if self.xbrl.fields['InterestAndDebtExpense'] == None:
                self.xbrl.fields['InterestAndDebtExpense'] = 0

        #IncomeBeforeEquityMethodInvestments
        try:self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        except:self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
            try:self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
            except:self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = 0

        #IncomeFromEquityMethodInvestments
        try:self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromEquityMethodInvestments", "Duration")
        except:self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("g:IncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
            try:self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromEquityMethodInvestments", "Duration")
            except:self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("g:IncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeFromEquityMethodInvestments'] = 0

        #IncomeFromContinuingOperationsBeforeTax
        try:self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        except:self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
            try:self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "Duration")
            except:self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = 0

        #IncomeTaxExpenseBenefit
        try:self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("fsa:IncomeTaxExpenseBenefit", "Duration")
        except:self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("g:IncomeTaxExpenseBenefit", "Duration")
        if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
            try:self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("fsa:IncomeTaxExpenseBenefitContinuingOperations", "Duration")
            except:self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("g:IncomeTaxExpenseBenefitContinuingOperations", "Duration")
            if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
                self.xbrl.fields['IncomeTaxExpenseBenefit'] = 0
        #IncomeFromContinuingOperationsAfterTax
        try:self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("fsa:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
        except:self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("g:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
            try:self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("fsa:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
            except:self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("g:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = 0

        #IncomeFromDiscontinuedOperations
        try:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:IncomeLossFromDiscontinuedOperationsNetOfTax", "Duration")
        except:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("g:IncomeLossFromDiscontinuedOperationsNetOfTax", "Duration")
        if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
            try:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:DiscontinuedOperationGainLossOnDisposalOfDiscontinuedOperationNetOfTax", "Duration")
            except:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("g:DiscontinuedOperationGainLossOnDisposalOfDiscontinuedOperationNetOfTax", "Duration")
            if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                try:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity", "Duration")
                except:self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("g:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity", "Duration")
                if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                    self.xbrl.fields['IncomeFromDiscontinuedOperations'] = 0

        #ExtraordaryItemsGainLoss
        try:self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("fsa:ExtraordinaryItemNetOfTax", "Duration")
        except:self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("g:ExtraordinaryItemNetOfTax", "Duration")
        if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
            try:self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("fsa:ExtraordinaryItemNetOfTax", "Duration")
            except:self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("g:ExtraordinaryItemNetOfTax", "Duration")
            if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
                self.xbrl.fields['ExtraordaryItemsGainLoss'] = 0
        #NetIncomeLoss
        try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:ProfitLoss", "Duration")
        except:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:ProfitLoss", "Duration")
        if self.xbrl.fields['NetIncomeLoss']== None:
            try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:NetIncomeLoss", "Duration")
            except:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:NetIncomeLoss", "Duration")
            if self.xbrl.fields['NetIncomeLoss']== None:
                try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
                except:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
                if self.xbrl.fields['NetIncomeLoss']== None:
                    try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperations", "Duration")
                    except:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperations", "Duration")
                    if self.xbrl.fields['NetIncomeLoss']== None:
                        try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossAttributableToParent", "Duration")
                        except:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:IncomeLossAttributableToParent", "Duration")
                        if self.xbrl.fields['NetIncomeLoss']== None:
                            try:self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest", "Duration")
                            except:                          self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("g:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest", "Duration")
                            if self.xbrl.fields['NetIncomeLoss']== None:
                                self.xbrl.fields['NetIncomeLoss'] = 0

        #NetIncomeAvailableToCommonStockholdersBasic
        try:self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
        except:self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.GetFactValue("g:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
        if self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']== None:
            self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = 0

        #PreferredStockDividendsAndOtherAdjustments
        try:self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.GetFactValue("fsa:PreferredStockDividendsAndOtherAdjustments", "Duration")
        except:self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.GetFactValue("g:PreferredStockDividendsAndOtherAdjustments", "Duration")
        if self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']== None:
            self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = 0

        #NetIncomeAttributableToNoncontrollingInterest
        try:self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAttributableToNoncontrollingInterest", "Duration")
        except:self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("g:NetIncomeLossAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest']== None:
            self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = 0

        #NetIncomeAttributableToParent
        try:self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:NetIncomeLoss", "Duration")
        except:self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue("g:NetIncomeLoss", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToParent']== None:
            self.xbrl.fields['NetIncomeAttributableToParent'] = 0

        #OtherComprehensiveIncome
        try:self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:OtherComprehensiveIncomeLossNetOfTax", "Duration")
        except:self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("g:OtherComprehensiveIncomeLossNetOfTax", "Duration")
        if self.xbrl.fields['OtherComprehensiveIncome']== None:
            try:self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:OtherComprehensiveIncomeLossNetOfTax", "Duration")
            except:self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("g:OtherComprehensiveIncomeLossNetOfTax", "Duration")
            if self.xbrl.fields['OtherComprehensiveIncome']== None:
                self.xbrl.fields['OtherComprehensiveIncome'] = 0

        #ComprehensiveIncome
        try:self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest", "Duration")
        except:self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncome']== None:
            try:self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
            except:self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncome']== None:
                self.xbrl.fields['ComprehensiveIncome'] = 0

        #ComprehensiveIncomeAttributableToParent
        try:self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
        except:self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTax", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
            try:self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
            except:self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
                self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = 0

        #ComprehensiveIncomeAttributableToNoncontrollingInterest
        try:self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
        except:self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==None:
            try:self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
            except:self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("g:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
            if self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==None:
                self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = 0

        #########'Adjustments to income statement information
        #Impute: NonoperatingIncomeLossPlusInterestAndDebtExpense
        self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] = self.xbrl.fields['NonoperatingIncomeLoss'] + self.xbrl.fields['InterestAndDebtExpense']

        #Impute: Net income available to common stockholders  (if it does not exist)
        if self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']==0 and self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']==0 and self.xbrl.fields['NetIncomeAttributableToParent']!=0:
            self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.fields['NetIncomeAttributableToParent']

        #Impute NetIncomeLoss
        if self.xbrl.fields['NetIncomeLoss']!=0 and self.xbrl.fields['IncomeFromContinuingOperationsAfterTax']==0:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.fields['NetIncomeLoss'] - self.xbrl.fields['IncomeFromDiscontinuedOperations'] - self.xbrl.fields['ExtraordaryItemsGainLoss']

        #Impute: Net income attributable to parent if it does not exist
        if self.xbrl.fields['NetIncomeAttributableToParent']==0 and self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest']==0 and self.xbrl.fields['NetIncomeLoss']!=0:
            self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.fields['NetIncomeLoss']

        #Impute: PreferredStockDividendsAndOtherAdjustments
        if self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']==0 and self.xbrl.fields['NetIncomeAttributableToParent']!=0 and self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']!=0:
            self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.fields['NetIncomeAttributableToParent'] - self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']

        #Impute: comprehensive income
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']==0 and self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==0 and self.xbrl.fields['ComprehensiveIncome']==0 and self.xbrl.fields['OtherComprehensiveIncome']==0:
            self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.fields['NetIncomeLoss']

        #Impute: other comprehensive income
        if self.xbrl.fields['ComprehensiveIncome']!=0 and self.xbrl.fields['OtherComprehensiveIncome']==0:
            self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.fields['ComprehensiveIncome'] - self.xbrl.fields['NetIncomeLoss']

        #Impute: comprehensive income attributable to parent if it does not exist
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']==0 and self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==0 and self.xbrl.fields['ComprehensiveIncome']!=0:
            self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.fields['ComprehensiveIncome']

        #Impute: IncomeFromContinuingOperations*Before*Tax
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments']!=0 and self.xbrl.fields['IncomeFromEquityMethodInvestments']!=0 and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']==0:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] + self.xbrl.fields['IncomeFromEquityMethodInvestments']

        #Impute: IncomeFromContinuingOperations*Before*Tax2 (if income before tax is missing)
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']==0 and self.xbrl.fields['IncomeFromContinuingOperationsAfterTax']!=0:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] + self.xbrl.fields['IncomeTaxExpenseBenefit']

        #Impute: IncomeFromContinuingOperations*After*Tax
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax']==0 and \
            (self.xbrl.fields['IncomeTaxExpenseBenefit']!=0 or self.xbrl.fields['IncomeTaxExpenseBenefit']==0) and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']!=0:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['IncomeTaxExpenseBenefit']


        #Impute: GrossProfit
        if self.xbrl.fields['GrossProfit']==0 and (self.xbrl.fields['Revenue']!=0 and self.xbrl.fields['CostOfRevenue']!=0):
            self.xbrl.fields['GrossProfit'] = self.xbrl.fields['Revenue'] - self.xbrl.fields['CostOfRevenue']

        #Impute: GrossProfit
        if self.xbrl.fields['GrossProfit']==0 and (self.xbrl.fields['Revenue']!=0 and self.xbrl.fields['CostOfRevenue']!=0):
            self.xbrl.fields['GrossProfit'] = self.xbrl.fields['Revenue'] - self.xbrl.fields['CostOfRevenue']

        #Impute: Revenue
        if self.xbrl.fields['GrossProfit']!=0 and (self.xbrl.fields['Revenue']==0 and self.xbrl.fields['CostOfRevenue']!=0):
            self.xbrl.fields['Revenue'] = self.xbrl.fields['GrossProfit'] + self.xbrl.fields['CostOfRevenue']

        #Impute: CostOfRevenue
        if self.xbrl.fields['GrossProfit']!=0 and (self.xbrl.fields['Revenue']!=0 and self.xbrl.fields['CostOfRevenue']==0):
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.fields['GrossProfit'] + self.xbrl.fields['Revenue']
        #Impute: CostsAndExpenses (would NEVER have costs and expenses if has gross profit, gross profit is multi-step and costs and expenses is single-step)
        if self.xbrl.fields['GrossProfit']==0 and self.xbrl.fields['CostsAndExpenses']==0 and (self.xbrl.fields['CostOfRevenue']!=0 and self.xbrl.fields['OperatingExpenses']!=0):
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['CostOfRevenue'] + self.xbrl.fields['OperatingExpenses']

        #Impute: CostsAndExpenses based on existance of both costs of Revenue and operating expenses
        if self.xbrl.fields['CostsAndExpenses']==0 and self.xbrl.fields['OperatingExpenses']!=0 and (self.xbrl.fields['CostOfRevenue']!=0):
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['CostOfRevenue'] + self.xbrl.fields['OperatingExpenses']

        #Impute: CostsAndExpenses
        if self.xbrl.fields['GrossProfit']==0 and self.xbrl.fields['CostsAndExpenses']==0 and self.xbrl.fields['Revenue']!=0 and self.xbrl.fields['OperatingIncomeLoss']!=0 and self.xbrl.fields['OtherOperatingIncome']!=0:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.fields['Revenue'] - self.xbrl.fields['OperatingIncomeLoss'] - self.xbrl.fields['OtherOperatingIncome']

        #Impute: OperatingExpenses based on existance of costs and expenses and cost of Revenue
        if self.xbrl.fields['CostOfRevenue']!=0 and self.xbrl.fields['CostsAndExpenses']!=0 and self.xbrl.fields['OperatingExpenses']==0:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.fields['CostsAndExpenses'] - self.xbrl.fields['CostOfRevenue']
            #print(self.xbrl.fields['OperatingExpenses'])

        #Impute: CostOfRevenue single-step method
        if self.xbrl.fields['Revenue']!=0 and self.xbrl.fields['GrossProfit']==0 and \
            (self.xbrl.fields['Revenue'] - self.xbrl.fields['CostsAndExpenses']==self.xbrl.fields['OperatingIncomeLoss']) and \
            self.xbrl.fields['OperatingExpenses']==0 and self.xbrl.fields['OtherOperatingIncome']==0:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.fields['CostsAndExpenses'] - self.xbrl.fields['OperatingExpenses']

        #Impute: IncomeBeforeEquityMethodInvestments
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments']==0 and self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']!=0:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['IncomeFromEquityMethodInvestments']

        #Impute: IncomeBeforeEquityMethodInvestments
        if self.xbrl.fields['OperatingIncomeLoss']!=0 and (self.xbrl.fields['NonoperatingIncomeLoss']!=0 and \
            self.xbrl.fields['InterestAndDebtExpense']==0 and self.xbrl.fields['IncomeBeforeEquityMethodInvestments']!=0):
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] - (self.xbrl.fields['OperatingIncomeLoss'] + self.xbrl.fields['NonoperatingIncomeLoss'])

        #Impute: OtherOperatingIncome
        if self.xbrl.fields['GrossProfit']!=0 and (self.xbrl.fields['OperatingExpenses']!=0 and self.xbrl.fields['OperatingIncomeLoss']!=0):
            self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.fields['OperatingIncomeLoss'] - (self.xbrl.fields['GrossProfit'] - self.xbrl.fields['OperatingExpenses'])

        #Move IncomeFromEquityMethodInvestments
        if self.xbrl.fields['IncomeFromEquityMethodInvestments']!=0 and \
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments']!=0 and self.xbrl.fields['IncomeBeforeEquityMethodInvestments']!=self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['IncomeFromEquityMethodInvestments']
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.fields['OperatingIncomeLoss'] - self.xbrl.fields['IncomeFromEquityMethodInvestments']

        #DANGEROUS!!  May need to turn off. IS3 had 2085 PASSES WITHOUT this imputing. if it is higher,: keep the test
        #Impute: OperatingIncomeLoss
        if self.xbrl.fields['OperatingIncomeLoss']==0 and self.xbrl.fields['IncomeBeforeEquityMethodInvestments']!=0:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] + self.xbrl.fields['NonoperatingIncomeLoss'] - self.xbrl.fields['InterestAndDebtExpense']


        self.xbrl.fields['NonoperatingIncomePlusInterestAndDbtExpnsPlsIncFrmEqtyMthdInvst'] = self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['OperatingIncomeLoss']

        #NonoperatingIncomeLossPlusInterestAndDebtExpense
        if self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense']== 0 and self.xbrl.fields['NonoperatingIncomePlusInterestAndDbtExpnsPlsIncFrmEqtyMthdInvst']!=0:
            self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] = self.xbrl.fields['NonoperatingIncomePlusInterestAndDbtExpnsPlsIncFrmEqtyMthdInvst'] - self.xbrl.fields['IncomeFromEquityMethodInvestments']


        lngIS1 = (self.xbrl.fields['Revenue'] - self.xbrl.fields['CostOfRevenue']) - self.xbrl.fields['GrossProfit']
        lngIS2 = (self.xbrl.fields['GrossProfit'] - self.xbrl.fields['OperatingExpenses'] + self.xbrl.fields['OtherOperatingIncome']) - self.xbrl.fields['OperatingIncomeLoss']
        lngIS3 = (self.xbrl.fields['OperatingIncomeLoss'] + self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense']) - self.xbrl.fields['IncomeBeforeEquityMethodInvestments']
        lngIS4 = (self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] + self.xbrl.fields['IncomeFromEquityMethodInvestments']) - self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax']
        lngIS5 = (self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['IncomeTaxExpenseBenefit']) - self.xbrl.fields['IncomeFromContinuingOperationsAfterTax']
        lngIS6 = (self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] + self.xbrl.fields['IncomeFromDiscontinuedOperations'] + self.xbrl.fields['ExtraordaryItemsGainLoss']) - self.xbrl.fields['NetIncomeLoss']
        lngIS7 = (self.xbrl.fields['NetIncomeAttributableToParent'] + self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest']) - self.xbrl.fields['NetIncomeLoss']
        lngIS8 = (self.xbrl.fields['NetIncomeAttributableToParent'] - self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']) - self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']
        lngIS9 = (self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] + self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']) - self.xbrl.fields['ComprehensiveIncome']
        lngIS10 = (self.xbrl.fields['NetIncomeLoss'] + self.xbrl.fields['OtherComprehensiveIncome']) - self.xbrl.fields['ComprehensiveIncome']
        lngIS11 = self.xbrl.fields['OperatingIncomeLoss'] - (self.xbrl.fields['Revenue'] - self.xbrl.fields['CostsAndExpenses'] + self.xbrl.fields['OtherOperatingIncome'])


        ###Cash flow statement

        #NetCashFlow
        try:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:CashAndCashEquivalentsPeriodIncreaseDecrease", "Duration")
        except:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("g:CashAndCashEquivalentsPeriodIncreaseDecrease", "Duration")
        if self.xbrl.fields['NetCashFlow']== None:
            try:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:CashPeriodIncreaseDecrease", "Duration")
            except:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("g:CashPeriodIncreaseDecrease", "Duration")
            if self.xbrl.fields['NetCashFlow']== None:
                try:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInContinuingOperations", "Duration")
                except:self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInContinuingOperations", "Duration")
                if self.xbrl.fields['NetCashFlow']== None:
                    self.xbrl.fields['NetCashFlow'] = 0

        #NetCashFlowsOperating
        try:self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInOperatingActivities", "Duration")
        except:self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInOperatingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsOperating']== None:
            self.xbrl.fields['NetCashFlowsOperating'] = 0

        #NetCashFlowsInvesting
        try:self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInInvestingActivities", "Duration")
        except:self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInInvestingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsInvesting']== None:
            self.xbrl.fields['NetCashFlowsInvesting'] = 0

        #NetCashFlowsFinancing
        try:self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInFinancingActivities", "Duration")
        except:self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInFinancingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancing']== None:
            self.xbrl.fields['NetCashFlowsFinancing'] = 0
        #NetCashFlowsOperatingContinuing
        try:self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingContinuing']== None:
            self.xbrl.fields['NetCashFlowsOperatingContinuing'] = 0

        #NetCashFlowsInvestingContinuing
        try:self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingContinuing']== None:
            self.xbrl.fields['NetCashFlowsInvestingContinuing'] = 0

        #NetCashFlowsFinancingContinuing
        try:self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingContinuing']== None:
            self.xbrl.fields['NetCashFlowsFinancingContinuing'] = 0

        #NetCashFlowsOperatingDiscontinued
        try:self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = self.xbrl.GetFactValue("g:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingDiscontinued']==None:
            self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = 0

        #NetCashFlowsInvestingDiscontinued
        try:self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = self.xbrl.GetFactValue("g:CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = 0

        #NetCashFlowsFinancingDiscontinued
        try:self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = self.xbrl.GetFactValue("g:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = 0

        #NetCashFlowsDiscontinued
        try:self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInDiscontinuedOperations", "Duration")
        except:self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.GetFactValue("g:NetCashProvidedByUsedInDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsDiscontinued'] = 0

        #ExchangeGainsLosses
        try:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:EffectOfExchangeRateOnCashAndCashEquivalents", "Duration")
        except:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("g:EffectOfExchangeRateOnCashAndCashEquivalents", "Duration")
        if self.xbrl.fields['ExchangeGainsLosses']== None:
            try:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", "Duration")
            except:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("g:EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", "Duration")
            if self.xbrl.fields['ExchangeGainsLosses']== None:
                try:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
                except:self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("g:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
                if self.xbrl.fields['ExchangeGainsLosses']== None:
                    self.xbrl.fields['ExchangeGainsLosses'] = 0

        ####Adjustments
        #Impute: total net cash flows discontinued if not reported
        if self.xbrl.fields['NetCashFlowsDiscontinued']==0:
            self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] + self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] + self.xbrl.fields['NetCashFlowsFinancingDiscontinued']

        #Impute: cash flows from continuing
        if self.xbrl.fields['NetCashFlowsOperating']!=0 and self.xbrl.fields['NetCashFlowsOperatingContinuing']==0:
            self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.fields['NetCashFlowsOperating'] - self.xbrl.fields['NetCashFlowsOperatingDiscontinued']
        if self.xbrl.fields['NetCashFlowsInvesting']!=0 and self.xbrl.fields['NetCashFlowsInvestingContinuing']==0:
            self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.fields['NetCashFlowsInvesting'] - self.xbrl.fields['NetCashFlowsInvestingDiscontinued']
        if self.xbrl.fields['NetCashFlowsFinancing']!=0 and self.xbrl.fields['NetCashFlowsFinancingContinuing']==0:
            self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.fields['NetCashFlowsFinancing'] - self.xbrl.fields['NetCashFlowsFinancingDiscontinued']


        if self.xbrl.fields['NetCashFlowsOperating']==0 and self.xbrl.fields['NetCashFlowsOperatingContinuing']!=0 and self.xbrl.fields['NetCashFlowsOperatingDiscontinued']==0:
            self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.fields['NetCashFlowsOperatingContinuing']
        if self.xbrl.fields['NetCashFlowsInvesting']==0 and self.xbrl.fields['NetCashFlowsInvestingContinuing']!=0 and self.xbrl.fields['NetCashFlowsInvestingDiscontinued']==0:
            self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.fields['NetCashFlowsInvestingContinuing']
        if self.xbrl.fields['NetCashFlowsFinancing']==0 and self.xbrl.fields['NetCashFlowsFinancingContinuing']!=0 and self.xbrl.fields['NetCashFlowsFinancingDiscontinued']==0:
            self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.fields['NetCashFlowsFinancingContinuing']


        self.xbrl.fields['NetCashFlowsContinuing'] = self.xbrl.fields['NetCashFlowsOperatingContinuing'] + self.xbrl.fields['NetCashFlowsInvestingContinuing'] + self.xbrl.fields['NetCashFlowsFinancingContinuing']

        #Impute: if net cash flow is missing,: this tries to figure out the value by adding up the detail
        if self.xbrl.fields['NetCashFlow']==0 and (self.xbrl.fields['NetCashFlowsOperating']!=0 or self.xbrl.fields['NetCashFlowsInvesting']!=0 or self.xbrl.fields['NetCashFlowsFinancing']!=0):
            self.xbrl.fields['NetCashFlow'] = self.xbrl.fields['NetCashFlowsOperating'] + self.xbrl.fields['NetCashFlowsInvesting'] + self.xbrl.fields['NetCashFlowsFinancing']


        lngCF1 = self.xbrl.fields['NetCashFlow'] - (self.xbrl.fields['NetCashFlowsOperating'] + self.xbrl.fields['NetCashFlowsInvesting'] + self.xbrl.fields['NetCashFlowsFinancing'] + self.xbrl.fields['ExchangeGainsLosses'])
        if lngCF1!=0 and (self.xbrl.fields['NetCashFlow'] - (self.xbrl.fields['NetCashFlowsOperating'] + self.xbrl.fields['NetCashFlowsInvesting'] + self.xbrl.fields['NetCashFlowsFinancing'] + self.xbrl.fields['ExchangeGainsLosses'])==(self.xbrl.fields['ExchangeGainsLosses']*-1)):
            lngCF1 = 888888
            #What is going on here is that 171 filers compute net cash flow differently than everyone else.
            #What I am doing is marking these by setting the value of the test to a number 888888 which would never occur naturally, so that I can differentiate this from errors.
        lngCF2 = self.xbrl.fields['NetCashFlowsContinuing'] - (self.xbrl.fields['NetCashFlowsOperatingContinuing'] + self.xbrl.fields['NetCashFlowsInvestingContinuing'] + self.xbrl.fields['NetCashFlowsFinancingContinuing'])
        lngCF3 = self.xbrl.fields['NetCashFlowsDiscontinued'] - (self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] + self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] + self.xbrl.fields['NetCashFlowsFinancingDiscontinued'])
        lngCF4 = self.xbrl.fields['NetCashFlowsOperating'] - (self.xbrl.fields['NetCashFlowsOperatingContinuing'] + self.xbrl.fields['NetCashFlowsOperatingDiscontinued'])
        lngCF5 = self.xbrl.fields['NetCashFlowsInvesting'] - (self.xbrl.fields['NetCashFlowsInvestingContinuing'] + self.xbrl.fields['NetCashFlowsInvestingDiscontinued'])
        lngCF6 = self.xbrl.fields['NetCashFlowsFinancing'] - (self.xbrl.fields['NetCashFlowsFinancingContinuing'] + self.xbrl.fields['NetCashFlowsFinancingDiscontinued'])
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
        #print('ANTOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONIO')
        conn_string = "host='localhost' dbname='mysite' user='postgres' password=''"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        lst = []
        try:start_dt = self.xbrl.getNode("gsd:ReportingPeriodStartDate").text
        except:start_dt = self.xbrl.getNode("c:ReportingPeriodStartDate").text
        try:end_dt = self.xbrl.getNode("gsd:ReportingPeriodEndDate").text
        except:end_dt = self.xbrl.getNode("c:ReportingPeriodEndDate").text
        columns = ['DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherOperatingIncomeAndExpenses', 'DescriptionOfMethodsOfStatingKeyFiguresAndFinancialRatiosIncludedInManagementReview', 'GainsLossesFromCurrentValueAdjustmentsOfOtherInvestmentAssets', 'NetCashFlowsFinancingDiscontinued', 'NonoperatingIncomeLossPlusInterestAndDebtExpense', 'OtherInvestmentAssets', 'ProfitLoss', 'DisclosureOfProvisions', 'InformationOnReceivablesFromOwnersAndManagement', 'DisclosureOfMortgagesAndCollaterals', 'GrossProfitLoss', 'DescriptionOfGeneralMattersRelatedToRecognitionMeasurementAndChangesInAccountingPolicies', 'NetCashFlowsInvestingDiscontinued', '&lt;br/&gt;Selskabet', 'StatementOfChangesInEquity', 'CashAndCashEquivalentsConcerningCashflowStatement', 'ExchangeGainsLosses', 'CostOfSales', 'IncomeFromEquityMethodInvestments', 'NetCashFlowsDiscontinued', 'FeesForAuditorsPerformingStatutoryAudit', 'InformationOnRecognisedButNotOwnedAssets', 'OtherOperatingIncome', 'ProfitLossFromOrdinaryActivitiesBeforeTax', 'ShorttermMortgageDebt', 'CostOfRevenue', 'TaxPayables', 'DisclosureOfLongtermLiabilities', 'Barberens', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfGrossProfitLoss', 'LiabilitiesOtherThanProvisions', 'InformationOnShorttermInvestmentsInAssociates', 'DescriptionOfSignificantEventsOccurringAfterEndOfReportingPeriod', 'InvestmentInPropertyPlantAndEquipment', 'DescriptionOfMethodsOfAmortisationOfNoncurrentAssets', 'IncomeFromInvestmentsInAssociates', 'PropertyPlantAndEquipmentGross', 'ResultsFromNetFinancials', 'IncomeFromContinuingOperationsBeforeTax', 'Ledelsen', 'EmployeeBenefitsExpense', 'SharePremium', 'OtherInterestExpenses', 'TaxExpenseOnOrdinaryActivities', 'Provisions', 'LongtermReceivablesFromOwnersAndManagement', 'InformationOnOmissionOfConsolidatedFinancialStatement', 'IncomeFromInvestmentsInGroupEnterprises', 'AdditionsToPropertyPlantAndEquipment', 'PropertyPlantAndEquipmentInProgress', 'LongtermDebtToOtherCreditInstitutions', 'RawMaterialsAndConsumables', 'anpartshaver&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;p&gt;&lt;span', 'TemporaryEquity', 'PrepaymentsForGoods', 'Auditor', 'CCTC', 'DescriptionOfAccountingPoliciesRelatedToDerivativeFinancialInstruments', 'Kontrakter', 'DisclosureOfRelatedParties', 'NetIncomeLoss', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisIncludingBasesUsedForRevaluationsDepreciationAmortisationEstimatedResidualValueUsefulLifeWritedownsUpwardAndDownwardAdjustments', 'Andre', 'ShorttermPrepaymentsReceivedFromCustomers', 'InterestAndDebtExpense', 'PayablesToShareholdersAndManagement', 'CurrentDeferredTaxAssets', 'InformationOnConsolidations', 'OpinionOnAuditedFinancialStatements', 'Ved', 'DepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssetsRecognisedInProfitOrLoss', 'Restl\xc3\xb8betid', 'DividendPaid', 'FeesForAuditorsPerformingTaxConsultancy', 'OtherComprehensiveIncome', 'RevaluationReserve', 'InformationOnConsolidatedFinancialStatements', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherInvestmentAssets', 'ComprehensiveIncome', 'DisclosureOfContingentLiabilities', 'MortgageDebt', 'DepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssets', 'DocumentType', 'AcquiredLicences', 'NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments', 'ShorttermReceivablesFromAssociates', 'NameOfComponentOfCashFlowsFromUsedInInvestingActivities', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfProvisions', 'DisclosureOfPropertyPlantAndEquipment', 'Revenue', 'ShorttermDebtToBanks', 'ShorttermPayablesToAssociates', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfTaxExpenses', 'DisclosureOfRevenue', 'ExchangeRateProfit', 'InformationOnCalculationOfKeyFiguresAndFinancialRatios', 'Positive', 'OtherShorttermReceivables', 'Egenkapitalen', 'ProposedDividendRecognisedInEquity', 'MP-AX', 'DisclosureOfAnyUnusualMatters', 'InvestmentProperty', 'AmountOfComponentOfCashFlowsFromUsedInInvestingActivities', 'DissolutionOfPreviousYearsRevaluations', 'typedMember', 'DisclosureOfProvisionsForDeferredTax', 'ProfitLossRelatedToInvestments', 'LongtermTaxPayablesToGroupEnterprises', 'LiabilitiesAndEquity', 'ShorttermPayablesToGroupEnterprises', 'ShorttermDebtToBanksCashFlowsStatement', 'ExplanationOfEntitysDefinitionOfCashAndCashEquivalents', 'DisclosureOfDepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssetsRecognisedInProfitOrLoss', 'OperatingIncomeLoss', 'NonoperatingIncomeLoss', 'DividendPaidCashFlow', 'DisclosureOfContingentAssets', 'AmountOfComponentOfCashFlowsFromUsedInOperatingActivities', 'Tilgodehavende', 'OtherDisclosures', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfPropertyPlantAndEquipment', 'OtherTaxExpenses', 'OtherLongtermReceivables', 'ExtraordaryItemsGainLoss', 'WorkInProgress', 'AdjustmentsForDeferredTax', 'Udskudt', 'Kostprisen', 'IncomeTaxesPaidRefundClassifiedAsOperatingActivities', 'NoncurrentLiabilities', 'CashFlowsFromUsedInOperatingActivities', 'AuditorsFees', 'ClassOfReportingEntity', 'NetCashFlowsInvestingContinuing', 'relatedEntityIdentifier', 'InformationOnShorttermInvestmentsInGroupEnterprises', 'TradePayables', 'ProfitLossFromOrdinaryActivitiesAfterTax', 'CashAndCashEquivalents', 'DescriptionOfMethodsOfLeases', 'ExternalExpenses', 'DisclosureOfOwnership', 'DisclosureOfReceivables', 'InterestPaidClassifiedAsOperatingActivities', 'Goodwill', 'EquityAttributableToParent', 'InformationOnAnyPartOfLiabilityFallingDueInMoreThanFiveYears', 'ImpairmentLossesAndDepreciationOfDisposedPropertyPlantAndEquipment', 'EquityAttributableToNoncontrollingInterest', 'DisclosureOfIncomeFromOtherLongtermInvestmentsAndReceivables', 'InformationOnUncertaintiesRelatingToGoingConcern', 'NonoperatingIncomePlusInterestAndDbtExpnsPlsIncFrmEqtyMthdInvst', 'Kapitalandele', 'DisclosureOfIncomeIncludingDividendIncomeFromInvestmentsInGroupEnterprisesAndAssociates', 'AdjustmentsForDecreaseIncreaseInWorkingCapital', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfLiabilitiesOtherThanProvisions', 'DescriptionMethodsOfRecognitionAndMeasurementBasisForCashFlowsStatement', '&lt;br/&gt;J\xc3\xb8rgen', 'SelectedElementsFromReportingClassD', 'FixturesFittingsToolsAndEquipment', 'SelectedElementsFromReportingClassC', 'CEO', 'xbrl', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfContractWorkInProgress', 'ShareHeldByEntityOrConsolidatedEnterprisesInRelatedEntity', 'OtherShorttermPayables', 'EntityRegistrantName', 'ShorttermTaxPayablesToGroupEnterprises', 'ShorttermTaxPayables', 'DisclosureOfAnyUncertaintyConnectedWithRecognitionOrMeasurement', 'NameOfComponentOfCashFlowsFromUsedInOperatingActivities', 'Nettorenteb\xc3\xa6rende', 'InformationOnReportingClassOfEntity', 'CashFlowsStatement', 'BiologicalAssets', 'Planes', 'GainsLossesFromCurrentValueAdjustmentsOfDebtLiabilitiesConcerningInvestmentProperty', 'ShorttermInvestmentsInGroupEnterprises', 'IncomeStatementPeriodYTD', 'componentOfCashFlowsIdentifier', 'Udskudte', 'Erik', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIncomeStatementItems', 'DisposalsOfIntangibleAssets', 'IncomeFromDiscontinuedOperations', 'OtherFinanceIncome', '?xml', 'DistributionCosts', 'LongtermLiabilitiesOtherThanProvisions', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfAssetsAndLiabilities', 'ExplanationOfPrepayments', 'DisclosureOfLiabilitiesOtherThanProvisions', 'Afsat', 'WritedownsOfCurrentAssetsOtherThanCurrentFinancialAssets', 'DepositsLongtermInvestmentsAndReceivables', 'RepaymentsOfLongtermLiabilitiesClassifiedAsFinancingActivities', 'CurrentAssets', 'Dividend', 'DisclosureOfCashAndCashEquivalents', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfEmployeeBenefitExpense', 'InformationOnOtherShorttermInvestments', 'InformationOnSegments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInventories', 'KINONDO', 'Netto', 'DisclosureOfEmployeeBenefitsExpense', 'TransferredToFromReservesAvailable', 'NetCashFlowsOperatingDiscontinued', 'SupplementaryInformationOnOtherMattersExtendedReview', 'PaidContributedCapital', 'ShorttermInvestments', 'Adjustments', 'Virksomhedens', 'AdjustmentsForDeferredTaxCashFlow', 'AccumulatedImpairmentLossesAndDepreciationOfPropertyPlantAndEquipment', 'Equity', 'DevelopmentProjectsInProgress', 'NameAndSurnameOfMemberOfSupervisoryBoard', '&lt;p', 'OtherInterestIncome', 'Da', 'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities', 'CurrentLiabilities', 'InformationOnReconciliationOfChangesInIntangibleAssets', 'RestOfOtherReserves', 'DisclosureOfTaxExpenseOnOrdinaryActivities', 'ShorttermDebtToOtherCreditInstitutions', 'DisclosureOfShorttermLiabilities', 'DisclosureOfInvestments', 'IntangibleAssets', 'ShorttermPayablesToShareholdersAndManagement', 'IncomeBeforeEquityMethodInvestments', 'Omkostninger', 'DisclosureOfContributedCapital', 'ShorttermReceivablesDividendsFromGroupEnterprises', 'ShorttermTradeReceivables', 'DisclosureOfAccountingPolicies', 'InformationOnRevaluatedOrWrittenDownLongtermInvestmentsNotContinuouslyAdjustedToFairValue', 'LongtermLeaseCommitments', 'RawMaterialsAndConsumablesUsed', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfTaxPayablesAndDeferredTax', '&lt;br/&gt;\xc3\x85rets', 'ProfitLossFromOrdinaryOperatingActivitiesBeforeGainsLossesFromFairValueAdjustments', 'DescriptionOfMethodsOfInvestmentsAsCurrentAssets', 'ExtraordinaryDividendPaid', 'Afskrivningsgrundlaget', 'TaxExpense', 'OtherExternalExpenses', 'Aktivitetsniveauet', 'DebtToBanks', 'ProvisionsForDeferredTax', 'CashFlowsFromUsedInFinancingActivities', 'Assets', 'NoncurrentAssets', 'explicitMember', 'DisclosureOfDiscontinuedOperations', 'DescriptionOfMethodsOfDividends', 'OtherLongtermPayables', 'NetIncomeAttributableToNoncontrollingInterest', 'NetCashFlowsFinancing', 'DescriptionOfMethodsOfTranslationOfForeignCurrencies', 'NetCashFlowsFinancingContinuing', 'LongtermPayablesToShareholdersAndManagement', 'InformationOnRelatedEntities', 'For', 'ShorttermReceivablesFromOwnersAndManagement', 'NameOfComponentOfCashFlowsFromUsedInFinancingActivities', 'LandAndBuildings', 'DisclosureOfEquity', 'OtherShorttermDebtRaisedByIssuanceOfBonds', 'ExtraordinaryProfitLossBeforeTax', 'AccumulatedRevaluationsOfInvestments', 'DescriptionOfMethodsOfInvestments', 'LongtermMortgageDebt', 'LongtermPayablesToGroupEnterprises', 'Tilgodehavendet', 'IncomeFromOtherLongtermInvestmentsAndReceivables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCashAndCashEquivalents', 'OtherShorttermInvestments', 'ShorttermPartOfLongtermLiabilitiesOtherThanProvisions', 'AcquiredOtherSimilarRights', 'DisclosureOfInventories', 'AverageNumberOfEmployees', 'ProceedsFromSalesOfIntangibleAssetsClassifiedAsInvestingActivities', '&lt;br/&gt;mellemv\xc3\xa6rende', 'InformationOnContractWorkInProgress', 'PurchaseOfInvestments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfExtraordinaryIncomeAndExpenses', 'Omfanget', 'context', 'SocialSecurityContributions', 'AdditionsToInvestments', 'InformationOnAuditorsFees', 'Inventories', 'ChangeInInventoriesOfFinishedGoodsWorkInProgressAndGoodsForResale', 'DisclosureOfOtherFinanceIncomeFromGroupEnterprises', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIncomeAndExpensesFromInvestmentsInGroupEnterprisesAndAssociates', 'DisclosureOfOtherFinanceIncome', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCostOfProduction', 'AmountOfComponentOfCashFlowsFromUsedInFinancingActivities', 'DisclosureOfOtherArrangementsNotRecognisedInBalanceSheet', 'Nettoopskrivning', 'ContextForInstants', 'NetCashFlowsInvesting', 'DepositsShorttermLiabilitiesOtherThanProvisions', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCostOfSales', 'ShorttermTaxReceivables', 'ComprehensiveIncomeAttributableToNoncontrollingInterest', 'Nettorealisationsv\xc3\xa6rdi', 'DisclosureOfTaxExpenses', 'CostsAndExpenses', 'DisclosureOfUncertaintiesRelatingToGoingConcern', 'LongtermInvestmentsInAssociates', 'DeferredIncomeAssets', 'DisposalsOfInvestments', 'ShorttermDeferredIncome', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfReceivables', 'IncomeTaxExpenseBenefit', 'ShorttermTradePayables', 'ProposedDividend', 'LongtermTaxPayables', 'CashFlowFromOrdinaryOperatingActivities', 'OperatingExpenses', 'Liabilities', 'ContractWorkInProgress', 'RelatedEntityName', 'ComprehensiveIncomeAttributableToParent', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfDeferredIncomeAssets', 'GainsLossesFromCurrentValueAdjustmentsOfInvestmentAssets', 'PrepaymentsForPropertyPlantAndEquipment', 'RestOfOtherFinanceExpenses', 'GainsLossesFromCurrentValueAdjustmentsOfInvestmentProperty', 'OtherOperatingExpenses', 'AccumulatedImpairmentLossesAndAmortisationOfIntangibleAssets', 'InformationOnNoncomparabilityOrRestatement', 'Til', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInvestments', 'GainsLossesFromCurrentValueAdjustmentsOfFinancialInstrumentsFinanceExpenses', 'DescriptionOfMethodsOfCurrentTaxReceivablesAndLiabilities', 'FinanceExpensesArisingFromGroupEnterprises', 'IncreaseDecreaseOfInvestmentsThroughNetExchangeDifferences', 'NetCashFlow', 'WagesAndSalaries', 'NetCashFlowsContinuing', 'DisclosureOfIntangibleAssets', '&lt;br/&gt;Peter', 'PlantAndMachinery', 'ExchangeRateLoss', 'ProvisionsForInvestmentsInGroupEnterprises', 'I', 'DescriptionOfMethodsOfImpairmentLossesAndDepreciation', 'DisclosureOfOtherFinanceExpenses', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInvestmentProperty', 'NumberOfEmployees', 'CurrentTaxExpense', 'LeaseholdImprovements', 'Som', 'PostemploymentBenefitExpense', 'ShorttermTaxReceivablesFromGroupEnterprises', 'NameAndSurnameOfMemberOfExecutiveBoard', 'ManufacturedGoodsAndGoodsForResale', 'AccountingPoliciesAreUnchangedFromPreviousPeriod', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfAdministrativeExpenses', 'PrepaymentsForIntangibleAssets', 'DisclosureOfLiabilitiesUnderLeases', 'ExplanationOfOtherMethodsOfRecognitionAndMeasurementBasisForAssetsInPreviousPeriod', 'InformationOnLeasingContracts', 'FeesForOtherServicesPerformedByAuditors', '\xc3\x85rets', 'RetainedEarnings', 'ContributedCapital', 'CostOfProduction', 'NetIncomeAvailableToCommonStockholdersBasic', 'TaxExpenseOnExtraordinaryEvents', 'Materielle', 'OtherLongtermInvestments', 'ProfitLossFromOrdinaryOperatingActivities', 'CommitmentsAndContingencies', 'EntityCentralIndexKey', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfEquity', 'DisclosureOfCollateralsAndAssetsPledgesAsSecurity', 'ReserveForNetRevaluationAccordingToEquityMethod', 'CashFlowFromOperatingActivitiesBeforeFinancialItems', 'RepaymentOfDebtToCreditInstitutions', 'IncomeFromContinuingOperationsAfterTax', 'InformationOnOtherReceivables', 'konklusion.&lt;/span&gt;&lt;br', 'OtherFinanceExpenses', 'OtherPayables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherOperatingExpenses', 'CompletedDevelopmentProjects', 'PreferredStockDividendsAndOtherAdjustments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisForInvestmentsInSubsidiariesAndAssociates', 'LongtermInvestmentsAndReceivables', 'DisclosureOfMainActivitiesAndAccountingAndFinancialMatters', 'DescriptionOfAmortisationForIntangibleAssetsExceedingFiveYears', '&lt;br/&gt;Foresl\xc3\xa5et', 'NetIncomeAttributableToParent', 'InformationOnRemunerationOfManagementCategoriesAndSpecialIncentiveProgrammes', 'ContingentLiabilitiesRelatedToGroupEnterprises', 'ShorttermReceivables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfFinanceIncomeAndExpenses', 'OtherLongtermDebtRaisedByIssuanceOfBonds', 'DepreciationOfPropertyPlantAndEquipment', 'DescriptionOfMethodsOfPrepayments', 'ExtraordinaryIncome', 'DescriptionOfMethodsOfForeignCurrencies', 'OtherEmployeeExpense', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfDeferredIncomeLiabilities', 'SaleOfInvestments', 'DisclosureOfOtherOperatingExpenses', 'DescriptionOfMethodsOfHedgingRecognisedExpectedToReceiveAndAssumedAssetsAndLiabilities', 'AdjustmentsOfHedgingInstruments', 'LongtermReceivablesFromGroupEnterprises', 'OtherFinanceIncomeFromGroupEnterprises', 'AmortisationOfIntangibleAssets', 'ReserveForNetRevaluationOfInvestmentAssets', 'OtherProvisions', 'InformationOnIntragroupTransactions', 'OtherReserves', 'NoncurrentDeferredTaxAssets', 'Chairmen', 'Modervirksomheden', 'PropertyPlantAndEquipment', 'Der', 'Det', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfGainsLossesFromCurrentValueAdjustmentsOfOtherInvestmentAssets', 'LongtermEquityLoan', 'Den', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfRevenue', 'NetCashFlowsOperatingContinuing', 'CashFlowsFromUsedInInvestingActivities', 'PropertyCost', 'ContextForDurations', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfLeaseholdImprovements', 'Efter', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIntangibleAssets', 'NetIncreaseDecreaseInCashAndCashEquivalents', 'DisposalsOfPropertyPlantAndEquipment', '&lt;br/&gt;som', '&lt;/span&gt;&lt;/p&gt;&lt;p&gt;&lt;br', 'InformationOnChangesAndEffectsOfChangesOnRecognitionAndMeasurementBasisResultingFromChangesInAccountingEstimatesOrErrors', 'ImpairmentLossesAndAmortisationOfDisposedIntangibleAssets', 'ShorttermReceivablesFromGroupEnterprises', 'ShorttermLiabilitiesOtherThanProvisions', 'DepositsLongtermLiabilitiesOtherThanProvisions', 'LongtermReceivablesFromAssociates', 'ImpairmentOfFinancialAssets', 'IntangibleAssetsGross', 'InformationOnAverageNumberOfEmployees', 'NetCashFlowsOperating', 'InterestReceivedClassifiedAsOperatingActivities', 'ProceedsFromSalesOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities', 'GrossProfit', 'ProvisionsForInvestmentsInGroupAssociates', 'LongtermDebtToBanks', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfExternalExpenses', 'AcquisitionOfOtherCompany', 'PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities', 'InvestmentsGross', 'DisclosureOfExternalExpenses', 'LongtermInvestmentsInGroupEnterprises', 'Selskabet', 'IncomeFromInvestmentsInGroupEnterprisesAndAssociates', 'GrossResult', 'BalanceSheetDate', 'AdministrativeExpenses', 'InformationOnReconciliationOfChangesInInvestments', 'AdditionsToIntangibleAssets']        
        dic = {}
        #print(dic)
        result_dic = {}
        #x.getNode("e:Assets[@contextRef='"+x.fields['ContextForInstants']+"']").text
        for item in self.xbrl.tags: 
            try:
                item_name = item.split(':')[1]
                tag = item.split(':')[0]
                if '>' in item_name:
                    item_name = item_name.split('>')[0]
                    item = item.split('>')[0]
                if '<' in tag:
                    tag = tag.split('<')[0]
            except:item_name = item
            try: dic[item_name] = self.xbrl.getNode(tag+':'+item_name+"[@contextRef='"+self.xbrl.fields['ContextForInstants']+"']").text
            except: 
                try:    dic[item_name] = self.xbrl.getNode(tag+':'+item_name+"[@contextRef='"+self.xbrl.fields['ContextForDurations']+"']").text
                except: dic[item_name] = '0'

        #print(dic)   
                
                #dic['DocumentType'] = unicodedata.normalize("NFKD", self.xbrl.getNode("gsd:InformationOnTypeOfSubmittedReport").text)
                #dic['EntityCentralIndexKey'] = self.xbrl.fields['EntityCentralIndexKey']
        try:dic['CEO'] = self.xbrl.getNode('cmn:NameAndSurnameOfMemberOfExecutiveBoard').text
        except:
            try:dic['CEO'] = self.xbrl.getNode('d:NameAndSurnameOfMemberOfExecutiveBoard').text
            except:dic['CEO'] = 'None'
        try:dic['Chairmen'] = self.xbrl.getNode('gsd:NameAndSurnameOfChairmanOfGeneralMeeting').text
        except:
            try:dic['Chairmen'] = self.xbrl.getNode('c:NameAndSurnameOfChairmanOfGeneralMeeting').text
            except:dic['Chairmen'] = 'None'
        try:dic['Auditor'] = self.xbrl.getNode('cmn:NameAndSurnameOfAuditor').text
        except:
            try:dic['Auditor'] = self.xbrl.getNode('d:NameAndSurnameOfAuditor').text
            except:dic['Auditor'] = 'None'
        #try:dic['EntityRegistrantName'] = self.xbrl.fields['EntityRegistrantName']
        #except:
        #    dic['EntityRegistrantName'] = 'None'

        string_lst = []
        
        for item in columns:
            result_dic[item] = 'None'            
        for value in dic:
            for item in result_dic:
                if value == item:
                    #print(value)
                    result_dic[item] = dic[value]           
        for item in self.xbrl.fields:
            #try:
            if result_dic[item] != '0' and self.xbrl.fields[item] == 0:
                    continue
            #except:
            result_dic[item] = self.xbrl.fields[item]
            #print('lil')
            
        i = 0 
        for item in result_dic:
            #if len(item) > 63:
                #result_dic[item[:63]] = result_dic.pop[item]
            try:string_lst.append("'"+str(result_dic[item])+"'")
            except:string_lst.append("'"+str(result_dic[item].encode('utf-8'))+"'")

        #print('antoha',unicodedata.normalize("NFKD", self.xbrl.getNode("gsd:InformationOnTypeOfSubmittedReport").text))
        #print('lol',)
        print(result_dic)
        #print(1,self.xbrl.fields['EntityRegistrantName'])
        #print(666,result_dic['EntityRegistrantName'])
        for item in dic:
            try:
                result_dic[item] = str(result_dic[item]).replace("'","")
            except: pass
                
         
                
        try:
            cursor.execute("INSERT INTO django_sec_new VALUES("+self.xbrl.fields['EntityCentralIndexKey']+", '"+start_dt+"', '"+end_dt+"', "+', '.join(string_lst)+")")
        except Exception as e:
            print(e)
            print(len(string_lst))
            raise
        conn.commit()
        conn.close()
        cursor.close()
        #os.system('python '+os.path.dirname(os.path.realpath(__file__))+'/adjuster.py')
        #print('adJUSTED!!!!')'''
        #Key ratios'''
        #print(dic)
        






