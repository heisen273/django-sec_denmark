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
        
        self.xbrl.fields['Assets'] = self.xbrl.GetFactValue("e:Assets","Instant")
        if self.xbrl.fields['Assets']== None:
            self.xbrl.fields['Assets'] = 0

        #Current Assets
        self.xbrl.fields['CurrentAssets'] = self.xbrl.GetFactValue("e:CurrentAssets", "Instant")
        if self.xbrl.fields['CurrentAssets']== None:
            self.xbrl.fields['CurrentAssets'] = 0
                
        #Noncurrent Assets
        self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("e:AssetsNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentAssets']==None:
            self.xbrl.fields['NoncurrentAssets'] = self.xbrl.GetFactValue("e:NoncurrentAssets", "Instant")
            if self.xbrl.fields['NoncurrentAssets']==None:
                if self.xbrl.fields['Assets'] and self.xbrl.fields['CurrentAssets']:
                    self.xbrl.fields['NoncurrentAssets'] = self.xbrl.fields['Assets'] - self.xbrl.fields['CurrentAssets']
                else:
                    self.xbrl.fields['NoncurrentAssets'] = 0
                
        #LiabilitiesAndEquity
        self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("e:LiabilitiesAndStockholdersEquity", "Instant")
        if self.xbrl.fields['LiabilitiesAndEquity']== None:
            self.xbrl.fields['LiabilitiesAndEquity'] = self.xbrl.GetFactValue("e:LiabilitiesAndPartnersCapital", "Instant")
            if self.xbrl.fields['LiabilitiesAndEquity']== None:
                self.xbrl.fields['LiabilitiesAndEquity'] = 0
        
        #Liabilities
        self.xbrl.fields['Liabilities'] = self.xbrl.GetFactValue("e:Liabilities", "Instant")
        if self.xbrl.fields['Liabilities']== None:
            self.xbrl.fields['Liabilities'] = 0
        #CurrentLiabilities
        self.xbrl.fields['CurrentLiabilities'] = self.xbrl.GetFactValue("e:LiabilitiesCurrent", "Instant")
        if self.xbrl.fields['CurrentLiabilities']== None:
            self.xbrl.fields['CurrentLiabilities'] = 0
                
        #Noncurrent Liabilities
        self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("e:LiabilitiesNoncurrent", "Instant")
        if self.xbrl.fields['NoncurrentLiabilities']== None:
            self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.GetFactValue("e:LiabilitiesNoncurrent", "Instant")
            if self.xbrl.fields['NoncurrentLiabilities']== None:
                if self.xbrl.fields['Liabilities'] and self.xbrl.fields['CurrentLiabilities']:
                    self.xbrl.fields['NoncurrentLiabilities'] = self.xbrl.fields['Liabilities'] - self.xbrl.fields['CurrentLiabilities']
                else:
                    self.xbrl.fields['NoncurrentLiabilities'] = 0
                
        #CommitmentsAndContingencies
        self.xbrl.fields['CommitmentsAndContingencies'] = self.xbrl.GetFactValue("e:CommitmentsAndContingencies", "Instant")
        if self.xbrl.fields['CommitmentsAndContingencies']== None:
            self.xbrl.fields['CommitmentsAndContingencies'] = 0
                
        #TemporaryEquity
        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:TemporaryEquityRedemptionValue", "Instant")
        if self.xbrl.fields['TemporaryEquity'] == None:
            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:RedeemablePreferredStockCarryingAmount", "Instant")
            if self.xbrl.fields['TemporaryEquity'] == None:
                self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:TemporaryEquityCarryingAmount", "Instant")
                if self.xbrl.fields['TemporaryEquity'] == None:
                    self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:TemporaryEquityValueExcludingAdditionalPaidInCapital", "Instant")
                    if self.xbrl.fields['TemporaryEquity'] == None:
                        self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:TemporaryEquityCarryingAmountAttributableToParent", "Instant")
                        if self.xbrl.fields['TemporaryEquity'] == None:
                            self.xbrl.fields['TemporaryEquity'] = self.xbrl.GetFactValue("e:RedeemableNoncontrollingInterestEquityFairValue", "Instant")
                            if self.xbrl.fields['TemporaryEquity'] == None:
                                self.xbrl.fields['TemporaryEquity'] = 0
                 
        #RedeemableNoncontrollingInterest (added to temporary equity)
        RedeemableNoncontrollingInterest = None
        
        RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("e:RedeemableNoncontrollingInterestEquityCarryingAmount", "Instant")
        if RedeemableNoncontrollingInterest == None:
            RedeemableNoncontrollingInterest = self.xbrl.GetFactValue("e:RedeemableNoncontrollingInterestEquityCommonCarryingAmount", "Instant")
            if RedeemableNoncontrollingInterest == None:
                RedeemableNoncontrollingInterest = 0

        #This adds redeemable noncontrolling interest and temporary equity which are rare, but can be reported seperately
        if self.xbrl.fields['TemporaryEquity']:
            self.xbrl.fields['TemporaryEquity'] = float(self.xbrl.fields['TemporaryEquity']) + float(RedeemableNoncontrollingInterest)


        #Equity
        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest", "Instant")
        if self.xbrl.fields['Equity'] == None:
            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:Equity", "Instant")
            if self.xbrl.fields['Equity'] == None:
                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest", "Instant")
                if self.xbrl.fields['Equity'] == None:
                    self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:PartnersCapital", "Instant")
                    if self.xbrl.fields['Equity'] == None:
                        self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:CommonStockholdersEquity", "Instant")
                        if self.xbrl.fields['Equity'] == None:
                            self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:MemberEquity", "Instant")
                            if self.xbrl.fields['Equity'] == None:
                                self.xbrl.fields['Equity'] = self.xbrl.GetFactValue("e:AssetsNet", "Instant")
                                if self.xbrl.fields['Equity'] == None:
                                    self.xbrl.fields['Equity'] = 0
        

        #EquityAttributableToNoncontrollingInterest
        self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("e:MinorityInterest", "Instant")
        if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
            self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("e:PartnersCapitalAttributableToNoncontrollingInterest", "Instant")
            if self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] == None:
                self.xbrl.fields['EquityAttributableToNoncontrollingInterest'] = 0
        
        #EquityAttributableToParent
        self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("e:StockholdersEquity", "Instant")
        if self.xbrl.fields['EquityAttributableToParent'] == None:
            self.xbrl.fields['EquityAttributableToParent'] = self.xbrl.GetFactValue("e:LiabilitiesAndPartnersCapital", "Instant")
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
        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:Revenue", "Duration")
        if self.xbrl.fields['Revenue'] == None:
            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:SalesRevenueNet", "Duration")
            if self.xbrl.fields['Revenue'] == None:
                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:SalesRevenueervicesNet", "Duration")
                if self.xbrl.fields['Revenue'] == None:
                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:RevenueNetOfInterestExpense", "Duration")
                    if self.xbrl.fields['Revenue'] == None:
                        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:RegulatedAndUnregulatedOperatingRevenue", "Duration")
                        if self.xbrl.fields['Revenue'] == None:
                            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:HealthCareOrganizationRevenue", "Duration")
                            if self.xbrl.fields['Revenue'] == None:
                                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:InterestAndDividendIncomeOperating", "Duration")
                                if self.xbrl.fields['Revenue'] == None:
                                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:RealEstateRevenueNet", "Duration")
                                    if self.xbrl.fields['Revenue'] == None:
                                        self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:RevenueMineralSales", "Duration")
                                        if self.xbrl.fields['Revenue'] == None:
                                            self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:OilAndGasRevenue", "Duration")
                                            if self.xbrl.fields['Revenue'] == None:
                                                self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:FinancialServicesRevenue", "Duration")
                                                if self.xbrl.fields['Revenue'] == None:
                                                    self.xbrl.fields['Revenue'] = self.xbrl.GetFactValue("e:RegulatedAndUnregulatedOperatingRevenue", "Duration")                                                
                                                    if self.xbrl.fields['Revenue'] == None:
                                                        self.xbrl.fields['Revenue'] = 0


        #CostOfRevenue
        self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("e:CostOfRevenue", "Duration")
        if self.xbrl.fields['CostOfRevenue'] == None:
            self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("e:CostOfServices", "Duration")
            if self.xbrl.fields['CostOfRevenue'] == None:
                self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("e:CostOfGoodsSold", "Duration")
                if self.xbrl.fields['CostOfRevenue'] == None:
                    self.xbrl.fields['CostOfRevenue'] = self.xbrl.GetFactValue("e:CostOfGoodsAndServicesSold", "Duration")
                    if self.xbrl.fields['CostOfRevenue'] == None:
                        self.xbrl.fields['CostOfRevenue'] = 0
     
        #GrossProfit
        self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("e:GrossProfit", "Duration")
        if self.xbrl.fields['GrossProfit'] == None:
            self.xbrl.fields['GrossProfit'] = self.xbrl.GetFactValue("e:GrossProfit", "Duration")
            if self.xbrl.fields['GrossProfit'] == None:
                self.xbrl.fields['GrossProfit'] = 0
     
        #OperatingExpenses
        self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("e:OperatingExpenses", "Duration")
        if self.xbrl.fields['OperatingExpenses'] == None:
            self.xbrl.fields['OperatingExpenses'] = self.xbrl.GetFactValue("e:OperatingCostsAndExpenses", "Duration")  #This concept seems incorrect.
            if self.xbrl.fields['OperatingExpenses'] == None:
                self.xbrl.fields['OperatingExpenses'] = 0
        #CostsAndExpenses
        self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("e:CostsAndExpenses", "Duration")
        if self.xbrl.fields['CostsAndExpenses'] == None:
            self.xbrl.fields['CostsAndExpenses'] = self.xbrl.GetFactValue("e:CostsAndExpenses", "Duration")
            if self.xbrl.fields['CostsAndExpenses'] == None:
                self.xbrl.fields['CostsAndExpenses'] = 0
     
        #OtherOperatingIncome
        self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("e:OtherOperatingIncome", "Duration")
        if self.xbrl.fields['OtherOperatingIncome'] == None:
            self.xbrl.fields['OtherOperatingIncome'] = self.xbrl.GetFactValue("e:OtherOperatingIncome", "Duration")
            if self.xbrl.fields['OtherOperatingIncome'] == None:
                self.xbrl.fields['OtherOperatingIncome'] = 0
     
        #OperatingIncomeLoss
        self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("e:OperatingIncomeLoss", "Duration")
        if self.xbrl.fields['OperatingIncomeLoss'] == None:
            self.xbrl.fields['OperatingIncomeLoss'] = self.xbrl.GetFactValue("e:OperatingIncomeLoss", "Duration")
            if self.xbrl.fields['OperatingIncomeLoss'] == None:
                self.xbrl.fields['OperatingIncomeLoss'] = 0
     
        #NonoperatingIncomeLoss
        self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("e:NonoperatingIncomeExpense", "Duration")
        if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
            self.xbrl.fields['NonoperatingIncomeLoss'] = self.xbrl.GetFactValue("e:NonoperatingIncomeExpense", "Duration")
            if self.xbrl.fields['NonoperatingIncomeLoss'] == None:
                self.xbrl.fields['NonoperatingIncomeLoss'] = 0

        #InterestAndDebtExpense
        self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("e:InterestAndDebtExpense", "Duration")
        if self.xbrl.fields['InterestAndDebtExpense'] == None:
            self.xbrl.fields['InterestAndDebtExpense'] = self.xbrl.GetFactValue("e:InterestAndDebtExpense", "Duration")
            if self.xbrl.fields['InterestAndDebtExpense'] == None:
                self.xbrl.fields['InterestAndDebtExpense'] = 0

        #IncomeBeforeEquityMethodInvestments
        self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
            self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeBeforeEquityMethodInvestments'] = 0
     
        #IncomeFromEquityMethodInvestments
        self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("e:IncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
            self.xbrl.fields['IncomeFromEquityMethodInvestments'] = self.xbrl.GetFactValue("e:IncomeLossFromEquityMethodInvestments", "Duration")
            if self.xbrl.fields['IncomeFromEquityMethodInvestments'] == None:
                self.xbrl.fields['IncomeFromEquityMethodInvestments'] = 0
     
        #IncomeFromContinuingOperationsBeforeTax
        self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
            self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] = 0
     
        #IncomeTaxExpenseBenefit
        self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("e:IncomeTaxExpenseBenefit", "Duration")
        if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
            self.xbrl.fields['IncomeTaxExpenseBenefit'] = self.xbrl.GetFactValue("e:IncomeTaxExpenseBenefitContinuingOperations", "Duration")
            if self.xbrl.fields['IncomeTaxExpenseBenefit'] == None:
                self.xbrl.fields['IncomeTaxExpenseBenefit'] = 0
        #IncomeFromContinuingOperationsAfterTax
        self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("e:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
        if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
            self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = self.xbrl.GetFactValue("e:IncomeLossBeforeExtraordinaryItemsAndCumulativeEffectOfChangeInAccountingPrinciple", "Duration")
            if self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] == None:
                self.xbrl.fields['IncomeFromContinuingOperationsAfterTax'] = 0

        #IncomeFromDiscontinuedOperations
        self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("e:IncomeLossFromDiscontinuedOperationsNetOfTax", "Duration")
        if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
            self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("e:DiscontinuedOperationGainLossOnDisposalOfDiscontinuedOperationNetOfTax", "Duration")
            if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                self.xbrl.fields['IncomeFromDiscontinuedOperations'] = self.xbrl.GetFactValue("e:IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity", "Duration")
                if self.xbrl.fields['IncomeFromDiscontinuedOperations']== None:
                    self.xbrl.fields['IncomeFromDiscontinuedOperations'] = 0

        #ExtraordaryItemsGainLoss
        self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("e:ExtraordinaryItemNetOfTax", "Duration")
        if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
            self.xbrl.fields['ExtraordaryItemsGainLoss'] = self.xbrl.GetFactValue("e:ExtraordinaryItemNetOfTax", "Duration")
            if self.xbrl.fields['ExtraordaryItemsGainLoss']== None:
                self.xbrl.fields['ExtraordaryItemsGainLoss'] = 0
        #NetIncomeLoss
        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:ProfitLoss", "Duration")
        if self.xbrl.fields['NetIncomeLoss']== None:
            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:NetIncomeLoss", "Duration")
            if self.xbrl.fields['NetIncomeLoss']== None:
                self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
                if self.xbrl.fields['NetIncomeLoss']== None:
                    self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperations", "Duration")
                    if self.xbrl.fields['NetIncomeLoss']== None:
                        self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:IncomeLossAttributableToParent", "Duration")
                        if self.xbrl.fields['NetIncomeLoss']== None:
                            self.xbrl.fields['NetIncomeLoss'] = self.xbrl.GetFactValue("e:IncomeLossFromContinuingOperationsIncludingPortionAttributableToNoncontrollingInterest", "Duration")
                            if self.xbrl.fields['NetIncomeLoss']== None:
                                self.xbrl.fields['NetIncomeLoss'] = 0

        #NetIncomeAvailableToCommonStockholdersBasic
        self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = self.xbrl.GetFactValue("e:NetIncomeLossAvailableToCommonStockholdersBasic", "Duration")
        if self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic']== None:
            self.xbrl.fields['NetIncomeAvailableToCommonStockholdersBasic'] = 0
                
        #PreferredStockDividendsAndOtherAdjustments
        self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = self.xbrl.GetFactValue("e:PreferredStockDividendsAndOtherAdjustments", "Duration")
        if self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments']== None:
            self.xbrl.fields['PreferredStockDividendsAndOtherAdjustments'] = 0
                
        #NetIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("e:NetIncomeLossAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest']== None:
            self.xbrl.fields['NetIncomeAttributableToNoncontrollingInterest'] = 0
                
        #NetIncomeAttributableToParent
        self.xbrl.fields['NetIncomeAttributableToParent'] = self.xbrl.GetFactValue("e:NetIncomeLoss", "Duration")
        if self.xbrl.fields['NetIncomeAttributableToParent']== None:
            self.xbrl.fields['NetIncomeAttributableToParent'] = 0

        #OtherComprehensiveIncome
        self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("e:OtherComprehensiveIncomeLossNetOfTax", "Duration")
        if self.xbrl.fields['OtherComprehensiveIncome']== None:
            self.xbrl.fields['OtherComprehensiveIncome'] = self.xbrl.GetFactValue("e:OtherComprehensiveIncomeLossNetOfTax", "Duration")
            if self.xbrl.fields['OtherComprehensiveIncome']== None:
                self.xbrl.fields['OtherComprehensiveIncome'] = 0

        #ComprehensiveIncome
        self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTaxIncludingPortionAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncome']== None:
            self.xbrl.fields['ComprehensiveIncome'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncome']== None:
                self.xbrl.fields['ComprehensiveIncome'] = 0

        #ComprehensiveIncomeAttributableToParent
        self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTax", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTax", "Duration")
            if self.xbrl.fields['ComprehensiveIncomeAttributableToParent']== None:
                self.xbrl.fields['ComprehensiveIncomeAttributableToParent'] = 0
     
        #ComprehensiveIncomeAttributableToNoncontrollingInterest
        self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
        if self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest']==None:
            self.xbrl.fields['ComprehensiveIncomeAttributableToNoncontrollingInterest'] = self.xbrl.GetFactValue("e:ComprehensiveIncomeNetOfTaxAttributableToNoncontrollingInterest", "Duration")
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
                
       
        self.xbrl.fields['NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments'] = self.xbrl.fields['IncomeFromContinuingOperationsBeforeTax'] - self.xbrl.fields['OperatingIncomeLoss']
    
        #NonoperatingIncomeLossPlusInterestAndDebtExpense
        if self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense']== 0 and self.xbrl.fields['NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments']!=0:
            self.xbrl.fields['NonoperatingIncomeLossPlusInterestAndDebtExpense'] = self.xbrl.fields['NonoperatingIncomePlusInterestAndDebtExpensePlusIncomeFromEquityMethodInvestments'] - self.xbrl.fields['IncomeFromEquityMethodInvestments']
    
       
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
        self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("e:CashAndCashEquivalentsPeriodIncreaseDecrease", "Duration")
        if self.xbrl.fields['NetCashFlow']== None:
            self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("e:CashPeriodIncreaseDecrease", "Duration")
            if self.xbrl.fields['NetCashFlow']== None:
                self.xbrl.fields['NetCashFlow'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInContinuingOperations", "Duration")
                if self.xbrl.fields['NetCashFlow']== None:
                    self.xbrl.fields['NetCashFlow'] = 0
                
        #NetCashFlowsOperating
        self.xbrl.fields['NetCashFlowsOperating'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInOperatingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsOperating']== None:
            self.xbrl.fields['NetCashFlowsOperating'] = 0
                
        #NetCashFlowsInvesting
        self.xbrl.fields['NetCashFlowsInvesting'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInInvestingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsInvesting']== None:
            self.xbrl.fields['NetCashFlowsInvesting'] = 0
                
        #NetCashFlowsFinancing
        self.xbrl.fields['NetCashFlowsFinancing'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInFinancingActivities", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancing']== None:
            self.xbrl.fields['NetCashFlowsFinancing'] = 0
        #NetCashFlowsOperatingContinuing
        self.xbrl.fields['NetCashFlowsOperatingContinuing'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingContinuing']== None:
            self.xbrl.fields['NetCashFlowsOperatingContinuing'] = 0
                
        #NetCashFlowsInvestingContinuing
        self.xbrl.fields['NetCashFlowsInvestingContinuing'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInInvestingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingContinuing']== None:
            self.xbrl.fields['NetCashFlowsInvestingContinuing'] = 0
                
        #NetCashFlowsFinancingContinuing
        self.xbrl.fields['NetCashFlowsFinancingContinuing'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInFinancingActivitiesContinuingOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingContinuing']== None:
            self.xbrl.fields['NetCashFlowsFinancingContinuing'] = 0
                
        #NetCashFlowsOperatingDiscontinued
        self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = self.xbrl.GetFactValue("e:CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsOperatingDiscontinued']==None:
            self.xbrl.fields['NetCashFlowsOperatingDiscontinued'] = 0
                
        #NetCashFlowsInvestingDiscontinued
        self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = self.xbrl.GetFactValue("e:CashProvidedByUsedInInvestingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsInvestingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsInvestingDiscontinued'] = 0
                
        #NetCashFlowsFinancingDiscontinued
        self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = self.xbrl.GetFactValue("e:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsFinancingDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsFinancingDiscontinued'] = 0
                
        #NetCashFlowsDiscontinued
        self.xbrl.fields['NetCashFlowsDiscontinued'] = self.xbrl.GetFactValue("e:NetCashProvidedByUsedInDiscontinuedOperations", "Duration")
        if self.xbrl.fields['NetCashFlowsDiscontinued']== None:
            self.xbrl.fields['NetCashFlowsDiscontinued'] = 0
                
        #ExchangeGainsLosses
        self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("e:EffectOfExchangeRateOnCashAndCashEquivalents", "Duration")
        if self.xbrl.fields['ExchangeGainsLosses']== None:
            self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("e:EffectOfExchangeRateOnCashAndCashEquivalentsContinuingOperations", "Duration")
            if self.xbrl.fields['ExchangeGainsLosses']== None:
                self.xbrl.fields['ExchangeGainsLosses'] = self.xbrl.GetFactValue("e:CashProvidedByUsedInFinancingActivitiesDiscontinuedOperations", "Duration")
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
        start_dt = self.xbrl.getNode("c:ReportingPeriodStartDate").text
        end_dt = self.xbrl.getNode("c:ReportingPeriodEndDate").text
        
        dic = {}
        #print(dic)
        for item in self.xbrl.tags: 
            if item[0] == '/':
                pass
            else: item = 'e'+item
           
            try:
                item_name = item.split(':')[1]
            except:continue
            try:
                dic[item_name] = self.xbrl.GetFactValue(item,'Instant')
                if dic[item_name] == None:
                    dic[item_name] = self.xbrl.GetFactValue(item,'Duration')
                    if dic[item_name] == None:
                        dic[item_name] = '0'
                dic['CEO'] = self.xbrl.getNode('d:NameAndSurnameOfMemberOfExecutiveBoard').text
                dic['Chairmen'] = self.xbrl.getNode('c:NameAndSurnameOfChairmanOfGeneralMeeting').text
                dic['Auditor'] = self.xbrl.getNode('d:NameAndSurnameOfAuditor').text
                #dic['DocumentType'] = unicodedata.normalize("NFKD", self.xbrl.getNode("gsd:InformationOnTypeOfSubmittedReport").text)
                #dic['EntityCentralIndexKey'] = self.xbrl.fields['EntityCentralIndexKey']

            
            except: pass    
        i = 0 
        print(dic)
        #print('antoha',unicodedata.normalize("NFKD", self.xbrl.getNode("gsd:InformationOnTypeOfSubmittedReport").text))
        #print('lol',)
        for item in dic:
            try:
                dic[item] = str(dic[item]).replace("'","")
            except: pass
                
            i += 1
            if i % 1000 == 0:
                conn.commit() 
            #print(123123123)
            try:
                cursor.execute("UPDATE django_sec_lol SET value_name='"+str(item)+"', value='"+str(dic[item])+"' ,start_date='"+str(start_dt)+"',end_date='"+str(end_dt)+"',company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+", doc_type='"+str(self.xbrl.fields['DocumentType'])+"' WHERE value_name='"+str(item)+"' and value='"+str(dic[item])+"' and start_date='"+str(start_dt)+"' and end_date='"+str(end_dt)+"' and company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+" and doc_type='"+str(self.xbrl.fields['DocumentType'])+"';")
                if cursor.rowcount == 0:
                    cursor.execute("INSERT INTO django_sec_lol SELECT '"+str(item)+"','"+str(dic[item])+"' ,'"+str(start_dt)+"','"+str(end_dt)+"',"+str(self.xbrl.fields['EntityCentralIndexKey'])+", '"+str(self.xbrl.fields['DocumentType'])+"' WHERE NOT EXISTS(select 1 from django_sec_lol where  value_name='"+str(item)+"' and  value='"+str(dic[item])+"' and start_date='"+str(start_dt)+"' and end_date='"+str(end_dt)+"' and company_id="+str(self.xbrl.fields['EntityCentralIndexKey'])+" and doc_type='"+str(self.xbrl.fields['DocumentType'])+"')")
                
                #conn.commit()
            except Exception as e:
                #print(66666)
                #print(e)
                pass
                #print(77777777777)
            conn.commit()
        conn.close()
        cursor.close()
        #os.system('python '+os.path.dirname(os.path.realpath(__file__))+'/adjuster.py')
        #print('adJUSTED!!!!')'''
        #Key ratios'''
        #print(dic)
        






