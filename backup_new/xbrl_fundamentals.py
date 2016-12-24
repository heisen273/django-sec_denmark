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
        
        self.xbrl.fields['Assets'] = self.xbrl.GetFactValue("fsa:Assets","Instant")
        if self.xbrl.fields['Assets']== None:
            self.xbrl.fields['Assets'] = 0

        #Current Assets
        self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue("fsa:CurrentAssets", "Instant")
        if self.xbrl.fields['CurrentAssets']== None:
            self.xbrl.fields['CurrentAssets'] = 0
                
        #Noncurrent Assets
        self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("fsa:AssetsNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentAssets']==None:
            self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("fsa:NoncurrentAssets", "Instant")
            if self.xbrl.fields['NoncurrentAssets']==None:
                if self.xbrl.fields['Assets'] and self.xbrl.fields['CurrentAssets']:
                    self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']
                else:
                    self.xbrl.fields['NoncurrentAssets'] = 0
                
        #LiabilitiesAndEquity
        self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndStockholdersEquity", "Instant")
        if self.xbrl.fields['LiabilitiesAndEquity']== None:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndPartnersCapital", "Instant")
            if self.xbrl.fields['LiabilitiesAndEquity']== None:
                self.xbrl.fields['LiabilitiesAndEquity'] = 0
        
        #Liabilities
        self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue("fsa:Liabilities", "Instant")
        if self.xbrl.fields['Liabilities']== None:
            self.xbrl.fields['Liabilities'] = 0
        #CurrentLiabilities
        self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue("fsa:LiabilitiesCurrent", "Instant")
        if self.xbrl.fields['CurrentLiabilities']== None:
            self.xbrl.fields['CurrentLiabilities'] = 0
                
        #Noncurrent Liabilities
        self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("fsa:LiabilitiesNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentLiabilities']== None:
            self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("fsa:LiabilitiesNoncurrent", "Instant")
            if self.xbrl.fields['NoncurrentLiabilities']== None:
                if self.xbrl.fields['Liabilities'] and self.xbrl.fields['CurrentLiabilities']:
                    self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - self.xbrl.fields['CurrentLiabilities']
                else:
                    self.xbrl.fields['NoncurrentLiabilities'] = 0
                
        #CommitmentsAndContingencies
        self.xbrl.fields['CommitmentsAndContingencies'] = self.xbrl.GetFactValue("fsa:CommitmentsAndContingencies", "Instant")
        if self.xbrl.fields['CommitmentsAndContingencies']== None:
            self.xbrl.fields['CommitmentsAndContingencies'] = 0
                
        #TemporaryEquity
        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityRedemptionValue", "Instant")
        if self.xbrl.fields['TemporaryEquity'] == None:
            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:RedeemablePreferredStockCarryingAmount", "Instant")
            if self.xbrl.fields['TemporaryEquity'] == None:
                self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityCarryingAmount", "Instant")
                if self.xbrl.fields['TemporaryEquity'] == None:
                    self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityValueExcludingAdditionalPaidInCapital", "Instant")
                    if self.xbrl.fields['TemporaryEquity'] == None:
                        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:TemporaryEquityCarryingAmountAttributableToParent", "Instant")
                        if self.xbrl.fields['TemporaryEquity'] == None:
                            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityFairValue", "Instant")
                            if self.xbrl.fields['TemporaryEquity'] == None:
                                self.xbrl.fields['TemporaryEquity'] = 0
                 
        #RedeemableNoncontrollingInterest (added to temporary equity)
        RedeemableNoncontrollingInterest = None
        
        RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityCarryingAmount", "Instant")
        if RedeemableNoncontrollingInterest == None:
            RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("fsa:RedeemableNoncontrollingInterestEquityCommonCarryingAmount", "Instant")
            if RedeemableNoncontrollingInterest == None:
                RedeemableNoncontrollingInterest = 0

        #This adds redeemable noncontrolling interest and temporary equity which are rare, but can be reported seperately
        if self.xbrl.fields['TemporaryEquity']:
            self.xbrl.fields['TemporaryEquity'] = float(self.xbrl.fields['TemporaryEquity']) + float(RedeemableNoncontrollingInterest)


        #Equity
        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "Instant")
        if self.xbrl.fields['Equity'] == None:
            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:Equity", "Instant")
            if self.xbrl.fields['Equity'] == None:
                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest", "Instant")
                if self.xbrl.fields['Equity'] == None:
                    self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:PartnersCapital", "Instant")
                    if self.xbrl.fields['Equity'] == None:
                        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:CommonStockholdersEquity", "Instant")
                        if self.xbrl.fields['Equity'] == None:
                            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:MemberEquity", "Instant")
                            if self.xbrl.fields['Equity'] == None:
                                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("fsa:AssetsNet", "Instant")
                                if self.xbrl.fields['Equity'] == None:
                                    self.xbrl.fields['Equity'] = 0
        

        #EquityAttributableToNoncontrollingInterest
        self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:MinorityInterest", "Instant")
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
            self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:PartnersCapitalAttributableToNoncontrollingInterest", "Instant")
            if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
                self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = 0
        
        #EquityAttributableToParent
        self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("fsa:StockholdersEquity", "Instant")
        if self.xbrl.fields['EquityAttributableToParent'] == None:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("fsa:LiabilitiesAndPartnersCapital", "Instant")
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
        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:Revenue", "Duration")
        if self.xbrl.fields['Revenue'] == None:
            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:SalesRevenueNet", "Duration")
            if self.xbrl.fields['Revenue'] == None:
                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:SalesRevenueervicesNet", "Duration")
                if self.xbrl.fields['Revenue'] == None:
                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RevenueNetOfInterestExpense", "Duration")
                    if self.xbrl.fields['Revenue'] == None:
                        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                        if self.xbrl.fields['Revenue'] == None:
                            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:HealthCareOrganizationRevenue", "Duration")
                            if self.xbrl.fields['Revenue'] == None:
                                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:InterestAndDividendIncomeOperating", "Duration")
                                if self.xbrl.fields['Revenue'] == None:
                                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RealEstateRevenueNet", "Duration")
                                    if self.xbrl.fields['Revenue'] == None:
                                        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RevenueMineralSales", "Duration")
                                        if self.xbrl.fields['Revenue'] == None:
                                            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:OilAndGasRevenue", "Duration")
                                            if self.xbrl.fields['Revenue'] == None:
                                                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:FinancialServicesRevenue", "Duration")
                                                if self.xbrl.fields['Revenue'] == None:
                                                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("fsa:RegulatedAndUnregulatedOperatingRevenue", "Duration")                                                
                                                    if self.xbrl.fields['Revenue'] == None:
                                                        self.xbrl.fields['Revenue'] = 0


        #CostOfRevenue
        self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfRevenue", "Duration")
        if self.xbrl.fields['CostOfRevenue'] == None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfServices", "Duration")
            if self.xbrl.fields['CostOfRevenue'] == None:
                self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfGoodsSold", "Duration")
                if self.xbrl.fields['CostOfRevenue'] == None:
                    self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("fsa:CostOfGoodsAndServicesSold", "Duration")
                    if self.xbrl.fields['CostOfRevenue'] == None:
                        self.xbrl.fields['CostOfRevenue'] = 0
     
        #GrossProfit
        self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("fsa:GrossProfit", "Duration")
        if self.xbrl.fields['GrossProfit'] == None:
            self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("fsa:GrossProfit", "Duration")
            if self.xbrl.fields['GrossProfit'] == None:
                self.xbrl.fields['GrossProfit'] = 0
     
        #OperatingExpenses
        self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("fsa:OperatingExpenses", "Duration")
        if self.xbrl.fields['OperatingExpenses'] == None:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("fsa:OperatingCostsAndExpenses", "Duration")  #This concept seems incorrect.
            if self.xbrl.fields['OperatingExpenses'] == None:
                self.xbrl.fields['OperatingExpenses'] = 0
        #CostsAndExpenses
        self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("fsa:CostsAndExpenses", "Duration")
        if self.xbrl.fields['CostsAndExpenses'] == None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("fsa:CostsAndExpenses", "Duration")
            if self.xbrl.fields['CostsAndExpenses'] == None:
                self.xbrl.fields['CostsAndExpenses'] = 0
     
        #OtherOperatingIncome
        self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("fsa:OtherOperatingIncome", "Duration")
        if self.xbrl.fields['OtherOperatingIncome'] == None:
            self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("fsa:OtherOperatingIncome", "Duration")
            if self.xbrl.fields['OtherOperatingIncome'] == None:
                self.xbrl.fields['OtherOperatingIncome'] = 0
     
        #OperatingIncomeLoss
        self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:OperatingIncomeLoss", "Duration")
        if self.xbrl.fields['OperatingIncomeLoss'] == None:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:OperatingIncomeLoss", "Duration")
            if self.xbrl.fields['OperatingIncomeLoss'] == None:
                self.xbrl.fields['OperatingIncomeLoss'] = 0
     
        #NonoperatingIncomeLoss
        self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:NonoperatingIncomeExpense", "Duration")
        if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
            self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("fsa:NonoperatingIncomeExpense", "Duration")
            if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
                self.xbrl.fields['NonoperatingIncomeLoss'] = 0

        #InterestAndDebtExpense
        self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("fsa:InterestAndDebtExpense", "Duration")
        if self.xbrl.fields['InterestAndDebtExpense'] == None:
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("fsa:InterestAndDebtExpense", "Duration")
            if self.xbrl.fields['InterestAndDebtExpense'] == None:
                self.xbrl.fields['InterestAndDebtExpense'] = 0

        #IncomeBeforeEquityMethodInvestments
        self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = 0
     
        #IncomeFromEquityMethodInvestments
        self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
            self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("fsa:IncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeFromEquityMethodInvestments'] = 0
     
        #IncomeFromContinuingOperationsBeforeTax
        self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = 0
     
        #IncomeTaxExpenseBenefit
        self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("fsa:IncomeTaxExpenseBenefit", "Duration")
        if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
            self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("fsa:IncomeTaxExpenseBenefitContinuingOperations", "Duration")
            if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
                self.xbrl.fields['IncomeTaxExpenseBenefit'] = 0
        #IncomeFromContinuingOperationsAfterTax
        self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("fsa:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("fsa:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = 0

        #IncomeFromDiscontinuedOperations
        self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:IncomeLossFromDiscontinuedOperationsNetOfTax", "Duration")
        if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
            self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:DiscontinuedOperationGainLossOnDisposalOfDiscontinuedOperationNetOfTax", "Duration")
            if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("fsa:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity", "Duration")
                if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                    self.xbrl.fields['IncomeFromDiscontinuedOperations'] = 0

        #ExtraordaryItemsGainLoss
        self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("fsa:ExtraordinaryItemNetOfTax", "Duration")
        if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
            self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("fsa:ExtraordinaryItemNetOfTax", "Duration")
            if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
                self.xbrl.fields['ExtraordaryItemsGainLoss'] = 0
        #NetIncomeLoss
        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:ProfitLoss", "Duration")
        if self.xbrl.fields['NetIncomeLoss']== None:
            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:NetIncomeLoss", "Duration")
            if self.xbrl.fields['NetIncomeLoss']== None:
                self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
                if self.xbrl.fields['NetIncomeLoss']== None:
                    self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperations", "Duration")
                    if self.xbrl.fields['NetIncomeLoss']== None:
                        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossAttributableToParent", "Duration")
                        if self.xbrl.fields['NetIncomeLoss']== None:
                            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("fsa:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest", "Duration")
                            if self.xbrl.fields['NetIncomeLoss']== None:
                                self.xbrl.fields['NetIncomeLoss'] = 0

        #NetIncomeAvailableToCommonStockholdersBasic
        self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
        if self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']== None:
            self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = 0
                
        #PreferredStockDividendsAndOtherAdjustments
        self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.GetFactValue("fsa:PreferredStockDividendsAndOtherAdjustments", "Duration")
        if self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']== None:
            self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = 0
                
        #NetIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:NetIncomeLossAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest']== None:
            self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = 0
                
        #NetIncomeAttributableToParent
        self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:NetIncomeLoss", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToParent']== None:
            self.xbrl.fields['NetIncomeAttributableToParent'] = 0

        #OtherComprehensiveIncome
        self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:OtherComprehensiveIncomeLossNetOfTax", "Duration")
        if self.xbrl.fields['OtherComprehensiveIncome']== None:
            self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:OtherComprehensiveIncomeLossNetOfTax", "Duration")
            if self.xbrl.fields['OtherComprehensiveIncome']== None:
                self.xbrl.fields['OtherComprehensiveIncome'] = 0

        #ComprehensiveIncome
        self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncome']== None:
            self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncome']== None:
                self.xbrl.fields['ComprehensiveIncome'] = 0

        #ComprehensiveIncomeAttributableToParent
        self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
                self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = 0
     
        #ComprehensiveIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("fsa:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
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
        self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:CashAndCashEquivalentsPeriodIncreaseDecrease", "Duration")
        if self.xbrl.fields['NetCashFlow']== None:
            self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:CashPeriodIncreaseDecrease", "Duration")
            if self.xbrl.fields['NetCashFlow']== None:
                self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInContinuingOperations", "Duration")
                if self.xbrl.fields['NetCashFlow']== None:
                    self.xbrl.fields['NetCashFlow'] = 0
                
        #NetCashFlowsOperating
        self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInOperatingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsOperating']== None:
            self.xbrl.fields['NetCashFlowsOperating'] = 0
                
        #NetCashFlowsInvesting
        self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInInvestingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsInvesting']== None:
            self.xbrl.fields['NetCashFlowsInvesting'] = 0
                
        #NetCashFlowsFinancing
        self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInFinancingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancing']== None:
            self.xbrl.fields['NetCashFlowsFinancing'] = 0
        #NetCashFlowsOperatingContinuing
        self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingContinuing']== None:
            self.xbrl.fields['NetCashFlowsOperatingContinuing'] = 0
                
        #NetCashFlowsInvestingContinuing
        self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingContinuing']== None:
            self.xbrl.fields['NetCashFlowsInvestingContinuing'] = 0
                
        #NetCashFlowsFinancingContinuing
        self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingContinuing']== None:
            self.xbrl.fields['NetCashFlowsFinancingContinuing'] = 0
                
        #NetCashFlowsOperatingDiscontinued
        self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingDiscontinued']==None:
            self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = 0
                
        #NetCashFlowsInvestingDiscontinued
        self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = 0
                
        #NetCashFlowsFinancingDiscontinued
        self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = 0
                
        #NetCashFlowsDiscontinued
        self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.GetFactValue("fsa:NetCashProvidedByUsedInDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsDiscontinued'] = 0
                
        #ExchangeGainsLosses
        self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:EffectOfExchangeRateOnCashAndCashEquivalents", "Duration")
        if self.xbrl.fields['ExchangeGainsLosses']== None:
            self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", "Duration")
            if self.xbrl.fields['ExchangeGainsLosses']== None:
                self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("fsa:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
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
        conn_string = "host='localhost' dbname='vcs' user='postgres' password='123'"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        lst = []
        start_dt = self.xbrl.getNode("gsd:ReportingPeriodStartDate").text
        end_dt = self.xbrl.getNode("gsd:ReportingPeriodEndDate").text
        columns = ['DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherOperatingIncomeAndExpenses', 'DescriptionOfMethodsOfStatingKeyFiguresAndFinancialRatiosIncludedInManagementReview', 'GainsLossesFromCurrentValueAdjustmentsOfOtherInvestmentAssets', 'NetCashFlowsFinancingDiscontinued', 'NonoperatingIncomeLossPlusInterestAndDebtExpense', 'OtherInvestmentAssets', 'ProfitLoss', 'DisclosureOfProvisions', 'InformationOnReceivablesFromOwnersAndManagement', 'DisclosureOfMortgagesAndCollaterals', 'GrossProfitLoss', 'DescriptionOfGeneralMattersRelatedToRecognitionMeasurementAndChangesInAccountingPolicies', 'NetCashFlowsInvestingDiscontinued', '&lt;br/&gt;Selskabet', 'StatementOfChangesInEquity', 'CashAndCashEquivalentsConcerningCashflowStatement', 'ExchangeGainsLosses', 'CostOfSales', 'IncomeFromEquityMethodInvestments', 'NetCashFlowsDiscontinued', 'FeesForAuditorsPerformingStatutoryAudit', 'InformationOnRecognisedButNotOwnedAssets', 'OtherOperatingIncome', 'ProfitLossFromOrdinaryActivitiesBeforeTax', 'ShorttermMortgageDebt', 'CostOfRevenue', 'TaxPayables', 'DisclosureOfLongtermLiabilities', 'Barberens', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfGrossProfitLoss', 'LiabilitiesOtherThanProvisions', 'InformationOnShorttermInvestmentsInAssociates', 'DescriptionOfSignificantEventsOccurringAfterEndOfReportingPeriod', 'InvestmentInPropertyPlantAndEquipment', 'DescriptionOfMethodsOfAmortisationOfNoncurrentAssets', 'IncomeFromInvestmentsInAssociates', 'PropertyPlantAndEquipmentGross', 'ResultsFromNetFinancials', 'IncomeFromContinuingOperationsBeforeTax', 'Ledelsen', 'EmployeeBenefitsExpense', 'SharePremium', 'OtherInterestExpenses', 'TaxExpenseOnOrdinaryActivities', 'Provisions', 'LongtermReceivablesFromOwnersAndManagement', 'InformationOnOmissionOfConsolidatedFinancialStatement', 'IncomeFromInvestmentsInGroupEnterprises', 'AdditionsToPropertyPlantAndEquipment', 'PropertyPlantAndEquipmentInProgress', 'LongtermDebtToOtherCreditInstitutions', 'RawMaterialsAndConsumables', 'anpartshaver&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;p&gt;&lt;span', 'TemporaryEquity', 'PrepaymentsForGoods', 'Auditor', 'CCTC', 'DescriptionOfAccountingPoliciesRelatedToDerivativeFinancialInstruments', 'Kontrakter', 'DisclosureOfRelatedParties', 'NetIncomeLoss', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisIncludingBasesUsedForRevaluationsDepreciationAmortisationEstimatedResidualValueUsefulLifeWritedownsUpwardAndDownwardAdjustments', 'Andre', 'ShorttermPrepaymentsReceivedFromCustomers', 'InterestAndDebtExpense', 'PayablesToShareholdersAndManagement', 'CurrentDeferredTaxAssets', 'InformationOnConsolidations', 'OpinionOnAuditedFinancialStatements', 'Ved', 'DepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssetsRecognisedInProfitOrLoss', 'Restl\xc3\xb8betid', 'DividendPaid', 'FeesForAuditorsPerformingTaxConsultancy', 'OtherComprehensiveIncome', 'RevaluationReserve', 'InformationOnConsolidatedFinancialStatements', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherInvestmentAssets', 'ComprehensiveIncome', 'DisclosureOfContingentLiabilities', 'MortgageDebt', 'DepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssets', 'DocumentType', 'AcquiredLicences', 'NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments', 'ShorttermReceivablesFromAssociates', 'NameOfComponentOfCashFlowsFromUsedInInvestingActivities', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfProvisions', 'DisclosureOfPropertyPlantAndEquipment', 'Revenue', 'ShorttermDebtToBanks', 'ShorttermPayablesToAssociates', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfTaxExpenses', 'DisclosureOfRevenue', 'ExchangeRateProfit', 'InformationOnCalculationOfKeyFiguresAndFinancialRatios', 'Positive', 'OtherShorttermReceivables', 'Egenkapitalen', 'ProposedDividendRecognisedInEquity', 'MP-AX', 'DisclosureOfAnyUnusualMatters', 'InvestmentProperty', 'AmountOfComponentOfCashFlowsFromUsedInInvestingActivities', 'DissolutionOfPreviousYearsRevaluations', 'typedMember', 'DisclosureOfProvisionsForDeferredTax', 'ProfitLossRelatedToInvestments', 'LongtermTaxPayablesToGroupEnterprises', 'LiabilitiesAndEquity', 'ShorttermPayablesToGroupEnterprises', 'ShorttermDebtToBanksCashFlowsStatement', 'ExplanationOfEntitysDefinitionOfCashAndCashEquivalents', 'DisclosureOfDepreciationAmortisationExpenseAndImpairmentLossesOfPropertyPlantAndEquipmentAndIntangibleAssetsRecognisedInProfitOrLoss', 'OperatingIncomeLoss', 'NonoperatingIncomeLoss', 'DividendPaidCashFlow', 'DisclosureOfContingentAssets', 'AmountOfComponentOfCashFlowsFromUsedInOperatingActivities', 'Tilgodehavende', 'OtherDisclosures', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfPropertyPlantAndEquipment', 'OtherTaxExpenses', 'OtherLongtermReceivables', 'ExtraordaryItemsGainLoss', 'WorkInProgress', 'AdjustmentsForDeferredTax', 'Udskudt', 'Kostprisen', 'IncomeTaxesPaidRefundClassifiedAsOperatingActivities', 'NoncurrentLiabilities', 'CashFlowsFromUsedInOperatingActivities', 'AuditorsFees', 'ClassOfReportingEntity', 'NetCashFlowsInvestingContinuing', 'relatedEntityIdentifier', 'InformationOnShorttermInvestmentsInGroupEnterprises', 'TradePayables', 'ProfitLossFromOrdinaryActivitiesAfterTax', 'CashAndCashEquivalents', 'DescriptionOfMethodsOfLeases', 'ExternalExpenses', 'DisclosureOfOwnership', 'DisclosureOfReceivables', 'InterestPaidClassifiedAsOperatingActivities', 'Goodwill', 'EquityAttributableToParent', 'InformationOnAnyPartOfLiabilityFallingDueInMoreThanFiveYears', 'ImpairmentLossesAndDepreciationOfDisposedPropertyPlantAndEquipment', 'EquityAttributableToNoncontrollingInterest', 'DisclosureOfIncomeFromOtherLongtermInvestmentsAndReceivables', 'InformationOnUncertaintiesRelatingToGoingConcern', 'NonoperatingIncomePlusInterestAndDbtExpnsPlsIncFrmEqtyMthdInvst', 'Kapitalandele', 'DisclosureOfIncomeIncludingDividendIncomeFromInvestmentsInGroupEnterprisesAndAssociates', 'AdjustmentsForDecreaseIncreaseInWorkingCapital', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfLiabilitiesOtherThanProvisions', 'DescriptionMethodsOfRecognitionAndMeasurementBasisForCashFlowsStatement', '&lt;br/&gt;J\xc3\xb8rgen', 'SelectedElementsFromReportingClassD', 'FixturesFittingsToolsAndEquipment', 'SelectedElementsFromReportingClassC', 'CEO', 'xbrl', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfContractWorkInProgress', 'ShareHeldByEntityOrConsolidatedEnterprisesInRelatedEntity', 'OtherShorttermPayables', 'EntityRegistrantName', 'ShorttermTaxPayablesToGroupEnterprises', 'ShorttermTaxPayables', 'DisclosureOfAnyUncertaintyConnectedWithRecognitionOrMeasurement', 'NameOfComponentOfCashFlowsFromUsedInOperatingActivities', 'Nettorenteb\xc3\xa6rende', 'InformationOnReportingClassOfEntity', 'CashFlowsStatement', 'BiologicalAssets', 'Planes', 'GainsLossesFromCurrentValueAdjustmentsOfDebtLiabilitiesConcerningInvestmentProperty', 'ShorttermInvestmentsInGroupEnterprises', 'IncomeStatementPeriodYTD', 'componentOfCashFlowsIdentifier', 'Udskudte', 'Erik', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIncomeStatementItems', 'DisposalsOfIntangibleAssets', 'IncomeFromDiscontinuedOperations', 'OtherFinanceIncome', '?xml', 'DistributionCosts', 'LongtermLiabilitiesOtherThanProvisions', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfAssetsAndLiabilities', 'ExplanationOfPrepayments', 'DisclosureOfLiabilitiesOtherThanProvisions', 'Afsat', 'WritedownsOfCurrentAssetsOtherThanCurrentFinancialAssets', 'DepositsLongtermInvestmentsAndReceivables', 'RepaymentsOfLongtermLiabilitiesClassifiedAsFinancingActivities', 'CurrentAssets', 'Dividend', 'DisclosureOfCashAndCashEquivalents', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfEmployeeBenefitExpense', 'InformationOnOtherShorttermInvestments', 'InformationOnSegments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInventories', 'KINONDO', 'Netto', 'DisclosureOfEmployeeBenefitsExpense', 'TransferredToFromReservesAvailable', 'NetCashFlowsOperatingDiscontinued', 'SupplementaryInformationOnOtherMattersExtendedReview', 'PaidContributedCapital', 'ShorttermInvestments', 'Adjustments', 'Virksomhedens', 'AdjustmentsForDeferredTaxCashFlow', 'AccumulatedImpairmentLossesAndDepreciationOfPropertyPlantAndEquipment', 'Equity', 'DevelopmentProjectsInProgress', 'NameAndSurnameOfMemberOfSupervisoryBoard', '&lt;p', 'OtherInterestIncome', 'Da', 'PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities', 'CurrentLiabilities', 'InformationOnReconciliationOfChangesInIntangibleAssets', 'RestOfOtherReserves', 'DisclosureOfTaxExpenseOnOrdinaryActivities', 'ShorttermDebtToOtherCreditInstitutions', 'DisclosureOfShorttermLiabilities', 'DisclosureOfInvestments', 'IntangibleAssets', 'ShorttermPayablesToShareholdersAndManagement', 'IncomeBeforeEquityMethodInvestments', 'Omkostninger', 'DisclosureOfContributedCapital', 'ShorttermReceivablesDividendsFromGroupEnterprises', 'ShorttermTradeReceivables', 'DisclosureOfAccountingPolicies', 'InformationOnRevaluatedOrWrittenDownLongtermInvestmentsNotContinuouslyAdjustedToFairValue', 'LongtermLeaseCommitments', 'RawMaterialsAndConsumablesUsed', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfTaxPayablesAndDeferredTax', '&lt;br/&gt;\xc3\x85rets', 'ProfitLossFromOrdinaryOperatingActivitiesBeforeGainsLossesFromFairValueAdjustments', 'DescriptionOfMethodsOfInvestmentsAsCurrentAssets', 'ExtraordinaryDividendPaid', 'Afskrivningsgrundlaget', 'TaxExpense', 'OtherExternalExpenses', 'Aktivitetsniveauet', 'DebtToBanks', 'ProvisionsForDeferredTax', 'CashFlowsFromUsedInFinancingActivities', 'Assets', 'NoncurrentAssets', 'explicitMember', 'DisclosureOfDiscontinuedOperations', 'DescriptionOfMethodsOfDividends', 'OtherLongtermPayables', 'NetIncomeAttributableToNoncontrollingInterest', 'NetCashFlowsFinancing', 'DescriptionOfMethodsOfTranslationOfForeignCurrencies', 'NetCashFlowsFinancingContinuing', 'LongtermPayablesToShareholdersAndManagement', 'InformationOnRelatedEntities', 'For', 'ShorttermReceivablesFromOwnersAndManagement', 'NameOfComponentOfCashFlowsFromUsedInFinancingActivities', 'LandAndBuildings', 'DisclosureOfEquity', 'OtherShorttermDebtRaisedByIssuanceOfBonds', 'ExtraordinaryProfitLossBeforeTax', 'AccumulatedRevaluationsOfInvestments', 'DescriptionOfMethodsOfInvestments', 'LongtermMortgageDebt', 'LongtermPayablesToGroupEnterprises', 'Tilgodehavendet', 'IncomeFromOtherLongtermInvestmentsAndReceivables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCashAndCashEquivalents', 'OtherShorttermInvestments', 'ShorttermPartOfLongtermLiabilitiesOtherThanProvisions', 'AcquiredOtherSimilarRights', 'DisclosureOfInventories', 'AverageNumberOfEmployees', 'ProceedsFromSalesOfIntangibleAssetsClassifiedAsInvestingActivities', '&lt;br/&gt;mellemv\xc3\xa6rende', 'InformationOnContractWorkInProgress', 'PurchaseOfInvestments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfExtraordinaryIncomeAndExpenses', 'Omfanget', 'context', 'SocialSecurityContributions', 'AdditionsToInvestments', 'InformationOnAuditorsFees', 'Inventories', 'ChangeInInventoriesOfFinishedGoodsWorkInProgressAndGoodsForResale', 'DisclosureOfOtherFinanceIncomeFromGroupEnterprises', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIncomeAndExpensesFromInvestmentsInGroupEnterprisesAndAssociates', 'DisclosureOfOtherFinanceIncome', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCostOfProduction', 'AmountOfComponentOfCashFlowsFromUsedInFinancingActivities', 'DisclosureOfOtherArrangementsNotRecognisedInBalanceSheet', 'Nettoopskrivning', 'ContextForInstants', 'NetCashFlowsInvesting', 'DepositsShorttermLiabilitiesOtherThanProvisions', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfCostOfSales', 'ShorttermTaxReceivables', 'ComprehensiveIncomeAttributableToNoncontrollingInterest', 'Nettorealisationsv\xc3\xa6rdi', 'DisclosureOfTaxExpenses', 'CostsAndExpenses', 'DisclosureOfUncertaintiesRelatingToGoingConcern', 'LongtermInvestmentsInAssociates', 'DeferredIncomeAssets', 'DisposalsOfInvestments', 'ShorttermDeferredIncome', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfReceivables', 'IncomeTaxExpenseBenefit', 'ShorttermTradePayables', 'ProposedDividend', 'LongtermTaxPayables', 'CashFlowFromOrdinaryOperatingActivities', 'OperatingExpenses', 'Liabilities', 'ContractWorkInProgress', 'RelatedEntityName', 'ComprehensiveIncomeAttributableToParent', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfDeferredIncomeAssets', 'GainsLossesFromCurrentValueAdjustmentsOfInvestmentAssets', 'PrepaymentsForPropertyPlantAndEquipment', 'RestOfOtherFinanceExpenses', 'GainsLossesFromCurrentValueAdjustmentsOfInvestmentProperty', 'OtherOperatingExpenses', 'AccumulatedImpairmentLossesAndAmortisationOfIntangibleAssets', 'InformationOnNoncomparabilityOrRestatement', 'Til', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInvestments', 'GainsLossesFromCurrentValueAdjustmentsOfFinancialInstrumentsFinanceExpenses', 'DescriptionOfMethodsOfCurrentTaxReceivablesAndLiabilities', 'FinanceExpensesArisingFromGroupEnterprises', 'IncreaseDecreaseOfInvestmentsThroughNetExchangeDifferences', 'NetCashFlow', 'WagesAndSalaries', 'NetCashFlowsContinuing', 'DisclosureOfIntangibleAssets', '&lt;br/&gt;Peter', 'PlantAndMachinery', 'ExchangeRateLoss', 'ProvisionsForInvestmentsInGroupEnterprises', 'I', 'DescriptionOfMethodsOfImpairmentLossesAndDepreciation', 'DisclosureOfOtherFinanceExpenses', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfInvestmentProperty', 'NumberOfEmployees', 'CurrentTaxExpense', 'LeaseholdImprovements', 'Som', 'PostemploymentBenefitExpense', 'ShorttermTaxReceivablesFromGroupEnterprises', 'NameAndSurnameOfMemberOfExecutiveBoard', 'ManufacturedGoodsAndGoodsForResale', 'AccountingPoliciesAreUnchangedFromPreviousPeriod', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfAdministrativeExpenses', 'PrepaymentsForIntangibleAssets', 'DisclosureOfLiabilitiesUnderLeases', 'ExplanationOfOtherMethodsOfRecognitionAndMeasurementBasisForAssetsInPreviousPeriod', 'InformationOnLeasingContracts', 'FeesForOtherServicesPerformedByAuditors', '\xc3\x85rets', 'RetainedEarnings', 'ContributedCapital', 'CostOfProduction', 'NetIncomeAvailableToCommonStockholdersBasic', 'TaxExpenseOnExtraordinaryEvents', 'Materielle', 'OtherLongtermInvestments', 'ProfitLossFromOrdinaryOperatingActivities', 'CommitmentsAndContingencies', 'EntityCentralIndexKey', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfEquity', 'DisclosureOfCollateralsAndAssetsPledgesAsSecurity', 'ReserveForNetRevaluationAccordingToEquityMethod', 'CashFlowFromOperatingActivitiesBeforeFinancialItems', 'RepaymentOfDebtToCreditInstitutions', 'IncomeFromContinuingOperationsAfterTax', 'InformationOnOtherReceivables', 'konklusion.&lt;/span&gt;&lt;br', 'OtherFinanceExpenses', 'OtherPayables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfOtherOperatingExpenses', 'CompletedDevelopmentProjects', 'PreferredStockDividendsAndOtherAdjustments', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisForInvestmentsInSubsidiariesAndAssociates', 'LongtermInvestmentsAndReceivables', 'DisclosureOfMainActivitiesAndAccountingAndFinancialMatters', 'DescriptionOfAmortisationForIntangibleAssetsExceedingFiveYears', '&lt;br/&gt;Foresl\xc3\xa5et', 'NetIncomeAttributableToParent', 'InformationOnRemunerationOfManagementCategoriesAndSpecialIncentiveProgrammes', 'ContingentLiabilitiesRelatedToGroupEnterprises', 'ShorttermReceivables', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfFinanceIncomeAndExpenses', 'OtherLongtermDebtRaisedByIssuanceOfBonds', 'DepreciationOfPropertyPlantAndEquipment', 'DescriptionOfMethodsOfPrepayments', 'ExtraordinaryIncome', 'DescriptionOfMethodsOfForeignCurrencies', 'OtherEmployeeExpense', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfDeferredIncomeLiabilities', 'SaleOfInvestments', 'DisclosureOfOtherOperatingExpenses', 'DescriptionOfMethodsOfHedgingRecognisedExpectedToReceiveAndAssumedAssetsAndLiabilities', 'AdjustmentsOfHedgingInstruments', 'LongtermReceivablesFromGroupEnterprises', 'OtherFinanceIncomeFromGroupEnterprises', 'AmortisationOfIntangibleAssets', 'ReserveForNetRevaluationOfInvestmentAssets', 'OtherProvisions', 'InformationOnIntragroupTransactions', 'OtherReserves', 'NoncurrentDeferredTaxAssets', 'Chairmen', 'Modervirksomheden', 'PropertyPlantAndEquipment', 'Der', 'Det', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfGainsLossesFromCurrentValueAdjustmentsOfOtherInvestmentAssets', 'LongtermEquityLoan', 'Den', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfRevenue', 'NetCashFlowsOperatingContinuing', 'CashFlowsFromUsedInInvestingActivities', 'PropertyCost', 'ContextForDurations', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfLeaseholdImprovements', 'Efter', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfIntangibleAssets', 'NetIncreaseDecreaseInCashAndCashEquivalents', 'DisposalsOfPropertyPlantAndEquipment', '&lt;br/&gt;som', '&lt;/span&gt;&lt;/p&gt;&lt;p&gt;&lt;br', 'InformationOnChangesAndEffectsOfChangesOnRecognitionAndMeasurementBasisResultingFromChangesInAccountingEstimatesOrErrors', 'ImpairmentLossesAndAmortisationOfDisposedIntangibleAssets', 'ShorttermReceivablesFromGroupEnterprises', 'ShorttermLiabilitiesOtherThanProvisions', 'DepositsLongtermLiabilitiesOtherThanProvisions', 'LongtermReceivablesFromAssociates', 'ImpairmentOfFinancialAssets', 'IntangibleAssetsGross', 'InformationOnAverageNumberOfEmployees', 'NetCashFlowsOperating', 'InterestReceivedClassifiedAsOperatingActivities', 'ProceedsFromSalesOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities', 'GrossProfit', 'ProvisionsForInvestmentsInGroupAssociates', 'LongtermDebtToBanks', 'DescriptionOfMethodsOfRecognitionAndMeasurementBasisOfExternalExpenses', 'AcquisitionOfOtherCompany', 'PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities', 'InvestmentsGross', 'DisclosureOfExternalExpenses', 'LongtermInvestmentsInGroupEnterprises', 'Selskabet', 'IncomeFromInvestmentsInGroupEnterprisesAndAssociates', 'GrossResult', 'BalanceSheetDate', 'AdministrativeExpenses', 'InformationOnReconciliationOfChangesInInvestments', 'AdditionsToIntangibleAssets']
        dic = {}
        #print(dic)
        result_dic = {}
        print(self.xbrl.fields)
        for item in self.xbrl.tags: 
            try:
                item_name = item.split(':')[1]
                if '>' in item_name:
                    item_name = item_name.split('>')[0]
                    item = item.split('>')[0]
            except:item_name = item
            try: dic[item_name] = self.xbrl.GetFactValue(item,'Instant')
            except: 
                try:    dic[item_name] = self.xbrl.GetFactValue(item,'Duration')
                except: dic[item_name] = '0'

                
                #dic['DocumentType'] = unicodedata.normalize("NFKD", self.xbrl.getNode("gsd:InformationOnTypeOfSubmittedReport").text)
                #dic['EntityCentralIndexKey'] = self.xbrl.fields['EntityCentralIndexKey']

            
        
        
        try:dic['CEO'] = self.xbrl.getNode('cmn:NameAndSurnameOfMemberOfExecutiveBoard').text
        except:pass
        try:dic['Chairmen'] = self.xbrl.getNode('gsd:NameAndSurnameOfChairmanOfGeneralMeeting').text
        except:pass
        try: dic['Auditor'] = self.xbrl.getNode('cmn:NameAndSurnameOfAuditor').text
        except: pass
        #try: dic['NameOfReportingEntity'] = self.xbrl.getNode('gsd:NameOfReportingEntity').text
        #except:pass
        
#####print("CREATE TABLE django_sec_new (company_id integer NOT NULL, start_date date NOT NULL, end_date date NOT NULL, "+' character varying(200), '.join(map(str,lst))+" character varying(200))")

        string_lst = []
        
        for item in columns:
            result_dic[item] = 'None'
        
        for value in dic:
            for item in result_dic:
                if value == item:
                    result_dic[item] = dic[value]
        for item in self.xbrl.fields:
            result_dic[item] = self.xbrl.fields[item]                
        
        for item in result_dic:
            #if len(item) > 63:
                #result_dic[item[:63]] = result_dic.pop[item]
            try:string_lst.append("'"+str(result_dic[item])+"'")
            except:string_lst.append("'"+str(result_dic[item].encode('utf-8'))+"'")
        #print(result_dic)
        #string_lst
        l=[]
        #print(result_dic)
        for item in result_dic:
            l.append(item)
        print(l)
	
        
        #for item in result_dic:
        #    try:
        #        result_dic[item] = str(result_dic[item]).replace("'","")
        #    except: pass
            

            #print(123123123)
        """
		try:
                cursor.execute("UPDATE django_sec_lol SET value_name='"+str(item)+"', value='"+str(dic[item])+"' ,start_date='"+str(start_dt)+"',end_date='"+str(end_dt)+"',company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+", doc_type='"+str(self.xbrl.fields['DocumentType'])+"' WHERE value_name='"+str(item)+"' and value='"+str(dic[item])+"' and start_date='"+str(start_dt)+"' and end_date='"+str(end_dt)+"' and company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+" and doc_type='"+str(self.xbrl.fields['DocumentType'])+"';")
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO django_sec_lol SELECT '"+str(item)+"','"+str(dic[item])+"' ,'"+str(start_dt)+"','"+str(end_dt)+"',"+str(self.xbrl.fields['EntityCentralIndexKey'])+", '"+str(self.xbrl.fields['DocumentType'])+"' WHERE NOT EXISTS(select 1 from django_sec_lol where  value_name='"+str(item)+"' and  value='"+str(dic[item])+"' and start_date='"+str(start_dt)+"' and end_date='"+str(end_dt)+"' and company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+" and doc_type='"+str(self.xbrl.fields['DocumentType'])+"')")"""
        try:
            cursor.execute("INSERT INTO django_sec_new VALUES("+self.xbrl.fields['EntityCentralIndexKey']+", '"+start_dt+"', '"+end_dt+"', "+', '.join(string_lst)+")")
                
                #conn.commit()
        except Exception as e:
            #print(66666)
            print(e)
            pass
                #print(77777777777)
        conn.commit()
            #print(dic['Assets'])
            #print(result_dic['Assets'])
        conn.close()
        cursor.close()
        #os.system('python '+os.path.dirname(os.path.realpath(__file__))+'/adjuster.py')
        #print('adJUSTED!!!!')'''
        #Key ratios'''
        #print(dic)

        






